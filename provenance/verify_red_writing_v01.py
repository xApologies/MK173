"""Verify the additive Red writing handoff and its preserved seven-book baseline; Python 3.10+."""

import argparse
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = "2f21fddcd67d40b7aa6c816a221950127125c317"
MANIFEST = "provenance/RED_WRITING_V01_SNAPSHOT_SHA256.json"
PRIOR = "provenance/SEVEN_BOOK_PASS1_AUDIT_SHA256.json"
APPENDED = {"README.md", "LIVE_MODEL.md", "canon/DECISIONS.md", "narrative/RED/README.md", "world_clock/README.md", "provenance/CHANGELOG.md"}
MAPPING = {
    "canon/11_MATHEMATICS_AND_PROSE_STYLE_ADDENDUM.md": "canon/11_MATHEMATICS_AND_PROSE_STYLE_ADDENDUM.md",
    "narrative/RED/CHAPTER_DEVELOPMENT_HANDOFF.md": "narrative/RED/CHAPTER_DEVELOPMENT_HANDOFF.md",
    "BREADCRUMB_NEXT_THREAD.txt": "provenance/handoffs/RED_WRITING_BREADCRUMB_v0_1.txt",
}
ADDED = set(MAPPING.values()) | {MANIFEST, "provenance/RED_WRITING_V01_IMPORT_AUDIT.md", "provenance/verify_red_writing_v01.py"}

# Reuse the unchanged historical verifier's read-only Git and audit functions.
spec = importlib.util.spec_from_file_location("seven_book_baseline", ROOT / "provenance/verify_seven_book_audit.py")
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
git, require, record = previous.git, previous.require, previous.record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--git-index", action="store_true")
    selection.add_argument("--commit")
    args = parser.parse_args()
    require(Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve() == ROOT, "Wrong repository root")
    current = previous.get_current()
    manifest = json.loads(current[MANIFEST])
    require(manifest["base_commit"] == BASE, "Unexpected baseline")
    require(set(current) == set(manifest["files"]) | {MANIFEST} and len(current) == 135, "Current inventory changed")
    require(all(record(current[n]) == info for n, info in manifest["files"].items()), "Current hash mismatch")
    base = previous.git_tree(BASE)
    require(len(base) == 129 and set(base) <= set(current), "Baseline inventory changed")
    require(set(manifest["base_files"]) == set(base), "Recorded baseline inventory")
    require(all(record(base[n]) == info for n, info in manifest["base_files"].items()), "Recorded baseline hash")
    changed = {n for n in base if base[n] != current[n]}
    require(changed == APPENDED == set(manifest["append_only_paths"]) == set(manifest["modified_paths"]), "Unexpected modification")
    require(all(current[n].startswith(base[n]) for n in changed), "Historical prefix changed")
    require(set(current) - set(base) == ADDED == set(manifest["added_paths"]), "Unexpected addition")
    prior = json.loads(base[PRIOR])
    require(set(prior["files"]) == set(base) - {PRIOR}, "Prior audit snapshot coverage")
    require(all(record(base[n]) == info for n, info in prior["files"].items()), "Prior audit hash mismatch")
    historical = previous.audit(base)
    for key, expected in prior["audit_results"].items():
        if key == "archives":
            expected = [{k: v for k, v in row.items() if k != "available_and_verified"} for row in expected]
            observed = [{k: v for k, v in row.items() if k != "available_and_verified"} for row in historical[key]]
        else:
            observed = historical[key]
        require(observed == expected, f"Prior audit evidence changed: {key}")
    require(manifest["import_mapping"] == MAPPING, "Source/destination mapping changed")
    wrappers = {"CODEX_UPDATE_PROMPT.md", "README.md", "provenance/SHA256.json"}
    source_paths = set(MAPPING) | wrappers
    require(set(manifest["archive_files"]) == source_paths, "Archive inventory")
    source = manifest["source_manifest"]
    require(set(source) == source_paths - {"provenance/SHA256.json"}, "Source manifest coverage")
    require(all(re.fullmatch(r"[0-9a-f]{64}", h) and manifest["archive_files"][n]["sha256"] == h for n, h in source.items()), "Source hashes")
    for source_name, target_name in MAPPING.items():
        require(record(current[target_name]) == manifest["archive_files"][source_name], f"Imported source bytes changed: {target_name}")
    require({c["path"] for c in manifest["wrapper_conflicts"]} == wrappers, "Wrapper conflict inventory")
    for conflict in manifest["wrapper_conflicts"]:
        n = conflict["path"]
        require(record(base[n])["sha256"] == conflict["base_sha256"] and manifest["archive_files"][n]["sha256"] == conflict["archive_sha256"], f"Wrapper hash changed: {n}")
    archive = ROOT / "_inbox" / manifest["archive"]["name"]
    if archive.exists():
        info = manifest["archive"]
        require(record(archive.read_bytes()) == {k: info[k] for k in ("bytes", "sha256")}, "ZIP hash mismatch")
        with zipfile.ZipFile(archive) as z:
            require(len(z.infolist()) == 6 and set(z.namelist()) == source_paths and z.testzip() is None, "ZIP CRC/inventory")
            require(sum(i.file_size for i in z.infolist()) == info["uncompressed_bytes"], "ZIP size")
            require(all(record(z.read(n)) == manifest["archive_files"][n] for n in source_paths), "ZIP entry hashes")
            require(json.loads(z.read("provenance/SHA256.json")) == source, "Supplied manifest mismatch")
    texts = {n: data.decode("utf-8", errors="strict") for n, data in current.items() if Path(n).suffix in (".md", ".json", ".csv", ".py", ".txt") or n in (".gitignore", ".gitattributes")}
    require(all("\0" not in t and "\ufffd" not in t for t in texts.values()), "Invalid text")
    addendum = texts["canon/11_MATHEMATICS_AND_PROSE_STYLE_ADDENDUM.md"]
    for phrase in ("Status: WORKING proposal", "## Working examples, not newly locked canon", "NOT a claim that a detailed patent statute", "legal distinction remains OPEN", "Not a quota or required allocation", "Exact chapter counts and scene breakdowns", "do not silently add major new plot events", "Do not invent Genesis-field equations", "supplements, never replaces"):
        require(phrase in addendum, f"Addendum status boundary missing: {phrase}")
    handoff = texts["narrative/RED/CHAPTER_DEVELOPMENT_HANDOFF.md"]
    for phrase in ("chapter plans, and manuscripts not yet written", "no premature knowledge of the network's true cause", "Municipal Genesis stabilization is independent", "Starscape singularity/Genesis-field conditions, not network failure", "Do not invent chapter count", "legal patent regimes as accepted canon"):
        require(phrase in handoff, f"Handoff safeguard missing: {phrase}")
    supplied_titles = re.findall(r"^(\d)\. \*\*(.+?)\*\* —", handoff, re.M)
    registry = re.findall(r"^## (\d{2}) (.+)$", texts["narrative/RED/ARCS.md"], re.M)
    require([(int(n), t.replace("’", "'")) for n, t in supplied_titles] == [(int(n), t.replace("’", "'")) for n, t in registry], "Handoff arc titles differ beyond apostrophe typography")
    require("precise patent law and international recognition remain OPEN" in texts[MAPPING["BREADCRUMB_NEXT_THREAD.txt"]], "Breadcrumb patent scope changed")
    for n in MAPPING.values():
        require(not re.search(r"\bBAEN\b|B-A-E-N", texts[n], re.I), f"Retired resource term in payload: {n}")
    for n in changed | ADDED:
        introduced = current[n][len(base[n]):].decode("utf-8") if n in changed else texts[n]
        require(all(line == line.rstrip(" \t") for line in introduced.splitlines()), f"Introduced trailing whitespace: {n}")
        require(not re.search(r"\n[ \t\r]*\n\Z", introduced), f"Introduced blank line at EOF: {n}")
        require(not re.search(r"^(?:<<<<<<< |=======$|>>>>>>> )", introduced, re.M), f"Conflict marker: {n}")
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
    patterns = [r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{30,}", r"AKIA[0-9A-Z]{16}", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"]
    require(not any(re.search(p, text) for text in texts.values() for p in patterns), "Possible credential pattern in text")
    require(not any(Path(n).suffix.lower() in (".zip", ".tar", ".gz", ".7z") for n in current), "Unexpected archive in project inventory")
    if args.git_index or args.commit:
        commit = None if args.git_index else git("rev-parse", "--verify", f"{args.commit}^{{commit}}").decode().strip()
        if commit:
            git("merge-base", "--is-ancestor", BASE, commit)
        require(previous.git_tree(commit) == current, "Git/worktree bytes differ")
    print(json.dumps({"result": "PASS", "base_commit": BASE, "project_files": len(current), "snapshot_hashes": len(manifest["files"]), "unchanged_base_files": len(base)-len(changed), "append_only_files": len(changed), "added_files": len(ADDED), "imported_payloads": len(MAPPING), "archive_checked": archive.exists(), "supplied_hashes": len(source), "utf8_files": len(texts), "unchanged_accepted_arcs": historical["accepted_arcs"], "unchanged_major_points": historical["accepted_major_points"], "unchanged_book_payloads": historical["source_payloads_unchanged"], "historical_snapshot_hashes": historical["historical_snapshot_hashes_verified"], "historical_archives_available": sum(row["available_and_verified"] for row in historical["archives"]), "matching_red_handoff_titles": len(supplied_titles), "local_links": links, "git_index_checked": args.git_index, "commit_checked": args.commit, "open_scope": ["Patent rules and legal distinctions", "Prose balance and voice", "Chapters, scenes and possible intellectual-property plot", "Previously documented seven-book issues"]}, indent=2))


if __name__ == "__main__":
    main()
