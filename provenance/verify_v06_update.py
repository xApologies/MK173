"""Verify the fixed MK173 v0.6 snapshot (Python 3.10+, Pillow, pypdf)."""

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

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BASE = "d921703d0f0724fce98ebea2d667899e000e2df3"
MANIFEST = "provenance/V06_SNAPSHOT_SHA256.json"
APPENDED = {"LIVE_MODEL.md", "README.md", "canon/DECISIONS.md", "canon/08_ECONOMY_AND_DAILY_LIFE.md", "world_clock/README.md", "provenance/CHANGELOG.md"}
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
    require(manifest["base_commit"] == BASE, "Unexpected base")
    actual = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in (".git", "_inbox") or "__pycache__" in relative.parts:
            continue
        require(not path.is_symlink() and ".git" not in relative.parts, f"Unexpected link/Git metadata: {relative}")
        if path.is_file() and path.suffix != ".pyc":
            actual.add(relative.as_posix())
    require(actual == set(manifest["files"]) | {MANIFEST}, "Snapshot inventory changed")
    require(len(actual) == 56, "Expected 56 files")
    current = {name: (ROOT / name).read_bytes() for name in actual}
    for name, info in manifest["files"].items():
        require(record(current[name]) == info, f"Snapshot mismatch: {name}")
    require(Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve() == ROOT, "Wrong Git root")
    base_names = set(git("ls-tree", "-r", "--name-only", "-z", BASE).decode().rstrip("\0").split("\0"))
    require(len(base_names) == 40 and base_names <= actual, "Base files lost")
    base = {name: git("show", f"{BASE}:{name}") for name in base_names}
    require(set(manifest["base_files"]) == base_names, "Base inventory mismatch")
    for name, data in base.items():
        require(record(data) == manifest["base_files"][name], f"Base hash mismatch: {name}")
    old_manifest = json.loads(base["provenance/V05_UPDATE_SHA256.json"])
    require(set(old_manifest["files"]) == base_names - {"provenance/V05_UPDATE_SHA256.json"}, "Old manifest coverage mismatch")
    for name, info in old_manifest["files"].items():
        require(record(base[name]) == info, f"Old snapshot mismatch: {name}")
    changed = {name for name in base if current[name] != base[name]}
    require(changed == APPENDED == set(manifest["modified_paths"]), "Unexpected base modifications")
    for name in APPENDED:
        require(current[name].startswith(base[name]), f"Historical prefix altered: {name}")
    require(actual - base_names == set(manifest["added_paths"]), "Unexpected additions")
    supplied = json.loads(current["provenance/V06_PAYLOAD_SHA256.json"])
    require(supplied["version"] == "0.6" and supplied["type"] == "incremental", "Wrong payload version")
    require(set(supplied["files"]) == set(manifest["archive_files"]) - {"provenance/V06_PAYLOAD_SHA256.json"}, "Payload manifest inventory mismatch")
    for name, info in supplied["files"].items():
        require(record(current[name]) == info, f"Payload hash mismatch: {name}")
    require(set(manifest["imported_paths"]) == set(manifest["archive_files"]), "Imported inventory mismatch")
    for name, info in manifest["archive_files"].items():
        require(record(current[name]) == info, f"Imported bytes changed: {name}")
    archive = ROOT / "_inbox" / manifest["archive"]["name"]
    if archive.exists():
        info = manifest["archive"]
        require(record(archive.read_bytes()) == {"bytes": info["bytes"], "sha256": info["sha256"]}, "ZIP hash mismatch")
        with zipfile.ZipFile(archive) as z:
            require(z.testzip() is None and len(z.infolist()) == 12, "ZIP CRC/count failure")
            require(set(z.namelist()) == set(manifest["archive_files"]), "ZIP inventory mismatch")
            for name in z.namelist():
                require(record(z.read(name)) == manifest["archive_files"][name], f"ZIP entry mismatch: {name}")
    text = {}
    for name, data in current.items():
        if Path(name).suffix in (".md", ".json", ".csv", ".py") or name in (".gitattributes", ".gitignore"):
            content = data.decode("utf-8", errors="strict")
            require("\x00" not in content and "\ufffd" not in content, f"Invalid text: {name}")
            text[name] = content
    links = 0
    for name, content in text.items():
        if not name.endswith(".md"):
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            path = ((ROOT / name).parent / unquote(parsed.path)).resolve()
            require(path.is_relative_to(ROOT) and path.exists(), f"Broken link: {name} -> {target}")
            links += 1
    require(not any(Path(n).suffix.lower() in (".zip", ".tar", ".gz", ".7z") for n in actual), "Archive committed into project")
    for book in BOOKS:
        name = f"narrative/{book}/ARCS.md"
        require(current[name] == base[name], f"Arc titles changed: {book}")
        require(re.findall(r"^## (\d{2}) ", text[name], re.M) == ["01", "02", "03", "04", "05"], f"Wrong arc headings: {book}")
    for version in ("", "_V2"):
        name = f"world_clock/REALM_CLOCKS{version}.csv"
        rows = list(csv.DictReader(io.StringIO(text[name])))
        require([r["realm"] for r in rows] == ["White"] + [b.title() for b in BOOKS[:-1]], "Realm rows changed")
        require(rows[0]["white_to_local_factor"] == "1" and rows[0]["status"] == "REFERENCE", "White reference changed")
        require(all(not r["white_to_local_factor"] and r["status"] == "OPEN" for r in rows[1:]), "Realm ratio invented")
        event_name = f"world_clock/EVENTS{version}.csv"
        events = list(csv.DictReader(io.StringIO(text[event_name])))
        require(len(events) == 3 and len({r["event_id"] for r in events}) == 3, "Event IDs changed")
        require(all(not r["white_date"] and r["status"] == "WORKING" for r in events), "Event date/status changed")
    post = text["canon/POST_V05_DECISIONS.md"]
    require(all(term in post for term in ("180 ahm = 1 eln", "White", "1080", "realm trade currency", "WORKING", "not a professional cardsmith", "vaen", "Vaelith", "velis", "ru’ne", "maege", "maegi")), "Accepted scope/terminology missing")
    for name in ("canon/DECISIONS.md", "canon/08_ECONOMY_AND_DAILY_LIFE.md"):
        addition = current[name][len(base[name]):].decode("utf-8")
        require("180 ahm = 1 eln" in addition and "supersed" in addition.lower(), f"Missing dated supersession: {name}")
    leadership = text["world_clock/L2_WORLD_CIVILIZATION/POLITICS/LEADERSHIP_WORKING.md"]
    require("WORKING PROPOSALS, NOT ACCEPTED CANON" in leadership and "None ratified" in leadership, "Political status lost")
    image_names = sorted(n for n in actual if Path(n).suffix.lower() in (".png", ".jpeg", ".jpg"))
    require(len(image_names) == 4, "Image inventory changed")
    for name in image_names:
        require(current[name] == base[name], f"Image bytes changed: {name}")
        with Image.open(ROOT / name) as im:
            im.verify()
        with Image.open(ROOT / name) as im:
            im.load()
    pdf_names = sorted(n for n in actual if n.endswith(".pdf"))
    require(pdf_names == sorted(p["path"] for p in manifest["pdfs"]), "PDF inventory mismatch")
    pages = 0
    for expected in manifest["pdfs"]:
        reader = PdfReader(ROOT / expected["path"], strict=True)
        require(not reader.is_encrypted and len(reader.pages) == expected["pages"], "PDF unreadable/page count changed")
        content = "\n".join(p.extract_text() or "" for p in reader.pages)
        require(all((p.extract_text() or "").strip() for p in reader.pages), "Unreadable PDF page")
        text[expected["path"]] = content
        pages += len(reader.pages)
    require(pages == 13, "Expected thirteen historical PDF pages")
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
        require(set(names.decode().rstrip("\0").split("\0")) == actual, "Git inventory mismatch")
        for name in actual:
            require(git("show", prefix + name) == current[name], f"Git bytes differ: {name}")
    print(json.dumps({"result": "PASS", "base_commit": BASE, "project_files": len(actual), "snapshot_hashes": len(manifest["files"]), "unchanged_base_files": len(base)-len(changed), "append_only_base_files": len(changed), "added_files": len(actual-base_names), "source_archive_checked": archive.exists(), "source_manifest_entries": len(supplied["files"]), "imported_files": len(manifest["imported_paths"]), "utf8_files": len(text)-len(pdf_names), "unchanged_images": len(image_names), "pdf_files": len(pdf_names), "readable_pdf_pages": pages, "unchanged_arc_headings": 35, "realm_rows_each": 7, "local_markdown_links": links, "git_index_checked": args.git_index, "commit_checked": args.commit, "limitations": ["Historical validators require their original checkouts.", "A missing ZIP is reported; recorded payload hashes still apply.", "Source provenance and remaining canon choices are qualified in V06_IMPORT_AUDIT.md."]}, indent=2))


if __name__ == "__main__":
    main()
