# RARE INSIGHTS source of truth

This directory is the canonical content index for the RARE INSIGHTS magazine section.

## Structure

- `manifest.json` — ordered list of RARE INSIGHTS series and title-page assets.
- `schema.json` — article metadata rules.
- `<series>/articles.json` — article inventory for that series.
- `<series>/images/` — destination for article images as they are migrated into the canonical structure.

## Migration status

The initial data was migrated from `RRM_NPM_SOURCE_1.0.29` without inventing missing metadata. A `null` author/date is intentional and means the current reader source did not contain that value. Titles marked `derived-from-url-slug-existing-reader-behavior` reproduce the existing reader's title-generation behavior and should be replaced with the exact published title when verified.

News & Press Releases currently points to the existing `press-releases/manifest.csv`; its full inventory should be migrated into its `articles.json` in a later metadata pass.

## Publishing rule

For future RARE INSIGHTS additions, update the matching `articles.json` first. The reader should consume this content layer rather than hard-coding article inventories in React.
