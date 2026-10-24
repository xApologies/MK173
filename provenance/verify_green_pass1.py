"""Verify the fixed Green Pass 1 snapshot and preserved Red/Orange/Yellow records; Python 3.10+."""

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
BASE = "4351150d9e3323294fa277f7cb707645a750d55f"
MANIFEST = "provenance/GREEN_PASS1_SNAPSHOT_SHA256.json"
PRIOR = "provenance/YELLOW_PASS1_SNAPSHOT_SHA256.json"
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
    require(len(names) == 86 and names <= actual, "Base file missing")
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
    require(actual - names == set(manifest["added_paths"]) and len(actual) == 96, "Unexpected addition")
    preserved_red = {name for name in names if name.startswith("narrative/RED/")}
    preserved_orange = {name for name in names if name.startswith("narrative/ORANGE/")}
    preserved_yellow = {name for name in names if name.startswith("narrative/YELLOW/")}
    require(len(preserved_red) == len(preserved_orange) == len(preserved_yellow) == 8, "Previous narrative inventory changed")
    require(all(current[n] == base[n] for n in preserved_red | preserved_orange | preserved_yellow), "Red/Orange/Yellow records changed")
    require(all(current[n] == base[n] for n in names if n.startswith("world_clock/") and n != "world_clock/README.md"), "World Clock records changed")
    imported = {"narrative/GREEN/LIVE_MODEL.md"} | {f"narrative/GREEN/ARC_{i:02d}_SUMMARY.md" for i in range(1, 6)}
    wrappers = {"CODEX_UPDATE_PROMPT.md", "README.md", "provenance/SHA256.json"}
    payload = imported | wrappers
    require(set(manifest["archive_files"]) == payload and set(manifest["imported_paths"]) == imported, "Archive/import inventory mismatch")
    source = manifest["source_manifest"]
    require(source["project"] == "MK173" and source["book"] == "GREEN" and source["version"] == "0.1" and source["algorithm"] == "SHA-256", "Unexpected source identity")
    supplied = source["files"]
    require(set(supplied) == payload - {"provenance/SHA256.json", "CODEX_UPDATE_PROMPT.md"}, "Source manifest coverage mismatch")
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
    registry = dict(re.findall(r"^## (\d{2}) (.+)$", texts["narrative/GREEN/ARCS.md"], re.M))
    accepted = []
    for number in range(1, 6):
        name = f"narrative/GREEN/ARC_{number:02d}_SUMMARY.md"
        content = texts[name]
        header = re.match(r"# GREEN — Arc (\d{2}): (.+)", content)
        require(header is not None and header[1] == f"{number:02d}" and header[2] == registry[header[1]], f"Arc title mismatch: {name}")
        require("**Status:** ACCEPTED — Pass 1 narrative skeleton; not a chapter outline or manuscript." in content, f"Acceptance scope changed: {name}")
        beats = re.findall(r"^### (\d+)\. ", content, re.M)
        require(beats == ["1", "2", "3", "4", "5"], f"Beat order/count mismatch: {name}")
        for phrase in ("## Principal plot points", "## Aren’s development", "## Causal transition", "## Limits of this pass", "No chapter count, precise dates, dialogue, field equations, quantitative performance, or unapproved names are established here", "without silently changing accepted causality"):
            require(phrase in content, f"Missing structure or scope in {name}")
        require(not re.search(r"\b\d{4}-\d{2}-\d{2}\b", content), f"Unexpected in-world date: {name}")
        accepted.append({"path": name, "number": header[1], "title": header[2], "main_beats": len(beats)})
    require(accepted == manifest["arcs"], "Accepted arc metadata mismatch")
    live = texts["narrative/GREEN/LIVE_MODEL.md"]
    require(dict(re.findall(r"^\| (0\d) \| (.+?) \|", live, re.M)) == registry, "Green live-model titles mismatch")
    for phrase in ("**Status:** ACCEPTED Pass 1", "Serenwood is a **White-realm** commonwealth", "native Sprite access is Green and White", "a **mathematical representation**", "specialization of AERA Transduction", "environmental evolution interacting with accumulated engineering constraints", "Sprite case studies are not secretly network infrastructure", "Municipal Genesis stabilization systems remain independent", "Starscape singularity configuration/local Genesis-field conditions", "**not** ancient-network failure or configuration trapping", "No arc confers moral decision-making authority on the atlas", "Remains in Green to observe"):
        require(phrase in live, f"Missing Green book safeguard: {phrase}")
    require("Green Arc 01 — The Forest of Possibilities" in texts["narrative/YELLOW/ARC_05_SUMMARY.md"], "Yellow handoff mismatch")
    first = texts["narrative/GREEN/ARC_01_SUMMARY.md"]
    for phrase in ("Following the Dawnshore work", "Pellian Vey authorizes participation", "Travel uses established terrestrial Corridors", "political culture is not caused by Green energy", "without selecting the final preserve design"):
        require(phrase in first, f"Green opening scope changed: {phrase}")
    require("NOT a hive mind or shared consciousness" in texts["narrative/GREEN/ARC_02_SUMMARY.md"], "Collective autonomy changed")
    third = texts["narrative/GREEN/ARC_03_SUMMARY.md"]
    require("every currently known route" in third and "Reachability claims remain bounded by known constraints and transitions" in third, "Reachability scope changed")
    fourth = texts["narrative/GREEN/ARC_04_SUMMARY.md"]
    require("Physical reactivation remains prohibited" in fourth and "permits noninvasive investigation while maintaining the operational ban" in fourth, "Research authorization changed")
    require("Sprite experiment is not itself a network component" in fourth, "Network analogy changed")
    final_arc = texts["narrative/GREEN/ARC_05_SUMMARY.md"]
    for phrase in ("decision support, not an automatic moral chooser", "weigh values differently", "implementation is phased, monitored, and subject to reassessment", "remains outside its present predictive capability", "Iri stays to monitor local implementation"):
        require(phrase in final_arc, f"Final arc scope changed: {phrase}")
    require("Arc 01 The Ancient Passage" in final_arc and "## 01 The Ancient Passage" in texts["narrative/BLUE/ARCS.md"], "Blue handoff mismatch")
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
    hardbreaks = []
    for name in sorted(imported):
        for lineno, line in enumerate(texts[name].splitlines(), 1):
            if line.rstrip(" \t") != line:
                require(line.endswith("  ") and not line.endswith("   ") and line.strip(), f"Unexpected source whitespace: {name}:{lineno}")
                hardbreaks.append({"path": name, "line": lineno})
    require(len(hardbreaks) == 0 and hardbreaks == manifest["source_markdown_hardbreaks"], "Source hard-break inventory changed")
    for name in (actual - names) | changed:
        if name not in texts:
            continue
        introduced = current[name][len(base[name]):].decode("utf-8") if name in changed else texts[name]
        if name not in imported:
            require(all(line.rstrip(" \t") == line for line in introduced.splitlines()), f"Introduced trailing whitespace: {name}")
        require(not re.search(r"^(?:<<<<<<< |=======$|>>>>>>> )", introduced, re.M), f"Conflict marker: {name}")
        require(not re.search(r"\n[ \t\r]*\n\Z", introduced), f"Blank line at EOF: {name}")
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
    print(json.dumps({"result": "PASS", "base_commit": BASE, "project_files": len(actual), "snapshot_hashes": len(manifest["files"]), "unchanged_base_files": len(base)-len(changed), "append_only_base_files": len(changed), "added_files": len(actual-names), "archive_checked": archive.exists(), "source_manifest_entries": len(supplied), "imported_narrative_files": len(imported), "utf8_files": len(texts), "accepted_arcs": accepted, "accepted_main_beats": sum(a["main_beats"] for a in accepted), "unchanged_red_files": len(preserved_red), "unchanged_orange_files": len(preserved_orange), "unchanged_yellow_files": len(preserved_yellow), "source_markdown_hardbreaks": len(hardbreaks), "matching_book_model_titles": 5, "unchanged_registry_headings": 35, "unchanged_clock_csvs": 4, "local_links": links, "git_index_checked": args.git_index, "commit_checked": args.commit, "limitations": ["Historical fixed-inventory verifiers require their original checkouts.", "ZIP availability is reported; recorded hashes still verify the imported files.", "Reachability, implementation outcomes, long-duration persistence and earlier open details remain qualified in the audit."]}, indent=2))


if __name__ == "__main__":
    main()
