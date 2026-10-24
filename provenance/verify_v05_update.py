"""Verify the fixed MK173 v0.5 update and its preserved v0.4 base (Python 3.10+, Pillow)."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
from urllib.parse import unquote, urlsplit
import zipfile

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
BASE = "9f557a3f4cebd45769dbc58cd079bf6e29656eac"
MANIFEST = "provenance/V05_UPDATE_SHA256.json"
BOOKS = ("RED", "ORANGE", "YELLOW", "GREEN", "BLUE", "VIOLET", "WHITE")
MODIFIED = {"canon/DECISIONS.md", "canon/AERA_INHERITANCE.md", "LIVE_MODEL.md", "README.md", "images/INDEX.md", "provenance/CHANGELOG.md"}
APPENDED = MODIFIED - {"canon/DECISIONS.md", "canon/AERA_INHERITANCE.md"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--git-index", action="store_true")
    group.add_argument("--commit", help="Additionally compare the selected commit with this snapshot.")
    args = parser.parse_args()
    manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    require(manifest["base_commit"] == BASE, "Unexpected base commit")
    actual = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in (".git", "_inbox") or "__pycache__" in relative.parts:
            continue
        require(not path.is_symlink(), f"Unexpected symlink: {relative}")
        require(".git" not in relative.parts, f"Nested Git metadata: {relative}")
        if path.is_file() and path.suffix != ".pyc":
            actual.add(relative.as_posix())
    require(actual == set(manifest["files"]) | {MANIFEST}, "Unexpected project inventory")
    require(len(actual) == 40, "Expected 40 project files")
    current = {name: (ROOT / name).read_bytes() for name in actual}
    for name, record in manifest["files"].items():
        require(len(current[name]) == record["bytes"] and sha(current[name]) == record["sha256"], f"Snapshot mismatch: {name}")
    require(Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve() == ROOT, "Wrong Git root")
    base_names = set(git("ls-tree", "-r", "--name-only", "-z", BASE).decode().rstrip("\0").split("\0"))
    base = {name: git("show", f"{BASE}:{name}") for name in base_names}
    require(len(base) == 27 and base_names <= actual, "Base file lost")
    require(set(manifest["base_files"]) == base_names, "Base manifest inventory mismatch")
    for name, data in base.items():
        require(sha(data) == manifest["base_files"][name]["sha256"], f"Base hash mismatch: {name}")
    old_manifest = json.loads(base["provenance/IMPORT_SHA256.json"])
    for name, digest in old_manifest["files"].items():
        require(sha(base[name]) == digest, f"Historical import manifest mismatch: {name}")
    changed = {name for name in base if current[name] != base[name]}
    require(changed == MODIFIED == set(manifest["modified_paths"]), "Unexpected modified paths")
    require(actual - base_names == set(manifest["added_paths"]), "Unexpected added paths")
    for name in APPENDED:
        require(current[name].startswith(base[name]), f"Historical prefix rewritten: {name}")
    for name in MODIFIED:
        old_urls = set(re.findall(rb"https?://[^\s)]+", base[name]))
        require(old_urls <= set(re.findall(rb"https?://[^\s)]+", current[name])), f"Source URL removed: {name}")
    archive = manifest["archive"]
    archive_path = ROOT / "_inbox" / archive["name"]
    archive_checked = archive_path.exists()
    if archive_checked:
        require(archive_path.stat().st_size == archive["bytes"] and sha(archive_path.read_bytes()) == archive["sha256"], "ZIP hash mismatch")
        with zipfile.ZipFile(archive_path) as z:
            require(z.testzip() is None, "ZIP CRC failure")
            entries = z.infolist()
            require(len(entries) == 12 and set(z.namelist()) == set(manifest["archive_files"]), "ZIP inventory mismatch")
            require(len({e.filename.casefold() for e in entries}) == 12, "ZIP case collision")
            for entry in entries:
                name = entry.filename
                parts = name.split("/")
                require(not PurePosixPath(name).is_absolute() and "\\" not in name and ":" not in name, f"Unsafe ZIP path: {name}")
                require(all(p not in ("", ".", "..", ".git", "_inbox") and not p.endswith((" ", ".")) for p in parts), f"Unsafe ZIP component: {name}")
                require(not any(re.match(r"^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)", p, re.I) for p in parts), f"Reserved ZIP name: {name}")
                require(stat.S_IFMT(entry.external_attr >> 16) in (0, stat.S_IFREG), f"Nonregular ZIP entry: {name}")
                data = z.read(entry)
                record = manifest["archive_files"][name]
                require(len(data) == record["bytes"] and sha(data) == record["sha256"], f"ZIP entry mismatch: {name}")
            supplied = json.loads(z.read("provenance/DELTA_SHA256.json"))
            require(set(supplied) == set(z.namelist()) - {"provenance/DELTA_SHA256.json"}, "Supplied manifest coverage mismatch")
            for name, record in supplied.items():
                require(record == manifest["archive_files"][name], f"Supplied source hash mismatch: {name}")
    require(len(manifest["imported_paths"]) == 10, "Expected ten imported delta paths")
    for name in manifest["imported_paths"]:
        require(sha(current[name]) == manifest["archive_files"][name]["sha256"], f"Imported source changed: {name}")
    text = {}
    for name, data in current.items():
        if Path(name).suffix in (".md", ".json", ".csv", ".py") or name in (".gitattributes", ".gitignore"):
            text[name] = data.decode("utf-8", errors="strict")
            require("\x00" not in text[name] and "\ufffd" not in text[name], f"Invalid text: {name}")
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
    for book in BOOKS:
        name = f"narrative/{book}/ARCS.md"
        require(current[name] == base[name], f"Arc source changed: {book}")
        require(re.findall(r"^## (\d{2}) ", text[name], re.M) == ["01", "02", "03", "04", "05"], f"Arc count/order: {book}")
    for number, name in (("08", "ECONOMY_AND_DAILY_LIFE"), ("09", "ENVIRONMENTAL_GEOGRAPHY"), ("10", "NARRATIVE_CONSTITUTION")):
        content = text[f"canon/{number}_{name}.md"]
        require(f"Development {number}:" in content and all(f"## {status}" in content for status in ("ACCEPTED", "WORKING", "OPEN")), f"Stage/status record missing: {number}")
    decisions = text["canon/DECISIONS.md"]
    require("transcription error for vaen" in decisions and "No separate BAEN resource exists." in decisions, "Accepted correction missing")
    require(not re.search(r"\bBAEN\b|B-A-E-N", decisions.split("## OPEN", 1)[1], re.I), "Terminology ambiguity remains OPEN")
    inheritance = text["canon/AERA_INHERITANCE.md"]
    require("BAEN transcription error corrected to vaen" in inheritance and "BAEN unresolved" not in inheritance, "Inheritance correction missing")
    require(all(term in inheritance for term in ("Vaelith", "velis", "ru’ne", "maege", "maegi", "vaen")), "Protected spelling missing")
    for filename, width in (("EVENTS_V2.csv", 13), ("REALM_CLOCKS_V2.csv", 7)):
        rows = list(csv.reader(io.StringIO(text[f"world_clock/{filename}"])))
        require(all(len(row) == width for row in rows), f"Inconsistent CSV row width: {filename}")
    for suffix in ("", "_V2"):
        clocks = list(csv.DictReader(io.StringIO(text[f"world_clock/REALM_CLOCKS{suffix}.csv"])))
        require([r["realm"] for r in clocks] == ["White"] + [b.title() for b in BOOKS[:-1]], "Realm inventory changed")
        require(clocks[0]["white_to_local_factor"] == "1" and clocks[0]["status"] == "REFERENCE", "White reference changed")
        require(all(not r["white_to_local_factor"] and r["status"] == "OPEN" for r in clocks[1:]), "Chromatic factor invented")
    event_reader = csv.DictReader(io.StringIO(text["world_clock/EVENTS_V2.csv"]))
    require(event_reader.fieldnames == ["event_id", "book", "arc", "event", "relative_order", "predecessor_id", "white_date", "realm", "realm_local_time", "location", "source", "status", "notes"], "Event v2 schema changed")
    events = list(event_reader)
    original_events = list(csv.DictReader(io.StringIO(text["world_clock/EVENTS.csv"])))
    require(len(events) == 3 and {r["event_id"] for r in events} == {"E0001", "E0002", "E0003"}, "Event inventory changed")
    for row, original in zip(events, original_events):
        require(all(row[k] == v for k, v in original.items()), "Original event content changed")
        require(row["book"] in BOOKS and row["arc"] in {"01", "02", "03", "04", "05"}, "Invalid event arc")
        require(row["realm"] == "White" and row["source"] and row["status"] == "WORKING", "Event provenance/status missing")
        require(not row["white_date"] and not row["realm_local_time"], "Event date invented")
        require(not row["predecessor_id"] or row["predecessor_id"] in {r["event_id"] for r in events}, "Unresolved predecessor")
    require(events[1]["predecessor_id"] == "E0001" and events[2]["predecessor_id"] == "", "Unexpected chronology dependencies")
    realm_reader = csv.DictReader(io.StringIO(text["world_clock/REALM_CLOCKS_V2.csv"]))
    require(realm_reader.fieldnames == ["realm", "white_to_local_factor", "epoch", "offset", "precision", "source", "status"], "Realm v2 schema changed")
    require(all(not r["epoch"] and not r["offset"] and r["source"] for r in realm_reader), "Invented epoch/offset or absent source")
    image_names = sorted(n for n in actual if Path(n).suffix.lower() in (".png", ".jpeg", ".jpg"))
    require(len(image_names) == 4, "Expected three original images plus one derivative")
    for name in image_names:
        with Image.open(ROOT / name) as im:
            im.verify()
        with Image.open(ROOT / name) as im:
            im.load()
    with Image.open(ROOT / "images/maps/political_v01.png") as old, Image.open(ROOT / "images/maps/political_v02_corrected.png") as new:
        require(old.size == new.size == (1774, 887), "Political map dimensions changed")
        diff = ImageChops.difference(old.convert("RGB"), new.convert("RGB"))
        require(list(diff.getbbox()) == [11, 120, 186, 162], "Map changes extend beyond supplied annotation")
        r, g, b = diff.split()
        changed_pixels = old.width * old.height - ImageChops.lighter(ImageChops.lighter(r, g), b).histogram()[0]
        require(changed_pixels == 7345, "Unexpected changed-pixel count")
    patterns = [r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{30,}", r"AKIA[0-9A-Z]{16}", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"]
    for name, content in text.items():
        require(not any(re.search(p, content) for p in patterns), f"Possible credential in {name}")
    if args.git_index or args.commit:
        if args.git_index:
            names = git("ls-files", "-z")
            prefix = ":"
        else:
            commit = git("rev-parse", "--verify", f"{args.commit}^{{commit}}").decode().strip()
            git("merge-base", "--is-ancestor", BASE, commit)
            names = git("ls-tree", "-r", "--name-only", "-z", commit)
            prefix = commit + ":"
        require(set(names.decode().rstrip("\0").split("\0")) == actual, "Git inventory differs")
        for name in sorted(actual):
            require(git("show", prefix + name) == current[name], f"Git bytes differ: {name}")
    print(json.dumps({"result": "PASS", "base_commit": BASE, "project_files": len(actual), "snapshot_hashes": len(manifest["files"]), "unchanged_base_files": len(base) - len(changed), "modified_base_files": len(changed), "append_only_files": len(APPENDED), "added_files": len(actual - base_names), "source_archive_checked": archive_checked, "imported_source_files": 10, "utf8_files": len(text), "images": len(image_names), "changed_map_pixels": changed_pixels, "working_arcs": 35, "realm_rows_per_csv": 7, "v2_events": len(events), "local_markdown_links": links, "git_index_checked": args.git_index, "commit_checked": args.commit, "qualifications": ["Old validator is retained for the v0.4 checkout only.", "A missing local delta ZIP is reported; copied files still match recorded source hashes.", "Map measurements, provenance gaps, dates, ratios, rates and E0003 dependencies remain qualified in the audit."]}, indent=2))


if __name__ == "__main__":
    main()
