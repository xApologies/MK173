"""Verify the separate seven-book Pass 1 audit, source packages and Git checkpoints; Python 3.10+."""

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
BASE = "f24072dc47756a10a1f05e5dcbe0a3c33a5dac7f"
MANIFEST = "provenance/SEVEN_BOOK_PASS1_AUDIT_SHA256.json"
REPORT = "provenance/SEVEN_BOOK_PASS1_AUDIT.md"
SCRIPT = "provenance/verify_seven_book_audit.py"
APPENDED = {"README.md", "LIVE_MODEL.md", "canon/DECISIONS.md", "world_clock/README.md", "provenance/CHANGELOG.md"}
CHECKPOINTS = {
    "RED": "82753131518018e94a65d37178de05a87d1ecee3",
    "ORANGE": "8dab4995c9451ea9b2540f0ad4d5c7d836809536",
    "YELLOW": "4351150d9e3323294fa277f7cb707645a750d55f",
    "GREEN": "ca760969f63865ac6c4ad58f90b6efdd4a07a776",
    "BLUE": "55cd299e253164d3f549599b32b394e63dd59a5f",
    "VIOLET": "2e2d5ab3eca669e3342e86d42c3d8825c174301b",
    "WHITE": BASE,
}
EXPECTED_BEATS = {book: [5, 5, 5, 5, 5] for book in CHECKPOINTS}
EXPECTED_BEATS.update(RED=[5, 4, 5, 5, 5], WHITE=[5, 5, 5, 6, 6])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def record(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def git(*args, input=None):
    return subprocess.check_output(["git", *args], cwd=ROOT, input=input)


def git_tree(commit=None):
    """Read Git blobs without checking out or changing an index/worktree."""
    if commit is None:
        entries = git("ls-files", "--stage", "-z").split(b"\0")
    else:
        entries = git("ls-tree", "-r", "-z", commit).split(b"\0")
    objects = []
    for entry in entries:
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        fields = metadata.split()
        require(fields[0] == b"100644", f"Unexpected Git file mode: {name!r}")
        if commit is None:
            require(fields[2] == b"0", "Unmerged index entry")
            oid = fields[1]
        else:
            require(fields[1] == b"blob", "Unexpected Git object")
            oid = fields[2]
        objects.append((name.decode("utf-8"), oid))
    stream = io.BytesIO(git("cat-file", "--batch", input=b"\n".join(oid for _, oid in objects) + b"\n"))
    result = {}
    for name, oid in objects:
        header = stream.readline().strip().split()
        require(len(header) == 3 and header[0] == oid and header[1] == b"blob", f"Bad Git blob header: {name}")
        result[name] = stream.read(int(header[2]))
        require(stream.read(1) == b"\n", "Bad Git blob separator")
    require(not stream.read(), "Extra Git batch output")
    return result


def get_current():
    current = {}
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in (".git", "_inbox") or "__pycache__" in relative.parts:
            continue
        require(not path.is_symlink() and ".git" not in relative.parts, f"Unexpected path: {relative}")
        if path.is_file() and path.suffix != ".pyc":
            current[relative.as_posix()] = path.read_bytes()
    return current


def audit(current):
    baseline = git_tree(BASE)
    require(len(baseline) == 126, "Unexpected White baseline inventory")
    for name, data in baseline.items():
        require(current.get(name) == data, f"White baseline changed during separate audit: {name}")
    summaries = []
    zip_results = []
    historical_hashes = 0
    supplied_hashes = 0
    previous_commit = "6cf26e538a0c6d1ffae8453a5b4fb33872cce62b"
    previous = git_tree(previous_commit)
    for book, commit in CHECKPOINTS.items():
        manifest_path = f"provenance/{book}_PASS1_SNAPSHOT_SHA256.json"
        snapshot = json.loads(current[manifest_path])
        require(snapshot["base_commit"] == previous_commit, f"Broken checkpoint chain: {book}")
        require(git("rev-parse", f"{commit}^").decode().strip() == previous_commit, f"Unexpected parent: {book}")
        checkpoint = git_tree(commit)
        require(checkpoint[manifest_path] == current[manifest_path], f"Historical manifest changed: {book}")
        require(set(snapshot["files"]) == set(checkpoint) - {manifest_path}, f"Historical snapshot coverage: {book}")
        for name, info in snapshot["files"].items():
            require(record(checkpoint[name]) == info, f"Historical checkpoint hash: {book}/{name}")
            historical_hashes += 1
        require(set(snapshot["base_files"]) == set(previous), f"Historical base inventory: {book}")
        require(all(record(previous[n]) == info for n, info in snapshot["base_files"].items()), f"Historical base hashes: {book}")
        changed = {n for n in previous if checkpoint.get(n) != previous[n]}
        require(set(previous) <= set(checkpoint) and changed == APPENDED, f"Unexpected historical change: {book}")
        require(changed == set(snapshot["modified_paths"]) == set(snapshot["append_only_paths"]), f"Historical change record: {book}")
        require(all(checkpoint[n].startswith(previous[n]) for n in changed), f"Historical prefix lost: {book}")
        require(set(checkpoint) - set(previous) == set(snapshot["added_paths"]), f"Historical additions: {book}")
        source = snapshot["source_manifest"]
        source_hashes = source.get("files", source)
        source_paths = set(snapshot["archive_files"])
        excluded = {"provenance/SHA256.json"}
        if book == "GREEN":
            excluded.add("CODEX_UPDATE_PROMPT.md")
        require(len(source_paths) == 9 and set(source_hashes) == source_paths - excluded, f"Source coverage: {book}")
        require(all(snapshot["archive_files"][n]["sha256"] == h for n, h in source_hashes.items()), f"Source hashes: {book}")
        supplied_hashes += len(source_hashes)
        imported = {f"narrative/{book}/LIVE_MODEL.md"} | {f"narrative/{book}/ARC_{i:02d}_SUMMARY.md" for i in range(1, 6)}
        require(set(snapshot["imported_paths"]) == imported, f"Imported inventory: {book}")
        require(all(record(current[n]) == snapshot["archive_files"][n] and current[n] == checkpoint[n] for n in imported), f"Source payload changed: {book}")
        archive = ROOT / "_inbox" / snapshot["archive"]["name"]
        if archive.exists():
            info = snapshot["archive"]
            require(record(archive.read_bytes()) == {k: info[k] for k in ("bytes", "sha256")}, f"Archive hash: {book}")
            with zipfile.ZipFile(archive) as z:
                require(len(z.infolist()) == 9 and set(z.namelist()) == source_paths and z.testzip() is None, f"ZIP CRC/inventory: {book}")
                require(sum(i.file_size for i in z.infolist()) == info["uncompressed_bytes"], f"ZIP size: {book}")
                require(all(record(z.read(n)) == snapshot["archive_files"][n] for n in source_paths), f"ZIP entry hashes: {book}")
                require(json.loads(z.read("provenance/SHA256.json")) == source, f"ZIP source manifest: {book}")
        zip_results.append({"book": book, "name": archive.name, "available_and_verified": archive.exists(), "sha256": snapshot["archive"]["sha256"], "supplied_hashes": len(source_hashes), "excluded_from_source_manifest": sorted(excluded)})
        registry_path = f"narrative/{book}/ARCS.md"
        registry = dict(re.findall(r"^## (\d{2}) (.+)$", current[registry_path].decode("utf-8"), re.M))
        require(list(registry) == ["01", "02", "03", "04", "05"], f"Registry structure: {book}")
        require(current[registry_path] == previous[registry_path], f"Registry changed: {book}")
        live = current[f"narrative/{book}/LIVE_MODEL.md"].decode("utf-8")
        require("ACCEPTED" in live or "author-accepted" in live, f"Book acceptance status: {book}")
        accepted = []
        for number, title in registry.items():
            path = f"narrative/{book}/ARC_{number}_SUMMARY.md"
            text = current[path].decode("utf-8")
            require(text.splitlines()[0].upper() == f"# {book} — Arc {number}: {title}".upper(), f"Summary title: {path}")
            pattern = r"^(\d+)\. \*\*" if book == "BLUE" else r"^### (\d+)\. "
            beats = re.findall(pattern, text, re.M)
            count = EXPECTED_BEATS[book][int(number)-1]
            require(beats == [str(i) for i in range(1, count+1)], f"Beat sequence: {path}")
            require(title in live and ("ACCEPTED" in text or "accepted" in text), f"Book/summary status or title: {path}")
            require(not re.search(r"\bBAEN\b|B-A-E-N", text, re.I), f"Retired term in accepted narrative: {path}")
            require(not re.search(r"^(?:<<<<<<< |=======$|>>>>>>> )", text, re.M), f"Conflict marker: {path}")
            accepted.append({"path": path, "number": number, "title": title, "main_beats": len(beats)})
        require(accepted == snapshot["arcs"], f"Snapshot arc metadata: {book}")
        summaries.append({"book": book, "commit": commit, "arcs": accepted, "main_beats": sum(a["main_beats"] for a in accepted)})
        previous_commit, previous = commit, checkpoint
    texts = {n: b.decode("utf-8", errors="strict") for n, b in current.items() if Path(n).suffix in (".md", ".json", ".csv", ".py") or n in (".gitignore", ".gitattributes")}
    require(all("\0" not in s and "\ufffd" not in s for s in texts.values()), "Invalid text")
    links = 0
    for name, text in texts.items():
        if not name.endswith(".md"):
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            path = ((ROOT / name).parent / unquote(parsed.path)).resolve()
            require(path.is_relative_to(ROOT) and path.exists(), f"Broken local link: {name} -> {target}")
            links += 1
    for suffix in ("", "_V2"):
        clocks = list(csv.DictReader(io.StringIO(texts[f"world_clock/REALM_CLOCKS{suffix}.csv"])))
        events = list(csv.DictReader(io.StringIO(texts[f"world_clock/EVENTS{suffix}.csv"])))
        require([r["realm"] for r in clocks] == ["White", "Red", "Orange", "Yellow", "Green", "Blue", "Violet"], "Clock inventory")
        require(clocks[0]["white_to_local_factor"] == "1" and all(not r["white_to_local_factor"] and r["status"] == "OPEN" for r in clocks[1:]), "Clock values")
        require([(r["event_id"], r["book"], r["arc"]) for r in events] == [("E0001", "RED", "01"), ("E0002", "RED", "01"), ("E0003", "WHITE", "05")], "Event inventory")
        require(all(not r["white_date"] and r["status"] == "WORKING" for r in events), "Event dates/status")
        if suffix:
            require(events[1]["predecessor_id"] == "E0001" and not events[2]["predecessor_id"], "Event predecessor status")
    # Specific evidence anchors supplement the prose audit; these are not a proof of literary consistency.
    anchors = {
        "narrative/BLUE/LIVE_MODEL.md": ["Conservator's daughter"],
        "narrative/ORANGE/ARC_05_SUMMARY.md": ["Seren by correspondence"],
        "narrative/ORANGE/LIVE_MODEL.md": ["May correspond in Arc 05"],
        "narrative/YELLOW/ARC_04_SUMMARY.md": ["passage is independent of the ancient network"],
        "narrative/GREEN/ARC_04_SUMMARY.md": ["Physical reactivation remains prohibited", "not itself a network component"],
        "narrative/BLUE/ARC_01_SUMMARY.md": ["Corridor belonging to the ancient weaving network", "distinct from the vessel's own hull sigils"],
        "narrative/BLUE/ARC_04_SUMMARY.md": ["unrecognized intermediate dependency", "conditional joint noninvasive research"],
        "narrative/VIOLET/ARC_03_SUMMARY.md": ["does not establish extra physical dimensions"],
        "narrative/VIOLET/ARC_05_SUMMARY.md": ["all six meet in Stormwall in White", "transition paths and global consequences remain unverified"],
        "narrative/WHITE/ARC_02_SUMMARY.md": ["The reunion", "oversight body defers approval"],
        "narrative/WHITE/ARC_03_SUMMARY.md": ["withdraws the premature certification request", "idea remains unproven"],
        "narrative/WHITE/ARC_04_SUMMARY.md": ["authorized noncritical subsystem test", "only bounded feasibility", "remaining stages are not presumed safe"],
        "narrative/WHITE/ARC_05_SUMMARY.md": ["no total permanent repair", "mountain remains physically present", "Proposed closing line:"],
        "canon/POST_V05_DECISIONS.md": ["180 ahm = 1 eln", "No White ahm coin"],
        "canon/TERMINOLOGY_CORRECTION.md": ["NO separate BAEN resource"],
    }
    for name, phrases in anchors.items():
        require(all(phrase in texts[name] for phrase in phrases), f"Continuity evidence anchor changed: {name}")
    total = sum(b["main_beats"] for b in summaries)
    require(total == 176, "Unexpected total major points")
    images = [n for n in baseline if Path(n).suffix.lower() in (".png", ".jpg", ".jpeg")]
    pdfs = [n for n in baseline if n.endswith(".pdf")]
    require(len(images) == 4 and len(pdfs) == 3, "Media inventory")
    return {"white_import_commit": BASE, "baseline_files_preserved": len(baseline), "book_checkpoints_verified": len(CHECKPOINTS), "historical_snapshot_hashes_verified": historical_hashes, "books": summaries, "accepted_arcs": 35, "accepted_major_points": total, "source_payloads_unchanged": 42, "supplied_source_hashes_verified": supplied_hashes, "archives": zip_results, "preserved_clock_csvs": 4, "preserved_images": images, "preserved_pdfs": pdfs, "local_links": links, "open_issue_ids": ["SB-01", "SB-02", "SB-03", "SB-04", "SB-05", "SB-06", "SB-07"], "limitations": ["Semantic findings require reading the separate prose audit; phrase checks are not a mathematical or literary proof.", "Unavailable archives are explicitly reported; recorded payload hashes remain checked.", "No external AERA checkout, manuscript completion, authorship or license certification is claimed."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--git-index", action="store_true")
    selection.add_argument("--commit")
    args = parser.parse_args()
    require(Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve() == ROOT, "Wrong Git root")
    current = get_current()
    manifest = json.loads(current[MANIFEST])
    require(manifest["base_commit"] == BASE, "Wrong audit baseline")
    require(set(current) == set(manifest["files"]) | {MANIFEST}, "Audit inventory changed")
    require(all(record(current[n]) == info for n, info in manifest["files"].items()), "Audit snapshot hash mismatch")
    baseline = git_tree(BASE)
    require(set(current) - set(baseline) == {REPORT, SCRIPT, MANIFEST}, "Unexpected audit additions")
    observed = audit(current)
    # Archive availability can differ on another checkout; it is always reported truthfully.
    expected = manifest["audit_results"]
    for key in expected:
        if key == "archives":
            require([{k: v for k, v in r.items() if k != "available_and_verified"} for r in observed[key]] == [{k: v for k, v in r.items() if k != "available_and_verified"} for r in expected[key]], "Archive records changed")
        else:
            require(observed[key] == expected[key], f"Audit result changed: {key}")
    for name in (REPORT, SCRIPT, MANIFEST):
        text = current[name].decode("utf-8")
        require(all(line == line.rstrip(" \t") for line in text.splitlines()), f"Trailing whitespace: {name}")
        require(not re.search(r"^(?:<<<<<<< |=======$|>>>>>>> )", text, re.M), f"Conflict marker: {name}")
    if args.git_index or args.commit:
        selected = None if args.git_index else git("rev-parse", "--verify", f"{args.commit}^{{commit}}").decode().strip()
        if selected:
            git("merge-base", "--is-ancestor", BASE, selected)
        require(git_tree(selected) == current, "Git/worktree bytes differ")
    print(json.dumps({"result": "PASS", "project_files": len(current), "snapshot_hashes": len(manifest["files"]), **observed, "git_index_checked": args.git_index, "commit_checked": args.commit}, indent=2))


if __name__ == "__main__":
    main()
