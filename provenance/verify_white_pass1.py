"""Verify the fixed White Pass 1 snapshot and preserved earlier book records; Python 3.10+."""

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
BASE = "2e2d5ab3eca669e3342e86d42c3d8825c174301b"
MANIFEST = "provenance/WHITE_PASS1_SNAPSHOT_SHA256.json"
PRIOR = "provenance/VIOLET_PASS1_SNAPSHOT_SHA256.json"
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
    require(len(names) == 116 and names <= actual, "Base file missing")
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
    require(actual - names == set(manifest["added_paths"]) and len(actual) == 126, "Unexpected addition")
    preserved_red = {name for name in names if name.startswith("narrative/RED/")}
    preserved_orange = {name for name in names if name.startswith("narrative/ORANGE/")}
    preserved_yellow = {name for name in names if name.startswith("narrative/YELLOW/")}
    preserved_green = {name for name in names if name.startswith("narrative/GREEN/")}
    preserved_blue = {name for name in names if name.startswith("narrative/BLUE/")}
    preserved_violet = {name for name in names if name.startswith("narrative/VIOLET/")}
    require(len(preserved_red) == len(preserved_orange) == len(preserved_yellow) == len(preserved_green) == len(preserved_blue) == len(preserved_violet) == 8, "Previous narrative inventory changed")
    require(all(current[n] == base[n] for n in preserved_red | preserved_orange | preserved_yellow | preserved_green | preserved_blue | preserved_violet), "Earlier book records changed")
    require(all(current[n] == base[n] for n in names if n.startswith("world_clock/") and n != "world_clock/README.md"), "World Clock records changed")
    imported = {"narrative/WHITE/LIVE_MODEL.md"} | {f"narrative/WHITE/ARC_{i:02d}_SUMMARY.md" for i in range(1, 6)}
    wrappers = {"CODEX_UPDATE_PROMPT.md", "README.md", "provenance/SHA256.json"}
    payload = imported | wrappers
    require(set(manifest["archive_files"]) == payload and set(manifest["imported_paths"]) == imported, "Archive/import inventory mismatch")
    source = manifest["source_manifest"]
    require(isinstance(source, dict) and all(isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) for v in source.values()), "Unexpected source hash format")
    supplied = source
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
    registry = dict(re.findall(r"^## (\d{2}) (.+)$", texts["narrative/WHITE/ARCS.md"], re.M))
    accepted = []
    for number in range(1, 6):
        name = f"narrative/WHITE/ARC_{number:02d}_SUMMARY.md"
        content = texts[name]
        header = re.match(r"# WHITE — Arc (\d{2}): (.+)", content)
        require(header is not None and header[1] == f"{number:02d}" and header[2] == registry[header[1]], f"Arc title mismatch: {name}")
        require("**Pass:** 1 accepted narrative skeleton" in content, f"Acceptance scope changed: {name}")
        count = 6 if number >= 4 else 5
        beats = re.findall(r"^### (\d+)\. ", content, re.M)
        require(beats == [str(i) for i in range(1, count+1)], f"Beat order/count mismatch: {name}")
        for phrase in ("## Accepted major plot points", "## Arc outcome / transition", "## Scope and continuity", "Plot-level summary only", "environmental evolution interacting with accumulated engineering constraints", "Municipal Genesis-field stabilization remains independent of the ancient weaving network", "Genesis storms, Domai and Eldris relate to Starscape singularity and Genesis-field conditions, not network deterioration", "six chromatic collaborators can meet in White, not in each other’s chromatic realms", "Sixfold means complementary expertise, not a new magic system", "AERA Transduction"):
            require(phrase in content, f"Missing structure or scope in {name}: {phrase}")
        require(not re.search(r"\b\d{4}-\d{2}-\d{2}\b", content), f"Unexpected in-world date: {name}")
        accepted.append({"path": name, "number": header[1], "title": header[2], "main_beats": len(beats)})
    require(accepted == manifest["arcs"], "Accepted arc metadata mismatch")
    live = texts["narrative/WHITE/LIVE_MODEL.md"]
    entries = re.findall(r"^(0\d)\. \*\*(.+?)\*\* — (.+)$", live, re.M)
    require({number: title for number, title, outcome in entries} == registry and len(entries) == 5, "White live-model titles mismatch")
    for number, title, outcome in entries:
        content = texts[f"narrative/WHITE/ARC_{number}_SUMMARY.md"]
        transition = re.search(r"## Arc outcome / transition\n(.+)", content)
        require(transition is not None and transition[1] == outcome, f"Book/summary outcome mismatch: {number}")
    for phrase in ("All five White arc skeletons ACCEPTED", "not a complete manuscript", "not a supreme authority or omnipotent engineer", "independently of her familial relationship", "not six mandatory power components", "not completely or permanently fixed", "Municipal stabilization remains independent", "dialogue remain OPEN"):
        require(phrase in live, f"Missing White book safeguard: {phrase}")
    first = texts["narrative/WHITE/ARC_01_SUMMARY.md"]
    for phrase in ("Stormwall → Elarith Republic", "President Celene Arveth", "Minister Oren Valcrest", "Elarith Research Accord", "explicitly reviewed tests", "governments retain sovereignty"):
        require(phrase in first, f"White opening scope changed: {phrase}")
    second = texts["narrative/WHITE/ARC_02_SUMMARY.md"]
    require("reunion" in second.lower(), "Stormwall/Elarith reunion link missing")
    collaborators = ["Tharos", "Saelith", "Orun", "Iri", "Vaelor", "Aelira"]
    require(all(name in second and name in live for name in collaborators), "Six collaborators missing")
    third = texts["narrative/WHITE/ARC_03_SUMMARY.md"]
    require("withdraws" in third and "unproven" in third, "Shared redesign scope changed")
    fourth = texts["narrative/WHITE/ARC_04_SUMMARY.md"]
    for phrase in ("overlap is mutually admissible and globally compatible", "authorized noncritical subsystem test", "only bounded feasibility", "regional consent, monitoring and suspension", "signs technical certification", "remaining stages are not presumed safe"):
        require(phrase in fourth, f"Transition boundary changed: {phrase}")
    final_arc = texts["narrative/WHITE/ARC_05_SUMMARY.md"]
    for phrase in ("unresolved constraints elsewhere", "no total permanent repair", "younger brother Tavin", "mountain remains physically present", "rather than erased or declared false", "Proposed closing line:"):
        require(phrase in final_arc, f"Ending scope changed: {phrase}")
    require("all six meet in Stormwall in White" in texts["narrative/VIOLET/ARC_05_SUMMARY.md"], "Violet meeting source changed")
    require("Conservator's daughter" in texts["narrative/BLUE/LIVE_MODEL.md"] and "OPEN — Seren family-status ambiguity continues" in texts["canon/DECISIONS.md"], "Earlier source-status ambiguity lost")
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
    print(json.dumps({"result": "PASS", "base_commit": BASE, "project_files": len(actual), "snapshot_hashes": len(manifest["files"]), "unchanged_base_files": len(base)-len(changed), "append_only_base_files": len(changed), "added_files": len(actual-names), "archive_checked": archive.exists(), "source_manifest_entries": len(supplied), "imported_narrative_files": len(imported), "utf8_files": len(texts), "accepted_arcs": accepted, "accepted_main_beats": sum(a["main_beats"] for a in accepted), "unchanged_red_files": len(preserved_red), "unchanged_orange_files": len(preserved_orange), "unchanged_yellow_files": len(preserved_yellow), "unchanged_green_files": len(preserved_green), "unchanged_blue_files": len(preserved_blue), "unchanged_violet_files": len(preserved_violet), "six_collaborators": list(collaborators), "sixfold_location": "Elarith reunion, White Realm", "source_markdown_hardbreaks": len(hardbreaks), "matching_book_model_titles": 5, "matching_arc_outcomes": 5, "unresolved_canon_status": ["Seren parentage acceptance scope remains open; White does not identify the other party to the familial relationship."], "unchanged_registry_headings": 35, "unchanged_clock_csvs": 4, "local_links": links, "git_index_checked": args.git_index, "commit_checked": args.commit, "limitations": ["Historical fixed-inventory verifiers require their original checkouts.", "ZIP availability is reported; recorded hashes still verify the imported files.", "Exact procedures, chronology, technical proof and prior Seren questions remain open; the seven-book audit is separate."]}, indent=2))


if __name__ == "__main__":
    main()
