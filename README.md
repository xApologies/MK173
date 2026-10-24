# MK173 — The Geometry of Existence

Independent AERA story and visual atlas, imported from the user-supplied v0.4 handoff on 2026-10-24. Repository: [xApologies/MK173](https://github.com/xApologies/MK173).

- [Retained live model and navigation](LIVE_MODEL.md): the complete supplied text, followed by import notes.
- [Accepted decisions, working proposals and open questions](canon/DECISIONS.md), [world and story](canon/WORLD_AND_STORY.md), and [AERA inheritance](canon/AERA_INHERITANCE.md).
- [Chronology scaffolding](world_clock/README.md), [realm factors](world_clock/REALM_CLOCKS.csv), and [event ledger](world_clock/EVENTS.csv).
- Working arcs: [Red](narrative/RED/ARCS.md), [Orange](narrative/ORANGE/ARCS.md), [Yellow](narrative/YELLOW/ARCS.md), [Green](narrative/GREEN/ARCS.md), [Blue](narrative/BLUE/ARCS.md), [Violet](narrative/VIOLET/ARCS.md), [White](narrative/WHITE/ARCS.md).
- [Three visual references and their qualifications](images/INDEX.md).
- [Import audit, stage coverage and provenance gaps](provenance/IMPORT_AUDIT.md), [original manifest](provenance/SHA256.json), [import snapshot manifest](provenance/IMPORT_SHA256.json), [changelog](provenance/CHANGELOG.md), and [original import instructions](CODEX_PROMPT.md).

Run `python provenance/verify_import.py` with Python 3.10+ and Pillow to verify the import snapshot. Add `--git-index` to verify staged bytes, or `--commit HEAD` to verify committed bytes. If the original ZIP remains in `_inbox`, it is checked too; a fresh clone reports its absence explicitly. The manifests describe this import snapshot and must be deliberately revised when the project changes.

The handoff preserves Development 01–07 individually and 08–10 as a combined summary; the original stage boundaries for 08–10 are missing. The maps are concepts: their scale bars, political boundaries and generated labels are not validated measurements or new canon. Realm clock factors and currency conversions remain OPEN.

Framework source: [AERA](https://github.com/xApologies/AERA). Related references: [_bricked](https://github.com/xApologies/_bricked), [Mk-147](https://github.com/xApologies/Mk-147), [MK727](https://github.com/xApologies/MK727). [MK163](https://github.com/xApologies/MK163) remains a separate novel. No external repository corpus is imported here. No new license or image authorship claim is assigned by this import.

## Current v0.5 continuity update — 2026-10-24

The v0.4 description above is retained as history. **Stages 08–10 now have individual records, and BAEN is corrected to vaen in active canon.** The earlier stage-coverage and terminology gaps are superseded by these supplied records:

- [08 — Economy and Daily Life](canon/08_ECONOMY_AND_DAILY_LIFE.md), [09 — Environmental Geography](canon/09_ENVIRONMENTAL_GEOGRAPHY.md), [10 — Narrative Constitution](canon/10_NARRATIVE_CONSTITUTION.md), and [terminology correction](canon/TERMINOLOGY_CORRECTION.md).
- [Political map v02](images/maps/political_v02_corrected.png) and [limited correction scope](images/maps/political_v02_README.md). The three original images are preserved; the visual collection now has four images.
- [Chronology v2 schema](world_clock/SCHEMA_V2.md), [events v2](world_clock/EVENTS_V2.csv), and [realm clocks v2](world_clock/REALM_CLOCKS_V2.csv). Original CSVs remain unchanged.
- [Update audit and remaining issues](provenance/V05_UPDATE_AUDIT.md), [v0.5 hashes](provenance/V05_UPDATE_SHA256.json), [supplied delta notes](provenance/DELTA_V05_NOTES.md), and [v0.5 verifier](provenance/verify_v05_update.py).

For the current snapshot, run `python provenance/verify_v05_update.py` with Python 3.10+ and Pillow. Use `--git-index` for staged bytes or `--commit HEAD` for committed bytes. The old verifier and manifests are unchanged historical v0.4 evidence: the old verifier requires the original v0.4 checkout and is expected to reject the expanded v0.5 working tree. Do not regenerate the old manifests to make it pass. The new verifier checks the preserved base and this update separately. Unknown clock factors, dates, exchange rates, surveyed map data and network mathematics remain OPEN.

## Current v0.6 civilization checkpoint — 2026-10-24

Earlier version descriptions remain historical. [The new decisions](canon/POST_V05_DECISIONS.md) accept Valedran's **180 ahm = 1 eln**, its specified denominations and adopted economic benchmarks. The six realms' trade-currency architecture is accepted; labels, denominations and exchange rates remain separately WORKING/OPEN. See [current decision precedence](canon/DECISIONS.md) and [economic supersessions](canon/08_ECONOMY_AND_DAILY_LIFE.md).

- [World Clock civilization index](world_clock/README.md): economy, land/materials, ships, security and working politics.
- [WORKING leadership and routes](world_clock/L2_WORLD_CIVILIZATION/POLITICS/LEADERSHIP_WORKING.md) alongside the unchanged [political map](images/maps/political_v02_corrected.png).
- [Historical PDFs and source boundaries](provenance/source_references/README.md), [supplied delta overview](README_DELTA.md), and [archived update instructions](CODEX_UPDATE_PROMPT.md).
- [Continuity audit and unresolved issues](provenance/V06_IMPORT_AUDIT.md), [supplied payload hashes](provenance/V06_PAYLOAD_SHA256.json), [v0.6 snapshot hashes](provenance/V06_SNAPSHOT_SHA256.json), and [v0.6 verifier](provenance/verify_v06_update.py).

Run `python provenance/verify_v06_update.py` with Python 3.10+, Pillow and pypdf; use `--git-index` or `--commit HEAD` for staged/committed bytes. The v0.4/v0.5 verifiers and manifests remain unchanged evidence for their original checkouts and are not current-tree validators. The v0.6 verifier checks the preserved v0.5 base and this update separately. Historical PDF instructions and canon-lock wording do not govern MK173. Original canon text, images, event/realm CSVs, source pointers and Git ancestry are preserved.
