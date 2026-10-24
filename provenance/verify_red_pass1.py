"""Verify the fixed Red Book Pass 1 import and preserved v0.6 base; Python 3.10+."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = "6cf26e538a0c6d1ffae8453a5b4fb33872cce62b"
MANIFEST = "provenance/RED_PASS1_SNAPSHOT_SHA256.json"
APPENDED = {"LIVE_MODEL.md", "README.md", "canon/DECISIONS.md", "world_clock/README.md", "provenance/CHANGELOG.md"}
BOOKS = ("RED", "ORANGE", "YELLOW", "GREEN", "BLUE", "VIOLET", "WHITE")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def record(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--git-index", action="store_true")
    selection.add_argument("--commit")
    args = parser.parse_args()
    manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    require(manifest["base_commit"] == BASE, "Unexpected base commit")
    actual = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in (".git", "_inbox") or "__pycache__" in relative.parts:
            continue
        require(not path.is_symlink() and ".git" not in relative.parts, f"Unexpected symlink or Git metadata: {relative}")
        if path.is_file() and path.suffix != ".pyc":
            actual.add(relative.as_posix())
    require(actual == set(manifest["files"]) | {MANIFEST}, "Current file inventory changed")
    current = {name: (ROOT / name).read_bytes() for name in actual}
    for name, info in manifest["files"].items():
        require(record(current[name]) == info, f"Current hash mismatch: {name}")
    require(Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve() == ROOT, "Wrong Git root")
    names = set(git("ls-tree", "-r", "--name-only", "-z", BASE).decode().rstrip("\0").split("\0"))
    require(len(names) == 56 and names <= actual, "Base file missing")
    base = {name: git("show", f"{BASE}:{name}") for name in names}
    require(set(manifest["base_files"]) == names, "Base inventory mismatch")
    for name, data in base.items():
        require(record(data) == manifest["base_files"][name], f"Base hash mismatch: {name}")
    old_manifest = json.loads(base["provenance/V06_SNAPSHOT_SHA256.json"])
    require(set(old_manifest["files"]) == names - {"provenance/V06_SNAPSHOT_SHA256.json"}, "Previous snapshot coverage mismatch")
    for name, info in old_manifest["files"].items():
        require(record(base[name]) == info, f"Previous snapshot mismatch: {name}")
    changed = {name for name in names if current[name] != base[name]}
    require(changed == APPENDED == set(manifest["modified_paths"]), "Unexpected base modification")
    for name in APPENDED:
        require(current[name].startswith(base[name]), f"Historical prefix changed: {name}")
    require(actual - names == set(manifest["added_paths"]) and len(actual) == 66, "Unexpected addition")
    expected_payload = {"CODEX_UPDATE_PROMPT.md", "README.md", "provenance/SHA256.json", "narrative/RED/LIVE_MODEL.md"} | {f"narrative/RED/ARC_{i:02d}_SUMMARY.md" for i in range(1, 6)}
    require(set(manifest["archive_files"]) == expected_payload, "Archive inventory mismatch")
    supplied = manifest["source_manifest"]
    require(set(supplied) == expected_payload - {"provenance/SHA256.json"}, "Source manifest coverage mismatch")
    for name, digest in supplied.items():
        require(manifest["archive_files"][name]["sha256"] == digest, f"Source digest mismatch: {name}")
    imported = {name for name in expected_payload if name.startswith("narrative/RED/")}
    require(imported == set(manifest["imported_paths"]), "Wrong imported paths")
    for name in imported:
        require(record(current[name]) == manifest["archive_files"][name], f"Imported bytes changed: {name}")
    archive = ROOT / "_inbox" / manifest["archive"]["name"]
    if archive.exists():
        info = manifest["archive"]
        require(record(archive.read_bytes()) == {"bytes": info["bytes"], "sha256": info["sha256"]}, "ZIP hash mismatch")
        with zipfile.ZipFile(archive) as z:
            require(z.testzip() is None and len(z.infolist()) == 9 and set(z.namelist()) == expected_payload, "ZIP CRC/inventory failure")
            for name in z.namelist():
                require(record(z.read(name)) == manifest["archive_files"][name], f"ZIP entry mismatch: {name}")
            require(json.loads(z.read("provenance/SHA256.json")) == supplied, "Supplied manifest mismatch")
    text = {}
    for name, data in current.items():
        if Path(name).suffix in (".md", ".json", ".csv", ".py") or name in (".gitattributes", ".gitignore"):
            text[name] = data.decode("utf-8", errors="strict")
            require("\x00" not in text[name] and "\ufffd" not in text[name], f"Invalid UTF-8 text: {name}")
    for book in BOOKS:
        name = f"narrative/{book}/ARCS.md"
        require(current[name] == base[name], f"Title registry changed: {book}")
        require(re.findall(r"^## (\d{2}) ", text[name], re.M) == ["01", "02", "03", "04", "05"], f"Arc heading count: {book}")
    registry = dict(re.findall(r"^## (\d{2}) (.+)$", text["narrative/RED/ARCS.md"], re.M))
    accepted = []
    for number in range(1, 6):
        name = f"narrative/RED/ARC_{number:02d}_SUMMARY.md"
        content = text[name]
        header = re.match(r"# Red — Arc (\d{2}): (.+)", content)
        require(header is not None and header[1] == f"{number:02d}" and header[2] == registry[header[1]], f"Arc title mismatch: {name}")
        require("**Status:** ACCEPTED — Pass 1 narrative skeleton; detailed scene and chapter plans OPEN." in content, f"Acceptance scope changed: {name}")
        beats = re.findall(r"^### (\d+)\. ", content, re.M)
        require(beats == [str(i) for i in range(1, (4 if number == 2 else 5) + 1)], f"Beat order/count mismatch: {name}")
        for phrase in ("## Outcome", "## Transition", "NOT consequences of the ancient weaving network", "Municipal stabilization sigils are independent", "not a finished manuscript or proven mathematical derivation", "Transduction, velis, ru’ne, realm access, White superposition"):
            require(phrase in content, f"Missing safeguard/structure in {name}")
        require(not re.search(r"\b\d{4}-\d{2}-\d{2}\b", content), f"Unexpected in-world date: {name}")
        accepted.append({"number": header[1], "title": header[2], "beats": len(beats)})
    live_titles = dict(re.findall(r"^(\d{2})\. \*\*(.+?)\*\*", text["narrative/RED/LIVE_MODEL.md"], re.M))
    require(live_titles == registry, "Red live-model titles do not match registry")
    require("Orange Arc 01: The Living Threshold" in text["narrative/RED/ARC_05_SUMMARY.md"] and "## 01 The Living Threshold" in text["narrative/ORANGE/ARCS.md"], "Orange handoff mismatch")
    for version in ("", "_V2"):
        clock_name = f"world_clock/REALM_CLOCKS{version}.csv"
        event_name = f"world_clock/EVENTS{version}.csv"
        require(current[clock_name] == base[clock_name] and current[event_name] == base[event_name], "Chronology source changed")
        clocks = list(csv.DictReader(io.StringIO(text[clock_name])))
        require(len(clocks) == 7 and clocks[0]["realm"] == "White" and clocks[0]["white_to_local_factor"] == "1", "Clock reference changed")
        require(all(not row["white_to_local_factor"] and row["status"] == "OPEN" for row in clocks[1:]), "Realm ratio invented")
        events = list(csv.DictReader(io.StringIO(text[event_name])))
        require([(r["event_id"], r["book"], r["arc"]) for r in events] == [("E0001", "RED", "01"), ("E0002", "RED", "01"), ("E0003", "WHITE", "05")], "Event anchors changed")
        require(all(not r["white_date"] for r in events), "Event date invented")
    links = 0
    for name, content in text.items():
        if not name.endswith(".md"):
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            path = ((ROOT / name).parent / unquote(parsed.path)).resolve()
            require(path.is_relative_to(ROOT) and path.exists(), f"Broken local link: {name} -> {target}")
            links += 1
    require(not any(Path(n).suffix.lower() in (".zip", ".tar", ".gz", ".7z") for n in actual), "Unexpected committed archive")
    patterns = [r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{30,}", r"AKIA[0-9A-Z]{16}", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"]
    for name, content in text.items():
        require(not any(re.search(p, content) for p in patterns), f"Possible credential in {name}")
    if args.git_index or args.commit:
        if args.git_index:
            tracked = git("ls-files", "-z")
            prefix = ":"
        else:
            commit = git("rev-parse", "--verify", f"{args.commit}^{{commit}}").decode().strip()
            git("merge-base", "--is-ancestor", BASE, commit)
            tracked = git("ls-tree", "-r", "--name-only", "-z", commit)
            prefix = commit + ":"
        require(set(tracked.decode().rstrip("\0").split("\0")) == actual, "Git inventory mismatch")
        for name in actual:
            require(git("show", prefix + name) == current[name], f"Git bytes mismatch: {name}")
    print(json.dumps({"result": "PASS", "base_commit": BASE, "project_files": len(actual), "snapshot_hashes": len(manifest["files"]), "unchanged_base_files": len(base)-len(changed), "append_only_base_files": len(changed), "added_files": len(actual-names), "archive_checked": archive.exists(), "source_manifest_entries": len(supplied), "imported_narrative_files": len(imported), "utf8_files": len(text), "accepted_arcs": accepted, "unchanged_registry_headings": 35, "unchanged_clock_csvs": 4, "local_links": links, "git_index_checked": args.git_index, "commit_checked": args.commit, "limitations": ["Older fixed-inventory verifiers apply to their original checkouts.", "Missing ZIP availability is reported; imported files still match recorded source hashes.", "Chapter plans, optional details and remaining continuity questions are qualified in the audit."]}, indent=2))


if __name__ == "__main__":
    main()
