"""Verify the fixed Orange Pass 1 snapshot and preserved Red base; Python 3.10+."""

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
BASE = "82753131518018e94a65d37178de05a87d1ecee3"
MANIFEST = "provenance/ORANGE_PASS1_SNAPSHOT_SHA256.json"
PRIOR = "provenance/RED_PASS1_SNAPSHOT_SHA256.json"
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
    require(len(names) == 66 and names <= actual, "Base file missing")
    base = {name: git("show", f"{BASE}:{name}") for name in names}
    require(set(manifest["base_files"]) == names, "Base inventory mismatch")
    for name, data in base.items():
        require(record(data) == manifest["base_files"][name], f"Base hash mismatch: {name}")
    previous = json.loads(base[PRIOR])
    require(set(previous["files"]) == names - {PRIOR}, "Previous snapshot coverage mismatch")
    for name, info in previous["files"].items():
        require(record(base[name]) == info, f"Previous snapshot mismatch: {name}")
    changed = {name for name in names if current[name] != base[name]}
    require(changed == APPENDED == set(manifest["modified_paths"]) == set(manifest["append_only_paths"]), "Unexpected base modification")
    for name in APPENDED:
        require(current[name].startswith(base[name]), f"Historical prefix changed: {name}")
    require(actual - names == set(manifest["added_paths"]) and len(actual) == 76, "Unexpected addition")
    preserved_red = {name for name in names if name.startswith("narrative/RED/")}
    require(len(preserved_red) == 8 and all(current[n] == base[n] for n in preserved_red), "Red records changed")
    require(all(current[n] == base[n] for n in names if n.startswith("world_clock/") and n != "world_clock/README.md"), "World Clock records changed")
    imported = {"narrative/ORANGE/LIVE_MODEL.md"} | {f"narrative/ORANGE/ARC_{i:02d}_SUMMARY.md" for i in range(1, 6)}
    wrappers = {"CODEX_UPDATE_PROMPT.md", "README.md", "provenance/SHA256.json"}
    payload = imported | wrappers
    require(set(manifest["archive_files"]) == payload and set(manifest["imported_paths"]) == imported, "Archive/import inventory mismatch")
    source = manifest["source_manifest"]
    require(source["schema"] == "mk173-orange-pass1-sha256-v1", "Unexpected source schema")
    supplied = source["files"]
    require(set(supplied) == payload - {"provenance/SHA256.json"}, "Source manifest coverage mismatch")
    for name, digest in supplied.items():
        require(manifest["archive_files"][name]["sha256"] == digest, f"Source digest mismatch: {name}")
    for name in imported:
        require(record(current[name]) == manifest["archive_files"][name], f"Imported bytes changed: {name}")
    require({c["path"] for c in manifest["wrapper_conflicts"]} == wrappers, "Wrapper records incomplete")
    for conflict in manifest["wrapper_conflicts"]:
        name = conflict["path"]
        require(record(base[name])["sha256"] == conflict["base_sha256"], f"Wrapper base mismatch: {name}")
        require(conflict["archive_sha256"] == manifest["archive_files"][name]["sha256"], f"Wrapper source mismatch: {name}")
    archive = ROOT / "_inbox" / manifest["archive"]["name"]
    if archive.exists():
        info = manifest["archive"]
        require(record(archive.read_bytes()) == {"bytes": info["bytes"], "sha256": info["sha256"]}, "ZIP hash mismatch")
        with zipfile.ZipFile(archive) as z:
            require(z.testzip() is None and len(z.infolist()) == 9 and set(z.namelist()) == payload, "ZIP CRC/inventory failure")
            require(sum(i.file_size for i in z.infolist()) == info["uncompressed_bytes"], "ZIP uncompressed size mismatch")
            for name in z.namelist():
                require(record(z.read(name)) == manifest["archive_files"][name], f"ZIP entry mismatch: {name}")
            require(json.loads(z.read("provenance/SHA256.json")) == source, "Supplied manifest mismatch")
    texts = {}
    for name, data in current.items():
        if Path(name).suffix in (".md", ".json", ".csv", ".py") or name in (".gitattributes", ".gitignore"):
            texts[name] = data.decode("utf-8", errors="strict")
            require("\x00" not in texts[name] and "\ufffd" not in texts[name], f"Invalid UTF-8 text: {name}")
    for book in BOOKS:
        name = f"narrative/{book}/ARCS.md"
        require(current[name] == base[name], f"Title registry changed: {book}")
        require(re.findall(r"^## (\d{2}) ", texts[name], re.M) == ["01", "02", "03", "04", "05"], f"Arc heading count: {book}")
    registry = dict(re.findall(r"^## (\d{2}) (.+)$", texts["narrative/ORANGE/ARCS.md"], re.M))
    accepted = []
    for number in range(1, 6):
        name = f"narrative/ORANGE/ARC_{number:02d}_SUMMARY.md"
        content = texts[name]
        header = re.match(r"# Orange — Arc (\d{2}): (.+)", content)
        require(header is not None and header[1] == f"{number:02d}" and header[2] == registry[header[1]], f"Arc title mismatch: {name}")
        require("**Status:** ACCEPTED — Pass 1 narrative skeleton (not chapter plan)" in content, f"Acceptance scope changed: {name}")
        beats = re.findall(r"^### (\d+)\. ", content, re.M)
        require(beats == ["1", "2", "3", "4", "5"], f"Beat order/count mismatch: {name}")
        for phrase in ("## Arc outcome", "## Transition", "## Boundaries", "exact dates, named local officials, scene order and dialogue remain OPEN", "AERA Transduction/velis rules govern all Weaves", "bounded and monitored, not autonomous or universal", "separate from Genesis storms, Domai, Eldris and municipal stabilization sigils", "Vaelith are autonomous individuals; Orange has globally non-ordinary geometry"):
            require(phrase in content, f"Missing boundary/structure in {name}")
        require(not re.search(r"\b\d{4}-\d{2}-\d{2}\b", content), f"Unexpected in-world date: {name}")
        accepted.append({"path": name, "number": header[1], "title": header[2], "main_beats": len(beats)})
    require(accepted == manifest["arcs"], "Accepted arc metadata mismatch")
    live = texts["narrative/ORANGE/LIVE_MODEL.md"]
    require(dict(re.findall(r"^\| (0\d) \| (.+?) \|", live, re.M)) == registry, "Orange live-model title table mismatch")
    require("Orange Arc 01: The Living Threshold" in texts["narrative/RED/ARC_05_SUMMARY.md"], "Red handoff mismatch")
    require("Several weeks after Red" in texts["narrative/ORANGE/ARC_01_SUMMARY.md"], "Relative interval missing")
    require("Vaelith may visit Orange and White, not other chromatic realms" in texts["narrative/ORANGE/ARC_02_SUMMARY.md"], "Realm access changed")
    require("Researchers terminate the test" in texts["narrative/ORANGE/ARC_03_SUMMARY.md"], "Failed-trial boundary missing")
    require("Full conversion is deferred pending certification and staffing" in texts["narrative/ORANGE/ARC_04_SUMMARY.md"], "Deployment scope changed")
    require("Yellow / The Shifting Landscape" in texts["narrative/ORANGE/ARC_05_SUMMARY.md"] and "## 01 The Shifting Landscape" in texts["narrative/YELLOW/ARCS.md"], "Yellow handoff mismatch")
    require("**Seren:** May correspond in Arc 05; precise messages and dates OPEN" in live, "Seren qualification changed")
    for version in ("", "_V2"):
        clock_name = f"world_clock/REALM_CLOCKS{version}.csv"
        event_name = f"world_clock/EVENTS{version}.csv"
        require(current[clock_name] == base[clock_name] and current[event_name] == base[event_name], "Chronology source changed")
        clocks = list(csv.DictReader(io.StringIO(texts[clock_name])))
        require(len(clocks) == 7 and clocks[0]["realm"] == "White" and clocks[0]["white_to_local_factor"] == "1", "Clock reference changed")
        require(all(not row["white_to_local_factor"] and row["status"] == "OPEN" for row in clocks[1:]), "Realm ratio invented")
        events = list(csv.DictReader(io.StringIO(texts[event_name])))
        require([(r["event_id"], r["book"], r["arc"]) for r in events] == [("E0001", "RED", "01"), ("E0002", "RED", "01"), ("E0003", "WHITE", "05")], "Event anchors changed")
        require(all(not r["white_date"] for r in events), "Event date invented")
    links = 0
    for name, content in texts.items():
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
    for name, content in texts.items():
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
    print(json.dumps({"result": "PASS", "base_commit": BASE, "project_files": len(actual), "snapshot_hashes": len(manifest["files"]), "unchanged_base_files": len(base)-len(changed), "append_only_base_files": len(changed), "added_files": len(actual-names), "archive_checked": archive.exists(), "source_manifest_entries": len(supplied), "imported_narrative_files": len(imported), "utf8_files": len(texts), "accepted_arcs": accepted, "accepted_main_beats": sum(a["main_beats"] for a in accepted), "unchanged_red_files": len(preserved_red), "unchanged_registry_headings": 35, "unchanged_clock_csvs": 4, "local_links": links, "git_index_checked": args.git_index, "commit_checked": args.commit, "limitations": ["Historical fixed-inventory verifiers require their original checkouts.", "ZIP availability is reported; recorded hashes still verify the imported files.", "Narrative detail and Seren correspondence remain qualified in the audit."]}, indent=2))


if __name__ == "__main__":
    main()
