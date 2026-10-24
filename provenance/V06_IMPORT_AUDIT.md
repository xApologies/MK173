# MK173 v0.6 incremental import audit — 2026-10-24

## Result, authority and scope

The live-model delta is integrated at `C:\Users\rando\_MK173` on `main`, origin `https://github.com/xApologies/MK173.git`. Local HEAD, fetched origin/main and independently queried remote main initially agreed on `d921703d0f0724fce98ebea2d667899e000e2df3`. The worktree was clean. The v0.5 verifier passed against all 40 files and committed bytes before mutation. No divergent history, user edits or conflicting destination paths were present.

The user's request authorizes this incremental import, audit, commit and normal push. Instructions inside the ZIP were reviewed as task material within that authorization. They do not override preservation requirements or authorize modifying AERA/MK163. Historical PDFs' canon-lock language is evidence about a different setting, not an agent instruction or current MK173 rule. No scripts supplied by the archive were executed; it contains documents and PDFs only.

Current snapshot: **56 files**. All 40 base paths remain: **34 byte-identical and six append-only**. Sixteen new paths comprise all twelve archive entries plus this audit, a new snapshot manifest/verifier and a historical-source README. Total changed paths: **22**, with no deletion or rename. All four original images, four chronology CSVs, seven arc files, earlier manifests/verifiers/audits, Development 09/10 and AERA inheritance remain byte-identical. Full prior contents of the six edited files remain exact prefixes. No narrative chapters were drafted.

This audit is pre-publication content. Its containing commit supplies the new SHA; it cannot embed its own final hash. Remote publication is confirmed separately after normal push by comparing live remote main with local HEAD. No force-push, reset or history rewrite is used.

## Archive integrity and inventory

Archive `MK173_live_model_delta_v0_6.zip`: **119,752 bytes**, SHA256 `5b6cf7db875bf798245903a6118cae9a74dea044f4d21949e81d38f484b15111`. Its twelve entries total **178,845 uncompressed bytes**, comprising nine strict UTF-8 text files and three PDFs. CRC passes. All eleven size/hash entries in the [supplied payload manifest](V06_PAYLOAD_SHA256.json) match. The supplied manifest omits itself; the new [snapshot manifest](V06_SNAPSHOT_SHA256.json) records its hash as well as all twelve archive entries.

Path checks rejected absolute paths, traversal, alternate data streams, Windows reserved names, invalid/control characters, trailing dots/spaces, case collisions, symlinks/nonregular entries and encrypted ZIP entries. Limits were 25 MB per entry and 50 MB total. None of these problems was found. Extraction used a new ignored `_inbox` staging directory; all destinations were checked absent, all staged bytes compared, and parent paths checked before copying. No nested Git metadata or ZIP wrapper directory was imported. The original ZIPs, extracted sources, PDF text and render previews remain ignored under `_inbox`.

The first PDF-text display encountered a Windows console encoding error for a ligature before any repository copy. Switching stdout to UTF-8 allowed complete review; the staged bytes were rechecked and the sources remained unchanged. This was a console-display issue, not damaged input.

**Prompt count discrepancy:** step 4 says seven new canon/civilization files. The actual archive contains five L2 documents plus one canon document, six in total, together with the overview, prompt, manifest and three PDFs. Every manifest-listed file is present and imported. No unnamed seventh domain document was invented.

The new manifest hashes the other **55 current files**, excluding itself to avoid a circular hash; Git covers all 56. It separately records 40 base hashes, six modified paths, sixteen added paths, the twelve exact imported paths and PDF page counts. Old manifests are unchanged.

## Changed paths

Append-only existing paths:

| Path | Addition |
|---|---|
| [LIVE_MODEL.md](../LIVE_MODEL.md) | Dated v0.6 scope, supersessions and navigation. |
| [README.md](../README.md) | Current indexes, source boundaries and version-specific verifier instructions. |
| [canon/DECISIONS.md](../canon/DECISIONS.md) | Explicit accepted currency/benchmark supersessions, accepted realm architecture and working/open limits. |
| [canon/08_ECONOMY_AND_DAILY_LIFE.md](../canon/08_ECONOMY_AND_DAILY_LIFE.md) | Closes only identified conversion/benchmark questions and preserves remaining personal/market unknowns. |
| [world_clock/README.md](../world_clock/README.md) | L2 civilization and existing chronology v2 navigation without modifying CSVs. |
| [provenance/CHANGELOG.md](CHANGELOG.md) | Dated v0.6 integration record. |

All twelve archive paths are new and byte-identical to the payload:

1. [CODEX_UPDATE_PROMPT.md](../CODEX_UPDATE_PROMPT.md)
2. [README_DELTA.md](../README_DELTA.md)
3. [canon/POST_V05_DECISIONS.md](../canon/POST_V05_DECISIONS.md)
4. [provenance/V06_PAYLOAD_SHA256.json](V06_PAYLOAD_SHA256.json)
5. [provenance/source_references/43_Bandits.pdf](source_references/43_Bandits.pdf)
6. [provenance/source_references/44_Cartels.pdf](source_references/44_Cartels.pdf)
7. [provenance/source_references/46_Evil_Organizations.pdf](source_references/46_Evil_Organizations.pdf)
8. [ECONOMY/INHERITED_PRICE_REFERENCE.md](../world_clock/L2_WORLD_CIVILIZATION/ECONOMY/INHERITED_PRICE_REFERENCE.md)
9. [ECONOMY/LAND_FORESTRY_CONSTRUCTION.md](../world_clock/L2_WORLD_CIVILIZATION/ECONOMY/LAND_FORESTRY_CONSTRUCTION.md)
10. [POLITICS/LEADERSHIP_WORKING.md](../world_clock/L2_WORLD_CIVILIZATION/POLITICS/LEADERSHIP_WORKING.md)
11. [SECURITY/ORGANIZATIONS.md](../world_clock/L2_WORLD_CIVILIZATION/SECURITY/ORGANIZATIONS.md)
12. [TRANSPORT/SHIPS_AND_TRADE.md](../world_clock/L2_WORLD_CIVILIZATION/TRANSPORT/SHIPS_AND_TRADE.md)

The final five paths above are under `world_clock/L2_WORLD_CIVILIZATION/`. Four implementation artifacts are added: this audit, [V06_SNAPSHOT_SHA256.json](V06_SNAPSHOT_SHA256.json), [verify_v06_update.py](verify_v06_update.py) and [source_references/README.md](source_references/README.md). The earlier root CODEX_PROMPT remains unchanged; the new update prompt is a distinct archived document.

## Continuity findings and explicit supersessions

**Valedran currency:** the prior OPEN conversion is now ACCEPTED as **180 ahm = 1 eln**. The ordinary ahm and ordinary eln series each have six denominations, 1/6/12/18/24/30, corresponding to Red through Violet. White eln notes are 180/360/540/720/900/1080; there is no White ahm coin. Coin diamond is not automatically a charged Genesis Diamond chip. The retained earlier OPEN statements are superseded explicitly by dated additions, not silently deleted.

**Economic scope:** adopted schedules now provide individual monthly incomes, average residential rents, card-class benchmarks, crystal prices per kilogram and selected physical equipment prices for Valedran. They are not household income, universal price caps, Aren's purchases, dust/vaen/charged-chip prices or a calendar. The exact schedules match the pinned upstream sources below. MK163's eleven-month annualization, personal leases/contracts, chronology, geography, royal-house names and other story details are not imported.

**Realm currencies:** one broadly accepted trade currency per chromatic realm, alongside possible local sovereign currencies, is accepted architecture. It is not one Starscape cash currency. Names Talon/Vela/Orin/Lira/Tide/Astra remain working proposals (including singular forms replacing earlier plural proposal variants); denominations, exchange rates and 180:1 assumptions for other realms remain unaccepted. The old Exchange Weight proposal is not ratified.

**Civilization and profession:** supplied accepted directions preserve independent civic stabilization and the distinction from the ancient network; protected estates, managed timber, premium meat, grown Type 1 stone and specialist Type 2–5 alchemy fit the existing preindustrial model. Material growth does not establish industrial shipyards. Ships are timber, sail-free and propelled by hull-integrated water-flow sigils; dimensions, speed and physical implementation remain OPEN. Aren's professional cartography and general relational Weaving do not confer professional cardsmith manufacture.

**Geography/narrative compatibility:** Development 09 and 10 were read and left unchanged. The accepted approximately 80,000-mile circumference, 20,000–30,000-foot mountains, White superposition, six nonordinary chromatic realms and asymmetric travel remain. No PDF's 60,000-mile setting replaces them. Seven books and all 35 existing working arc titles are unchanged; no chapters or required villain/cabal are created. The proposed route has the same book-color order but does not establish distance, time or obligatory plot.

**Terminology:** active resource usage remains vaen. The literal BAEN retained in the payload's protected-name bullet is correction context only; previous correction provenance and historical records remain intact. Vaelith, velis, ru’ne, maege, maegi and abecca are preserved. No new BAEN resource is created. The historical geography filename and old live-model version labels remain qualified history.

## Political-map comparison — labels only

Compared the supplied registry with unchanged [political v02](../images/maps/political_v02_corrected.png), using the retained geography map's continental naming. Each of the eight roster territories is depicted; the additional Thalorin correction is also supported by a visible label. This confirms spelling/depiction, not accepted statehood, borders, governance, rulers, ages, treaties or book routes.

| Proposed registry location | Observed artwork label/location | Qualification |
|---|---|---|
| Valedran Concord | Valedran Concord, Aerdan | Existing constitutional aristocracy and civic council remain; proposed federal leadership is not ratified. |
| Elarith Republic | Elarith Republic, Tyranor | President, ministers and Conservator headquarters remain WORKING. |
| Sunfall Republic | Sunfall Republic, Aerdan | Leadership and Orange-book route remain WORKING. |
| Dawnshore Principalities | Dawnshore Principalities, Tyranor | Ruling family, institutions and Yellow route remain WORKING. |
| Serenwood Commonwealth | Serenwood Commonwealth, Tyranor | Officers, parliamentary form and Green route remain WORKING. |
| Azure League | Azure League, Sylvaris | Officers and Blue maritime route remain WORKING. |
| Stormwall Kingdom | Stormwall Kingdom, Tyranor | Dynasty, constitutional form and Violet route remain WORKING. |
| Kaelmont Heights | Kaelmont Heights, Aerdan | Warden and frontier authority remain WORKING. |
| Thalorin | Thalorin Kingdom, Aerdan | House Vaelmont remains proposed; Halverin is not established by the inspected map. |

The Continuity Directorate roster, treaties and Elarith seat are explicitly WORKING. Matching a map label does not promote any of them. Scale bars, capital markers, projection, political boundaries and the four-continent/archipelago versus five-continent question retain earlier qualifications.

## PDF readability and provenance boundaries

| Historical PDF | Pages | SHA256 |
|---|---:|---|
| 43_Bandits | 4 | `37646717e91963bfb7143fae83ea4aaf06615d837bb41454c05131e7fed87588` |
| 44_Cartels | 5 | `67f3d1b6d1134eb987c90d2551ce469154eb6452d73d1cddf51ff9b75549cd8f` |
| 46_Evil_Organizations | 4 | `3886c0630650fb8b1232cb696e6405ae548222e64a7e1451914dc29968ae9ece` |

All three parse strictly with pypdf, are unencrypted and yield text on every page. Poppler rendered all thirteen pages; visual inspection found readable source layouts, including the Cartels document's sparse fifth end-marker page. Text extraction has some ligature/spacing artifacts, so layout review used rendered pages. The PDFs were not edited or regenerated. No root OpenAction, JavaScript name tree or embedded-file name tree was found in the bounded inspection; this is not a general PDF security certification.

Metadata identifies Pages/Quartz, generic title Blank 195 and creation/modification dates on 2026-01-17. These are embedded metadata claims, not independent proof of authorship, dates or rights. The user-supplied bytes and manifest establish this import's chain of custody, not an upstream publication URL or license.

The source security descriptions support only the supplied bounded adaptation. Sanctuary discs/rings/cubes, the old six-kingdom/eleven-cartel counts, fixed Pirate King/hubs, old planet/sea distances and specific drug/slave-market plot are not current MK173 facts. The PDF's elemental warfare vocabulary does not replace AERA classifications. The added source README makes that boundary explicit. No original PDF content is duplicated into operative canon beyond the supplied scoped summaries.

## Read-only upstream verification

MK163 main was observed at **f2be3e917321c0fe0efbb6e37f30c0948e7f84fa**. The following source files were fetched at that commit for comparison; their contents were not copied into this repository. All numerical schedules adopted in the payload agree with these sources, within the stated scope.

| Pinned MK163 source | Checked values/scope |
|---|---|
| [Individual incomes](https://github.com/xApologies/MK163/blob/f2be3e917321c0fe0efbb6e37f30c0948e7f84fa/WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/CHROMATIC_INDIVIDUAL_INCOME_SCALE.md) | Red–Violet 100/200/400/1200/3000/5000 eln per month; no annual calendar imported. |
| [Rental averages](https://github.com/xApologies/MK163/blob/f2be3e917321c0fe0efbb6e37f30c0948e7f84fa/WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/CHROMATIC_RENTAL_AVERAGES.md) | 50/90/175/600/1400/3750; average rents only, no character lease. |
| [Currency and commodities](https://github.com/xApologies/MK163/blob/f2be3e917321c0fe0efbb6e37f30c0948e7f84fa/WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/CURRENCY_AND_COMMODITY_EXCHANGE.md) | 180:1, ordinary six denominations, White note series and coin material pairings; no royal-house/story adoption. |
| [Card classes](https://github.com/xApologies/MK163/blob/f2be3e917321c0fe0efbb6e37f30c0948e7f84fa/WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/GENESIS_CARD_CLASS_PRICES.md) | 100/230/540/1300/3100 eln benchmarks, not each catalogue item's price. |
| [Crystals](https://github.com/xApologies/MK163/blob/f2be3e917321c0fe0efbb6e37f30c0948e7f84fa/WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md) | 200/350/600/1100/2300/5000/31000 eln/kg; crystals only. |
| [Weapons](https://github.com/xApologies/MK163/blob/f2be3e917321c0fe0efbb6e37f30c0948e7f84fa/WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/MELEE_WEAPON_BASE_PRICES.md) | 35/30/20 ordinary and 165 massive physical construction; enhancements separate. |
| [Armor](https://github.com/xApologies/MK163/blob/f2be3e917321c0fe0efbb6e37f30c0948e7f84fa/WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/ARMOR_AND_CHAINMAIL_PRICES.md) | 50/110/180 leather, 200 standard shirt; no personal commission or story duration. |
| [Agriculture](https://github.com/xApologies/MK163/blob/f2be3e917321c0fe0efbb6e37f30c0948e7f84fa/WORLD_CLOCK/L2_WORLD_CIVILIZATION/AGRICULTURE/FOOD_PRODUCTION.md) | 17 slices × 13 crop positions, nutrients/velis and plant-based economy; no invented 221-name list or named ruler. |

The existing [AERA alchemy source](https://github.com/xApologies/AERA/blob/6f71b068cba3bf7d851041084e7bb90700a0a751/L2/ALCHEMY_VAEN.md) was read at the already recorded commit for Type 1–5 and vaen boundaries. All previous AERA URLs are preserved. These are targeted source checks, not a full upstream physics audit. AERA and MK163 were accessed read-only; neither local directories nor remote content were mutated.

## Validation and reproduction

Run `python provenance/verify_v06_update.py` with Python 3.10+, Pillow and pypdf. The verifier checks the current hash inventory, base Git blobs and preserved v0.5 snapshot, all twelve exact payload files, the source manifest, ZIP integrity when available, strict UTF-8, local Markdown links, six append-only prefixes, 35 unchanged arc headings, unchanged images and chronology, accepted correction scope, working political status, readable PDFs and common credential/private-key patterns. ZIP absence is reported, not mistaken for archive verification. The pattern scan does not guarantee detection of every possible secret format.

Use `--git-index` before committing or `--commit HEAD` after committing to compare every Git path and blob byte with the verified worktree; the commit check also requires the base as ancestor. The original v0.4/v0.5 scripts and manifests remain unchanged and require their original checkouts. They are not presented as v0.6 validators. Source previews/text and preflight reports are local ignored artifacts, not part of the commit.

The workflow reviews status, text diff, staged statistics, whitespace, exact path scope, absence of deletions/renames, correct remote/branch and current remote history. All preserved prefix/file assertions and imported hashes must pass before publication. Local Markdown links are checked; the already-qualified historical geography alias is retained. The user-facing final result independently reports the remote SHA after normal push.

Content verification passed: 56 project files, 55 snapshot hashes, 34 unchanged base files, six append-only base files, sixteen additions, twelve exact payload imports, 49 strict UTF-8 files, four unchanged decoded images, three readable PDFs totaling thirteen pages, 35 unchanged arc headings, seven rows per realm table and 193 resolving local Markdown links. Archive, bounded secret-pattern and whitespace checks also passed. Exact staged/committed bytes are checked before push; remote equality is checked afterward.

## Remaining OPEN / WORKING matters

- Aren's exact salary, apartment district/lease, favorite abecca and personal purchases; meals, fees, taxes, other trade prices, currency backing, Dust/vaen/charged-chip values and settlement institutions. Adopted benchmark schedules do not close these.
- Other realm currency names remain WORKING; denominations, monetary ratios and foreign exchange remain OPEN. No single Starscape cash system is adopted.
- Leaders, ages, dynasties, noble houses, political structures beyond established choices, treaties, routes, Continuity Directorate roles and Elarith headquarters remain WORKING. No Pirate King or old sanctuary infrastructure is accepted.
- Ship classes, dimensions, speeds, power/flow mechanics, ports and exact routes/travel durations remain OPEN. Detailed crop catalogue, recipes/effects, forestry/livestock quantities and industrial fabrication capabilities are not invented.
- Six realm clock factors, epochs/offsets, dates and event population remain OPEN; E0003 still lacks a formal predecessor. All four chronology CSVs remain unchanged.
- Surveyed projection, scale, coordinates, distances, gravity/climate/orbital details, gateways, continental taxonomy and realm geometry remain unresolved. Safe network transition mathematics and detailed chapter/scene plans remain OPEN.
- Original image/PDF authorship, source history and reuse terms are not established by hashes or generic metadata. Raw workshop transcripts and the earlier version-label discrepancy remain provenance qualifications. The supplied prompt's seven-versus-six domain-file count is recorded; no listed payload file is missing.
