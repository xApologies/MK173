# MK173 v0.4 import audit — 2026-10-24

## Result and scope

The supplied 22-file handoff is imported at repository root, with three unchanged images, seven books containing five working arcs each, and the complete original LIVE_MODEL text preserved as an exact byte prefix. Integrity checks pass subject to the provenance and continuity qualifications below. Development 08–10 cannot be individually reconstructed from this package; this audit does not certify complete stage-level provenance.

Local root: `C:\Users\rando\_MK173`. Branch: `main`. Origin: [xApologies/MK173](https://github.com/xApologies/MK173), Git URL `https://github.com/xApologies/MK173.git`. Git version: 2.53.0.windows.3. Before import, this directory contained only `_inbox/MK173_handoff_v04.zip` and was not a Git repository. The remote was confirmed to have no refs using a successful `git ls-remote --symref` call; GitHub metadata reported default branch main and size zero. The initial sandbox network attempt failed before access; the permitted retry succeeded. No existing project paths or histories conflicted.

All writes and Git mutations target MK173. The ZIP and staged extraction remain in ignored `_inbox`. No files were deleted, no nested Git repository was introduced, and no force operation or history replacement was used. AERA was read only through source-file requests and a remote-ref query. MK163 received only a repository-metadata read. Neither repository, its local directories, nor any other external repository was modified. No external source corpus was copied into MK173; inherited summaries already in the supplied handoff are preserved.

This is a pre-publication audit recorded in the import commit. The commit cannot contain its own SHA. Publication is verified separately by comparing local HEAD with a fresh remote main ref after a normal push; do not treat this document alone as proof of remote publication.

## Archive and file accounting

- Archive: `MK173_handoff_v04.zip`, 6,801,942 bytes, SHA256 `adbf60cf673ad5a1913430783fb7169d7241b519b771bf0141ea821c101a2de4`.
- Archive payload: 22 regular files, 6,960,518 uncompressed bytes; 16 Markdown files, two CSVs, one JSON manifest, two PNGs and one JPEG. All 19 text files decode strictly as UTF-8. No executable source or Git metadata was supplied.
- Original [SHA256 manifest](SHA256.json): all 21 listed file hashes match the archive; it intentionally does not hash itself. The new [snapshot manifest](IMPORT_SHA256.json) records all 22 source file sizes and hashes, including the original manifest's hash.
- Final project: 27 files. The snapshot manifest hashes the other 26 files and excludes itself to avoid a circular hash. The containing Git commit records all 27 files, including that manifest.
- Seventeen supplied files are byte-identical: CODEX_PROMPT, three canon documents, two CSVs, seven arc files, three images and the original manifest. Four supplied files have append-only additions: LIVE_MODEL, the image index, world-clock README and changelog. The root README is deliberately rewritten as the project index; its original bytes remain recoverable from the untouched ZIP and staged extraction.
- Five added files: root `.gitignore` and `.gitattributes`, this audit, the snapshot manifest and [the verifier](verify_import.py). Git attributes disable text conversion so hashes remain stable despite the host's global autocrlf setting. `_inbox`, Python bytecode and cache directories are ignored.

Archive checks covered CRC, exact file inventory, absolute/traversal paths, alternate data streams, Windows reserved names, invalid/control characters, trailing dots/spaces, case collisions, symlinks and nonregular entries, encrypted entries and bounded uncompressed sizes. Every destination was compared or checked for absence before any copy. The file-size limit was 25 MB per entry and the total limit was 50 MB. No unsafe entries or destination conflicts were found.

## Images and provenance

| Image | Format and dimensions | Verified SHA256 |
|---|---|---|
| [Geography concept](../images/maps/geography_v01.png) | PNG, 1774 × 887 | `58e258f5cb88aa5b11ba8f8f36075717c7547bb9b559e942626cb5e29521b0d8` |
| [Political concept](../images/maps/political_v01.png) | PNG, 1774 × 887 | `5c1e6084a64595175432ab4b8b34dbb9fe0991e920abea244954c891b99ad48e` |
| [Nonordinary geometry reference](../images/references/nonordinary_geometry.jpeg) | JPEG, 1320 × 1012 | `b8c18c90390f945114d86cec3f57b9ca382f5c0cc45258bd9292c2bcb43dabf3` |

All three passed Pillow verification and full pixel decoding and were visually inspected. Geography depicts four continental landmasses plus a central archipelago; politics depicts illustrative territories over that setting; the reference depicts nonordinary water/sky geometry. No fourth image or source MK163 map is present in the handoff. This is an archive-inventory observation, not a visual-comparison proof against an unavailable original MK163 map.

The handoff calls the geography image original AI-generated MK173 workshop art, the political image an overlay, and the JPEG a user-supplied reference. Generator/model/seed/prompt history, independently verifiable authorship, the reference's original URL/creator and reuse terms are not supplied. These remain provenance gaps. Hash integrity does not establish authorship or licensing; no license is inferred or added.

Neither PNG exposes embedded metadata through Pillow. The JPEG's EXIF/IPTC describes it as a screenshot and records `2026:10:12 12:35:09` without a timezone. No creator, source URL or GPS location was found in the inspected metadata. This embedded timestamp is not independently authenticated and does not establish the original artwork's creation date. Metadata and pixels are retained unchanged.

The political image prints an 80,000-mile **diameter**, an incompatible Earth comparison, a capital marker and a note treating major geographic features as canon. These conflict with or exceed the written accepted approximately 80,000-mile **circumference** and unplaced city coordinates. Its measurements, boundaries, states and annotations remain concept-only. The geography scale and legend likewise cannot establish distances or travel times. Original images are retained unchanged and the conflict is recorded in the image index and appended live-model notes.

## Ten pre-narrative development stages

Source status is distinguished from import verification. The live model explicitly numbers 01–07. The original changelog says v0.4 consolidates Development 08–10 decisions, clock scaffolding and the second political map, but it does not assign topics to each of those three stages. All ten stage numbers are accounted for below; only seven have individually attributable evidence.

| Stage | Supplied evidence and retained scope | Coverage |
|---|---|---|
| 01 | LIVE_MODEL Development 01: Aren's family and working upbringing; proposed Tavin and Conservator family. | Individually represented; proposed names remain WORKING. |
| 02 | Development 02: selected environmental/engineering causal model C and independent municipal stabilization model A. | Individually represented; precise network math OPEN. |
| 03 | Development 03: selected general relational Weaving scope B under inherited constraints. | Individually represented; operation permissions remain bounded. |
| 04 | Development 04: Asterhold civic council; proposed Concord cities, nine seats and institutions. | Individually represented; accepted/working distinctions retained. |
| 05 | Development 05: selected recurring chromatic ensemble A; proposed character names. | Individually represented; no new character canon. |
| 06 | Development 06: stable realm-time correspondence B and optional interworld bridges. | Individually represented; numerical factors OPEN. |
| 07 | Development 07: constitutional aristocracy B; noble-rank distinction and provisional polities. | Individually represented; borders unratified. |
| 08 | Original changelog's combined Development 08–10 claim; newer canon, economy, clock and political-map material retained. | Aggregate evidence only; individual topic boundary and transcript missing. |
| 09 | Same combined Development 08–10 evidence. | Aggregate evidence only; not assigned an invented topic. |
| 10 | Same combined Development 08–10 evidence. | Aggregate evidence only; not assigned an invented topic. |

The newest decisions and world/story summary contain the single-mountain/engineered-adjacency clarification, Concord eln/ahm economy, specialized resources and concept-map status. These additions are preserved, but their exact allocation among 08, 09 and 10 is not recoverable. Restoring original workshop records would be necessary to certify stage-by-stage completeness. No prose chapters were drafted.

## Continuity, references and missing information

- Seven arc files have exactly headings 01–05, are explicitly working names rather than manuscripts, and retain 35 OPEN detailed outlines. Their order and titles correspond to the supplied live model, allowing typographic apostrophe differences.
- ACCEPTED, WORKING and OPEN sections remain intact in the decision ledger. The approximate 80,000-mile circumference is ACCEPTED there, while the older live-model wording calls specific planet size a proposal. Appended precedence notes preserve both the historical text and the newer status.
- Vaelith, velis, ru’ne (curly apostrophe), maege and maegi are present with their protected spellings. Case changes at sentence starts and the hyphenated spelling guides are not alternate terms. No normalization or renaming was performed.
- BAEN / B-A-E-N versus vaen / V-A-E-N remains explicitly unresolved. The inherited definition of vaen does not establish what the user's BAEN meant.
- Realm factors: White = 1 as reference identity; all six chromatic factors empty and OPEN. Three unique events have valid book/arc references, WORKING status and empty White dates. E0002's reference to E0001 resolves. The last event uses prose chronology rather than a stable dependency ID. No ratios, prices or exchange rates were added; eln/ahm conversion remains OPEN.
- The original clock README describes intended realm-local-time and provenance fields absent from the seven-column event CSV. The appended note identifies this schema gap without fabricating fields or values. The directory is a chronology aid; it does not redefine AERA's L0–L4 World Clock.
- The historical geography filename in LIVE_MODEL is absent as a physical path. It is explicitly mapped to the existing geography image in the appended navigation. All current local Markdown links resolve. This qualified historical alias is the only stale supplied project-file reference; the old text is not silently rewritten or duplicated into a fourth asset.
- The supplied LIVE_MODEL heading says v0.1 while the prompt/changelog describe retained v0.3 inside v0.4. No separate v0.3 file or workshop transcript is supplied to prove that label. The full delivered file is preserved; its earlier pre-upload statement is marked historical.
- Gravity/density, city coordinates, exact gateways, network mathematics and safe reconfiguration, detailed outlines, clock values, currency rates and detailed image provenance remain OPEN or missing as recorded. No mathematical proof, final map geometry or new canon is inferred by this import.

## Read-only external source checks

AERA main was observed at `6f71b068cba3bf7d851041084e7bb90700a0a751`. The following documents were read at that pinned commit; only references and audit conclusions are recorded here. No source documents were copied into this repository.

| Pinned source | Audit relevance |
|---|---|
| [AERA README](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/README.md) | Framework/source boundaries; implementations are author choices. |
| [World Clock](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/WORLD_CLOCK.md) | Confirms L0–L4 meaning and optional chronology ledgers. |
| [Framework index](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/FRAMEWORK_INDEX.md) | Confirms source and domain boundaries; not a full upstream-corpus audit. |
| [L1 overview](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/L1/README.md) | Relational Weaving remains a Transduction specialization. |
| [Lifecycle](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/L1/TRANSDUCTION_LIFECYCLE.md) | Confirms the retained six-stage order. |
| [Principal interfaces](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/L1/INTERFACES/00_READ_FIRST.md) | Confirms maege-glass and card basin exclusivity across interfaces. |
| [Sigils and velis](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/L2/SIGILS_ARCHITECTS_VELIS.md) | Confirms physical ru’ne/sigils versus direct field velis. |
| [Alchemy and vaen](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/L2/ALCHEMY_VAEN.md) | Confirms specialized resource meaning; cannot resolve BAEN. |
| [Vaelith crosswalk](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/L2/BIOLOGY/07_VAELITH_PROPHECY_CROSSWALK.md) | Supports optional denizen/prophecy correspondences; Garden/Gardens variation remains an upstream qualification. |
| [Rainbow Road](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/L0/RAINBOW_ROAD.md) | Confirms optional bridges and author-specific temporal correspondence. |

The five external repository references supplied by the package were accessible: AERA through the pinned reads above, and Mk-147, MK727, _bricked and MK163 through read-only GitHub metadata. Metadata reachability is not verification of their complete content, licensing or historical influence. MK163's map was not retrieved. Not every inherited claim or mathematical source was independently proven; the pinned checks above define the scope of source verification.

## Validation and reproduction

Run `python provenance/verify_import.py` from the repository with Python 3.10+ and Pillow installed. It checks the fixed project inventory and snapshot hashes; the original manifest; unchanged source files and append-only prefixes; ZIP hash, CRC and contents when locally available; strict UTF-8; three decoded images; 35 arc headings and statuses; clock/event integrity; protected terminology; ten coverage rows; current local Markdown links and the documented historical alias; and common credential/private-key patterns. The pattern scan is a bounded check, not a guarantee against every secret format.

Run `python provenance/verify_import.py --git-index` after staging to compare all staged blob bytes with the checked worktree. Run `python provenance/verify_import.py --commit HEAD` after committing to compare all committed blob bytes and paths. The verifier reports missing local ZIP availability explicitly for fresh clones and does not claim it rechecked an unavailable source archive. Integrity PASS does not turn incomplete stage records, image attribution or unvalidated map details into verified facts.

The import workflow also reviews `git status --short --branch`, `git diff --stat`, `git diff --cached --stat`, `git diff --cached --check`, ignored-inbox behavior and the origin URL before committing. Normal push uses main, without force. A concurrent remote history or conflicting path must be reconciled before publication; none existed at initial inspection. Successful push and the independently queried remote SHA are reported outside this pre-publication document.
