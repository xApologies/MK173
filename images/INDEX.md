# Visual provenance
`maps/geography_v01.png`: original MK173 geography illustration, NOT validated scale. `maps/political_v01.png`: political overlay, illustrative boundaries/names only. `references/nonordinary_geometry.jpeg`: user-supplied nonordinary realm geometry reference, NOT White map. The supplied MK163 map is not copied into this independent story. Written decisions override incidental image labels.

## Import verification — 2026-10-24

| Asset | Decoded format and size | Provenance qualification |
|---|---|---|
| [Geography concept](maps/geography_v01.png) | PNG, 1774 × 887 | Handoff identifies original AI-generated MK173 workshop art; generation record and source prompt not supplied. |
| [Political concept](maps/political_v01.png) | PNG, 1774 × 887 | Handoff identifies a political overlay; generator/editor history not supplied. |
| [Nonordinary geometry reference](references/nonordinary_geometry.jpeg) | JPEG, 1320 × 1012 | Handoff identifies a user-supplied reference; original creator, source URL and license not supplied. |

All three decoded successfully and were visually inspected. Their original bytes and source SHA256 values are unchanged. See the [import audit](../provenance/IMPORT_AUDIT.md) and [original manifest](../provenance/SHA256.json). These checks establish integrity from the supplied archive, not independent authorship or licensing.

The political map's printed 80,000-mile **diameter** conflicts with the written approximately 80,000-mile **circumference**. Its Earth comparison, scale bar, capital marker and note treating major features as canon are unratified image annotations. Written decisions govern. The geography map's scale and legend also remain illustrative. Neither map places chromatic realms on the White planet or determines travel times.

The retained live model's older geography filename is a historical alias for the geography concept linked here. The nonordinary reference is a visual direction, not a proven realm geometry or White-world map.

## v0.5 derived political map — 2026-10-24

[Political concept v02](maps/political_v02_corrected.png) is the user-supplied, narrowly annotated derivative of the retained [v01](maps/political_v01.png). It is a 1774 × 887 PNG with SHA256 `386327ddbb8d26aae4a4d9560932242e168010c10d635955b8cd6c2812da2229`. Its top-left annotation now reads approximately 80,000-mile **circumference** and approximately 3.2 Earth circumferences; see the [supplied derivative note](maps/political_v02_README.md).

Full decoding and pixel comparison found 7,345 changed pixels, confined to the rectangle x=11–185, y=120–161 (zero-based coordinates). Every decoded RGB pixel outside that annotation is identical to v01. This verifies the narrow visual scope, not the derivative's editing software or original authorship. All three original image files remain byte-identical.

The correction does not validate the scale bar, political borders, government names, capitals, coordinates, projection or legend's canon claims. Both versions remain concept art subordinate to written decisions. Original image provenance gaps remain recorded in the [v0.5 audit](../provenance/V05_UPDATE_AUDIT.md); no new licensing claim is made.
