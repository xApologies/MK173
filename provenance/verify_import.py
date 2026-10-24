"""Verify the fixed MK173 v0.4 import snapshot; requires Python 3.10+ and Pillow."""

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

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "provenance/IMPORT_SHA256.json"
BOOKS = ("RED", "ORANGE", "YELLOW", "GREEN", "BLUE", "VIOLET", "WHITE")
APPENDED = {"LIVE_MODEL.md", "images/INDEX.md", "world_clock/README.md", "provenance/CHANGELOG.md"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--git-index", action="store_true")
    parser.add_argument("--commit", help="Also verify file paths and bytes in this commit.")
    args = parser.parse_args()
    snapshot = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    expected = snapshot["files"]
    actual = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in (".git", "_inbox") or "__pycache__" in relative.parts:
            continue
        require(not path.is_symlink(), f"Unexpected symlink: {relative}")
        if path.is_file() and path.suffix != ".pyc":
            actual.add(relative.as_posix())
    require(actual == set(expected) | {MANIFEST}, "Import file inventory changed")
    for name, sha in expected.items():
        require(digest((ROOT / name).read_bytes()) == sha, f"Snapshot hash mismatch: {name}")
    source = snapshot["archive_files"]
    original_manifest = json.loads((ROOT / "provenance/SHA256.json").read_text(encoding="utf-8"))
    require(set(original_manifest) == set(source) - {"provenance/SHA256.json"}, "Source manifest inventory mismatch")
    for name, sha in original_manifest.items():
        require(source[name]["sha256"] == sha, f"Source manifest hash mismatch: {name}")
    for name, info in source.items():
        data = (ROOT / name).read_bytes()
        if name in APPENDED:
            data = data[:info["bytes"]]
        if name != "README.md":
            require(digest(data) == info["sha256"], f"Source bytes changed: {name}")

    archive_path = ROOT / "_inbox" / snapshot["archive"]["name"]
    archive_checked = archive_path.exists()
    if archive_checked:
        require(digest(archive_path.read_bytes()) == snapshot["archive"]["sha256"], "Archive SHA256 mismatch")
        with zipfile.ZipFile(archive_path) as archive:
            require(archive.testzip() is None, "ZIP CRC failure")
            names = archive.namelist()
            require(set(names) == set(source) and len(names) == len(source), "Archive inventory mismatch")
            require(len({name.casefold() for name in names}) == len(names), "Case collision")
            for entry in archive.infolist():
                name = entry.filename
                parts = name.split("/")
                require(not PurePosixPath(name).is_absolute() and "\\" not in name and ":" not in name, f"Unsafe ZIP path: {name}")
                require(all(p not in ("", ".", "..", ".git", "_inbox") and not p.endswith((" ", ".")) for p in parts), f"Unsafe ZIP component: {name}")
                require(stat.S_IFMT(entry.external_attr >> 16) in (0, stat.S_IFREG), f"Nonregular ZIP entry: {name}")
                data = archive.read(name)
                require(len(data) == source[name]["bytes"] and digest(data) == source[name]["sha256"], f"Archive entry mismatch: {name}")
    text_files = {}
    for name in actual:
        if Path(name).suffix in (".md", ".json", ".csv", ".py") or name in (".gitignore", ".gitattributes"):
            text = (ROOT / name).read_bytes().decode("utf-8", errors="strict")
            require("\x00" not in text and "\ufffd" not in text, f"Invalid text: {name}")
            text_files[name] = text
    images = []
    for name in sorted(actual):
        if Path(name).suffix.lower() in (".png", ".jpeg", ".jpg"):
            with Image.open(ROOT / name) as image:
                images.append({"path": name, "format": image.format, "size": list(image.size)})
                image.verify()
            with Image.open(ROOT / name) as image:
                image.load()
    require(images == snapshot["images"], "Image inventory or dimensions changed")
    require(len(images) == 3, "Expected exactly three images")
    for book in BOOKS:
        text = text_files[f"narrative/{book}/ARCS.md"]
        require(re.findall(r"^## (\d{2}) ", text, re.M) == ["01", "02", "03", "04", "05"], f"Arc headings: {book}")
        require("working arc names, not manuscript" in text and text.count("Detailed outline OPEN.") == 5, f"Arc status: {book}")
    clocks = list(csv.DictReader(io.StringIO(text_files["world_clock/REALM_CLOCKS.csv"])))
    require(clocks == [{"realm": "White", "white_to_local_factor": "1", "status": "REFERENCE"}] + [{"realm": b.title(), "white_to_local_factor": "", "status": "OPEN"} for b in BOOKS[:-1]], "Clock factors/status changed")
    events = list(csv.DictReader(io.StringIO(text_files["world_clock/EVENTS.csv"])))
    ids = {row["event_id"] for row in events}
    require(len(events) == len(ids) == 3, "Duplicate or changed event IDs")
    require(all(row["status"] == "WORKING" and not row["white_date"] for row in events), "Event dates/status changed")
    for row in events:
        require(row["book"] in BOOKS and row["arc"] in {"01", "02", "03", "04", "05"}, "Invalid event arc")
        require(all(ref in ids for ref in re.findall(r"E\d{4}", row["relative_order"])), "Missing event dependency")
    decisions = text_files["canon/DECISIONS.md"]
    require(all(heading in decisions for heading in ("## ACCEPTED", "## WORKING", "## OPEN")), "Decision status headings missing")
    require("B-A-E-N" in decisions and "Do not silently conflate." in decisions, "BAEN ambiguity lost")
    inheritance = text_files["canon/AERA_INHERITANCE.md"]
    require(all(term in inheritance for term in ("Vaelith", "velis", "ru’ne", "maege", "maegi")), "Protected spelling missing")
    require(all(f"| {i:02d} |" in text_files["provenance/IMPORT_AUDIT.md"] for i in range(1, 11)), "Stage coverage rows missing")
    links_checked = 0
    for name, text in text_files.items():
        if not name.endswith(".md"):
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            path = (ROOT / name).parent / unquote(parsed.path)
            require(path.resolve().is_relative_to(ROOT) and path.exists(), f"Broken local Markdown link: {name} -> {target}")
            links_checked += 1
    legacy = "images/maps/MK173_white_world_geography_concept_v01.png"
    require(legacy in text_files["LIVE_MODEL.md"] and "Historical filename resolution" in text_files["LIVE_MODEL.md"], "Historical alias record missing")
    require((ROOT / "images/maps/geography_v01.png").is_file(), "Historical alias target missing")
    secret_patterns = [r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{30,}", r"AKIA[0-9A-Z]{16}", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"]
    for name, text in text_files.items():
        require(not any(re.search(pattern, text) for pattern in secret_patterns), f"Possible credential in: {name}")
    if args.git_index or args.commit:
        require(git("rev-parse", "--show-toplevel").decode().strip().replace("\\", "/").casefold() == ROOT.as_posix().casefold(), "Wrong Git root")
        if args.git_index:
            tracked = set(git("ls-files", "-z").decode().rstrip("\0").split("\0"))
            prefix = ":"
        else:
            commit = git("rev-parse", "--verify", f"{args.commit}^{{commit}}").decode().strip()
            tracked = set(git("ls-tree", "-r", "--name-only", "-z", commit).decode().rstrip("\0").split("\0"))
            prefix = commit + ":"
        require(tracked == actual, "Git snapshot inventory differs from import")
        for name in sorted(actual):
            require(git("show", prefix + name) == (ROOT / name).read_bytes(), f"Git bytes differ: {name}")
    print(json.dumps({"result": "PASS", "project_files": len(actual), "snapshot_hashes": len(expected), "archive_files": len(source), "archive_checked": archive_checked, "source_manifest_entries": len(original_manifest), "utf8_files": len(text_files), "images": images, "working_arcs": 35, "local_markdown_links": links_checked, "historical_aliases": 1, "git_index_checked": args.git_index, "commit_checked": args.commit, "qualifications": ["Stages 08-10 have aggregate evidence only.", "Original image attribution and generation history are incomplete.", "Historical image filename is explicitly mapped to the delivered file.", "PASS verifies integrity and recorded safeguards; it does not fill provenance gaps."]}, indent=2))


if __name__ == "__main__":
    main()
