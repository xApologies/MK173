# World Clock
Event ledger with stable IDs, relative chronology, White date, realm local time, provenance and status. No absolute dates or cross-realm time ratios yet. Update events and canon together; no invented dates. This is an organizational model, not a new physics law.

## Scope and current schema — import clarification

This directory is MK173's optional chronology scaffold. In [AERA's pinned definition](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/WORLD_CLOCK.md), the World Clock is the full L0–L4 framework. A chronological ledger does not replace that framework.

The supplied [event CSV](EVENTS.csv) has seven columns: stable event ID, book, arc, event, relative order, White date and status. It does **not yet have** realm-local-time or provenance columns despite the intended scope described above. Those fields, a calendar epoch and actual local times remain unprovided; this import preserves the original schema and adds no invented values. The final event's narrative relation is prose rather than a dependency on a stable event ID.

The [realm CSV](REALM_CLOCKS.csv) has seven realms. White's factor of 1 is the reference identity; the six chromatic factors are empty and OPEN. Neither currency conversions nor rates appear here. See [current decisions](../canon/DECISIONS.md) and the [audit](../provenance/IMPORT_AUDIT.md).

## v0.6 World Clock navigation — 2026-10-24

The full AERA L0–L4 meaning above remains authoritative. This directory now also holds MK173's L2 civilization records. The historical chronology description is retained; the additive [v2 schema](SCHEMA_V2.md), [v2 event ledger](EVENTS_V2.csv) and [v2 realm table](REALM_CLOCKS_V2.csv) remain unchanged. No chronology migration or new date/factor occurs in v0.6.

- [Adopted Valedran economic benchmarks](L2_WORLD_CIVILIZATION/ECONOMY/INHERITED_PRICE_REFERENCE.md).
- [Land, forestry, food and construction](L2_WORLD_CIVILIZATION/ECONOMY/LAND_FORESTRY_CONSTRUCTION.md).
- [Ships and trade](L2_WORLD_CIVILIZATION/TRANSPORT/SHIPS_AND_TRADE.md).
- [Source-bounded organizations](L2_WORLD_CIVILIZATION/SECURITY/ORGANIZATIONS.md) and [historical PDFs](../provenance/source_references/README.md).
- [WORKING leadership, treaties and seven-book route](L2_WORLD_CIVILIZATION/POLITICS/LEADERSHIP_WORKING.md): map labels are evidence of depicted names, not acceptance of the roster or travel distances.
- [Current workshop decisions](../canon/POST_V05_DECISIONS.md) and [v0.6 audit](../provenance/V06_IMPORT_AUDIT.md).

The accepted 180 ahm per eln is a Valedran currency conversion, not a realm-time correspondence or another realm's monetary ratio. Realm clock factors, epochs and offsets remain OPEN.

## Red Book Pass 1 narrative pointers — 2026-10-24

This date records repository integration, not an in-world event. The [Red Book index](../narrative/RED/README.md) links all five ACCEPTED major-beat summaries and the [book live model](../narrative/RED/LIVE_MODEL.md). Their relative order is Arc 01 → 02 → 03 → 04 → 05, followed by the proposed expansion of [Orange Arc 01, The Living Threshold](../narrative/ORANGE/ARCS.md); no Orange outline is created here.

Existing E0001/E0002 remain compatible opening-arc anchors; the later White E0003 is not moved into Red. All original and v2 event/realm CSVs remain byte-identical. No new event IDs, dates, durations, clock factors or schema migration are introduced. A fuller ledger and E0003's formal dependency remain OPEN.

The [decision note](../canon/DECISIONS.md) and [continuity audit](../provenance/RED_PASS1_IMPORT_AUDIT.md) distinguish this accepted narrative skeleton from detailed chapter planning, optional proposals and unresolved mechanics. Environmental storms/Domai/Eldris and municipal stabilization are not consequences or components of the ancient network merely because these stories share a setting.

## Orange Book Pass 1 narrative pointers — 2026-10-24

This is an integration date, not an in-world date. The [Orange index](../narrative/ORANGE/README.md) and [book live model](../narrative/ORANGE/LIVE_MODEL.md) add the accepted sequence Arc 01 → 02 → 03 → 04 → 05 after [Red's ending](../narrative/RED/ARC_05_SUMMARY.md), then the prospective [Yellow handoff](../narrative/YELLOW/ARCS.md). The earlier Red note remains a record of its own import; Orange now has its separate accepted skeleton.

Arc 01 supplies an approximate interval of several weeks after Red. No exact date, trial span, travel duration, realm-clock factor, new event ID or schema migration follows from that phrase. All four existing event/realm CSVs and all L2 civilization records remain byte-identical. E0001/E0002 remain opening Red anchors, and E0003 remains the later White working event. A fuller chronology ledger and its dependencies remain OPEN.

The route is Asterhold/White → Sunfall/White → Orange → Sunfall/White, with a prospective Dawnshore/White introduction for Yellow. Saelith's travel respects Orange/White access; she stays in Orange at book end. Seren's possible correspondence does not establish a dated event. The [decision note](../canon/DECISIONS.md) and [continuity audit](../provenance/ORANGE_PASS1_IMPORT_AUDIT.md) retain these scope limits and the full AERA L0–L4 meaning of World Clock.

## Yellow Book Pass 1 narrative pointers — 2026-10-24

This is an integration date, not an in-world date. The [Yellow index](../narrative/YELLOW/README.md) and [book model](../narrative/YELLOW/LIVE_MODEL.md) add Arc 01 → 02 → 03 → 04 → 05 following [Orange's ending](../narrative/ORANGE/ARC_05_SUMMARY.md), then the prospective [Green handoff](../narrative/GREEN/ARCS.md). Earlier Red/Orange notes retain their historical scope; Yellow now has a separate accepted skeleton.

The route is Sunfall/White → ocean crossing → Dawnshore/White → Yellow → Dawnshore/White, with a research lead toward Serenwood/White and Green. Orun returns to Yellow; no other chromatic travel is implied for him. Elarith appears through correspondence, not an Aren visit. The crossing is costly and immense, but no numerical fare, duration, distance, calendar date or clock factor is supplied.

All four original/v2 chronology CSVs and every L2 civilization record remain byte-identical. E0001/E0002 stay opening Red anchors and E0003 remains the later White working event. No new event ID, schema migration or inferred date is added; full chronology population and E0003's formal dependency remain OPEN. The [decision note](../canon/DECISIONS.md) and [audit](../provenance/YELLOW_PASS1_IMPORT_AUDIT.md) preserve these limits and AERA's full L0–L4 World Clock meaning.

## Green Book Pass 1 narrative pointers — 2026-10-24

This is an integration date, not an in-world date. The [Green index](../narrative/GREEN/README.md) and [book model](../narrative/GREEN/LIVE_MODEL.md) add Arc 01 → 02 → 03 → 04 → 05 after [Yellow's ending](../narrative/YELLOW/ARC_05_SUMMARY.md), then a prospective [Blue handoff](../narrative/BLUE/ARCS.md). Earlier Red/Orange/Yellow notes keep their historical scope.

The supplied route is Dawnshore/White → terrestrial Corridors → Serenwood/White → Green → Serenwood/White, with preparation for Azure League/Blue research. Iri first visits White and later stays in Green; no travel to another chromatic realm is implied. The White forest preserve and Green passage proposals are separate cases. The restricted historical experiment remains inactive; the Collective's authorized compromise is phased and monitored without supplied completion dates or long-term results.

All four original/v2 chronology CSVs and all L2 civilization records remain byte-identical. E0001/E0002 remain opening Red anchors and E0003 remains the later White working event. No new event IDs, dates, durations, clock factors or schema migration are introduced. Full ledger population and E0003's formal dependency remain OPEN. [Scoped decisions](../canon/DECISIONS.md) and [the audit](../provenance/GREEN_PASS1_IMPORT_AUDIT.md) retain AERA's L0–L4 World Clock meaning and the distinction between accepted causality and unspecified details.

## Blue Book Pass 1 narrative pointers — 2026-10-24

This is an integration date, not an in-world date. The [Blue index](../narrative/BLUE/README.md) and [book model](../narrative/BLUE/LIVE_MODEL.md) add Arc 01 → 02 → 03 → 04 → 05 after [Green's ending](../narrative/GREEN/ARC_05_SUMMARY.md), then the prospective [Violet handoff](../narrative/VIOLET/ARCS.md). Earlier book notes retain their historical scope.

The sequence is Serenwood/White → maritime travel to Azure League/White → Blue research → Azure-based cooperation and assessment using Elarith/selected White monitoring records. The Conservator and Seren travel to Azure in Arc 04. Individual movements during the later distributed assessment are unspecified. Vaelor visits Blue and White only; no Violet journey is inferred for him. Stormwall/Violet is the next research direction. “Centuries-old” infrastructure and an “extended” past disruption remain qualitative durations without dates or a fixed collapse deadline.

All four original/v2 chronology CSVs and every L2 civilization record remain byte-identical. E0001/E0002 remain opening Red anchors; E0003 stays the later White working event, not a Blue reconfiguration. No new event IDs, dates, clock factors, precise durations or schema migration are added. [Scoped decisions](../canon/DECISIONS.md) and [the audit](../provenance/BLUE_PASS1_IMPORT_AUDIT.md) preserve AERA's L0–L4 scope and distinguish narrative acceptance from unresolved details.

## Violet Book Pass 1 narrative pointers — 2026-10-24

This is an integration date, not an in-world date. The [Violet index](../narrative/VIOLET/README.md) and [book model](../narrative/VIOLET/LIVE_MODEL.md) add Arc 01 → 02 → 03 → 04 → 05 after [Blue's ending](../narrative/BLUE/ARC_05_SUMMARY.md), followed by the proposed [White/Elarith assembly](../narrative/WHITE/ARCS.md). Prior book notes retain their historical scope.

Aren's supplied sequence runs from Azure/White to Stormwall/White, then Violet research with Aelira, then a sixfold synthesis in Stormwall/White. Tharos, Saelith, Orun, Iri, Vaelor and Aelira can each visit White; the gathering does not take the other five natives into Violet. Elarith archive access is authorized without specifying each participant's itinerary. The later international assembly remains proposed, and no extra realm crossing is inferred from the Return to White beat title.

All four original/v2 chronology CSVs and every L2 civilization record remain byte-identical. E0001/E0002 stay opening Red anchors; E0003 remains the later White working event and is not performed in Violet. No new event IDs, dates, clock factors, travel durations or schema migration are introduced. [Scoped decisions](../canon/DECISIONS.md) and [the audit](../provenance/VIOLET_PASS1_IMPORT_AUDIT.md) retain AERA's L0–L4 scope, open chronology dependencies and the distinction between the accepted Stormwall meeting and White's still-unexpanded arc titles.

## White Pass 1 narrative references — 2026-10-25

The [White index](../narrative/WHITE/README.md) and [accepted book model](../narrative/WHITE/LIVE_MODEL.md) complete the seven-book Pass 1 outline imports. Relative progression is Stormwall/White → Elarith/White research accord and reunion → refusal and redesign → authorized bounded test → phased program authorization and certification → monitored regional stage → continuing work and Asterhold/Kaelmont homecoming. Six chromatic natives gather in White, preserving access restrictions.

Both event CSVs retain E0001, E0002 and E0003 byte-for-byte. E0003 remains the WORKING White 05 reconfiguration anchor with incomplete dependency; the new narrative distinguishes the first regional stage in White 04 from continuing phased work in White 05. It does not authorize a global permanent-repair reading or supply missing dates. Formal ledger expansion remains OPEN. Both realm-clock CSVs retain White factor 1 and six OPEN chromatic factors; no travel duration, signatory list or conversion ratio is inferred. L1/L2/L3 records remain unchanged. See [the scoped import audit](../provenance/WHITE_PASS1_IMPORT_AUDIT.md).
