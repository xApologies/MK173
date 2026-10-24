# World Clock
Event ledger with stable IDs, relative chronology, White date, realm local time, provenance and status. No absolute dates or cross-realm time ratios yet. Update events and canon together; no invented dates. This is an organizational model, not a new physics law.

## Scope and current schema — import clarification

This directory is MK173's optional chronology scaffold. In [AERA's pinned definition](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/WORLD_CLOCK.md), the World Clock is the full L0–L4 framework. A chronological ledger does not replace that framework.

The supplied [event CSV](EVENTS.csv) has seven columns: stable event ID, book, arc, event, relative order, White date and status. It does **not yet have** realm-local-time or provenance columns despite the intended scope described above. Those fields, a calendar epoch and actual local times remain unprovided; this import preserves the original schema and adds no invented values. The final event's narrative relation is prose rather than a dependency on a stable event ID.

The [realm CSV](REALM_CLOCKS.csv) has seven realms. White's factor of 1 is the reference identity; the six chromatic factors are empty and OPEN. Neither currency conversions nor rates appear here. See [current decisions](../canon/DECISIONS.md) and the [audit](../provenance/IMPORT_AUDIT.md).
