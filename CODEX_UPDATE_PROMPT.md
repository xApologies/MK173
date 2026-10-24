# CODEX — MK173 Live Model v0.6 Incremental Import

Repository: `C:\Users\rando\_MK173` (verify actual path) -> https://github.com/xApologies/MK173
Baseline expected `main` remote SHA: `d921703d0f0724fce98ebea2d667899e000e2df3` (v0.5). ZIP: `_inbox/MK173_live_model_delta_v0_6.zip`.

## Preflight — mandatory
1. Verify local repository root, clean Git worktree, branch, origin, and remote HEAD. Do not reset, force-push, delete, or overwrite any user changes. If remote advanced, reconcile with current state before importing.
2. Verify ZIP entries are safe relative paths, not symlinks, no path traversal; CRC and SHA256 against `provenance/V06_PAYLOAD_SHA256.json`. Validate Markdown UTF-8 and source PDFs readable. Unpack to ignored `_inbox` staging.
3. Preserve all v0.4/v0.5 canon, world clock, images, snapshots, audit scripts, and provenance. Do not edit AERA or MK163 repositories. Do not import old Genesis Point geography as canon.

## Integration
4. Add the seven new `world_clock/L2_WORLD_CIVILIZATION/...` and `canon/POST_V05_DECISIONS.md` files at exactly their relative paths, plus three historical source PDFs and this update's source manifest/provenance as appropriate. If a path already exists, compare and merge without blind replacement.
5. Append a dated v0.6 update note and links in `LIVE_MODEL.md`, `README.md`, `canon/DECISIONS.md`, `canon/08_ECONOMY_AND_DAILY_LIFE.md` and `provenance/CHANGELOG.md` (do not truncate earlier content). Supersede prior OPEN eln/ahm conversion with accepted 180:1; six ordinary denominations are 1/6/12/18/24/30. Mark universal realm trade currency architecture accepted but labels/denominations working/open. Add map/leadership proposal links without promoting them to accepted canon.
6. Cross-check `canon/09_ENVIRONMENTAL_GEOGRAPHY.md` and `canon/10_NARRATIVE_CONSTITUTION.md` for compatibility; do not rewrite or duplicate their content. Add relevant navigation under world_clock/README.md or new index. Keep existing `world_clock/EVENTS_V2.csv` untouched unless adding a documented schema migration; no fabricated dates.
7. Maintain distinction: accepted user decisions versus working Astraeus proposals versus open parameters. The leadership roster and routes are WORKING, not accepted; all named political map locations must be compared against existing artwork before promotion. Historical BAEN spelling only in correction provenance; active text uses vaen. Do not manufacture an accepted pirate king or old sanctuary system.
8. MK163 economic source remains upstream linked reference. Copy only adopted numerical benchmarks and source pointers, not the MK163 repository or its character-specific story.

## Validation / publication
9. Audit accepted terminology, 7 books, 35 existing arc headings unchanged, no deleted images, no unrelated file changes, links resolve, PDFs remain provenance only, no hidden archives committed. Generate a dated `provenance/V06_IMPORT_AUDIT.md` and a new v0.6 snapshot hash manifest, preserving old manifests and verifiers.
10. Commit with message `Integrate MK173 pre-Red civilization and economy model v0.6`, push normally (never force), independently verify remote SHA matches local HEAD. Report changed paths, audit results, commit SHA and remaining OPEN decisions. No narrative chapters drafted by this update.
