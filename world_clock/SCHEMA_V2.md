# MK173 World Clock — additive v2 chronology schema
AERA's World Clock is the L0–L4 framework. This is a story-specific chronology ledger, not a new physics law.

`EVENTS_V2.csv` adds explicit predecessor, realm, realm-local time, location, source and notes fields. The existing `EVENTS.csv` is a preserved v0.4 import snapshot. `REALM_CLOCKS_V2.csv` records epoch/offset/provenance columns without inventing factors. White's factor 1 is a reference identity; six chromatic factors remain OPEN. Previously illustrative 0.8–1.3 values were never accepted.

New events require stable IDs and provenance; dates and factors stay empty until author-selected. Existing `provenance/verify_import.py` is a v0.4 import-snapshot validator, NOT a v0.5 whole-repository validator. Preserve the old SHA256 snapshot manifests; create a separate v0.5 delta manifest. Future replacement of original CSVs must be a separately audited migration.
