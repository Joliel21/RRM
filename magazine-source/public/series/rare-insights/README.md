# RARE INSIGHTS canonical source

This directory is the canonical structured-data layer for the RARE INSIGHTS magazine section.

## Current approved structure

RARE INSIGHTS contains **16 approved title/divider entries total**:

- 1 main RARE INSIGHTS divider spread
- 15 individual RARE INSIGHTS series

Travel Series is part of the approved structure and must remain after Sunday Sessions and before Turning the Tide for Rare Disease.

## Files

- `manifest.json` — ordered list of the 16 approved RARE INSIGHTS divider/title entries and their authoritative artwork paths.
- `schema.json` — metadata fields and integrity rules for future article inventories.
- `<series>/articles.json` — future canonical article inventory for that series. These files are not considered complete until created and verified during the metadata migration step.
- `<series>/images/` — optional canonical destination for verified article images when they are migrated into this content layer.

## Source-of-truth split

- `Joliel21/RRM/main` is authoritative for RARE INSIGHTS artwork, asset paths, and canonical structured content.
- `Joliel21/RRM-Runnable/main` is the runnable React/Vite reader and should consume this canonical data rather than becoming the long-term article database.

## Metadata integrity rules

- Do not invent missing titles, authors, dates, URLs, or images.
- Missing values remain `null` until verified.
- Use exact published article titles, bylines, dates, URLs, and article imagery when verified.
- `metadataStatus` records whether a record is `complete`, `partial`, or `pending-migration`.
- Artwork filenames and paths must match current `Joliel21/RRM/main` exactly.

## Interaction rule

Title-page artwork remains static. Clickable behavior belongs in the magazine HTML/editorial hotspot layer, not in newly created clickable SVG artwork.

## Migration status

Step 4 establishes the canonical structure only. Article inventories and article-level metadata are handled in the next metadata migration step. No article metadata should be described as migrated until it has actually been verified and written to the appropriate series inventory.
