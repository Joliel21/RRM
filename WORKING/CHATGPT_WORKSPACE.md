# ChatGPT Working Workspace

Temporary persistent workspace for active RRM work performed through ChatGPT.

## Rules
- Work here on the `chatgpt-work` branch, not `main`.
- Store temporary notes, manifests, page maps, generated text/config files, and work-in-progress references here.
- When a file is approved, move/copy the finalized version into its proper repository location and merge the intended changes into `main`.
- Do not treat files in this folder as production-ready unless explicitly marked approved.
- Binary/source packages can be stored elsewhere on this branch when needed; this file serves as the persistent index/checkpoint.

## Current RRM page-map decisions
- Cover: use page 1 of the HAR magazine as the cover.
  - Verified directly from attached `full-RRM.har` on 2026-08-23.
  - HAR page-image URL: `https://pages.pagesuite.com/5/9/592aa374-340b-4d09-9cc8-9e8c635a4f55/largepage.jpg`
  - Image dimensions: 1161 x 1648 px.
  - SHA-256 of the HAR-embedded JPEG: `48ce4021d1670fa685456ec111783e67b597f410fe9b05121b477d236b018766`.
  - Visual identity: Summer 2026, Issue No. 036, RARE Revolution Magazine cover featuring the RARE skin / RARE Inspiration cover artwork.
- Inside cover: leave blank for now.
- Printed page 1: leave blank for now.
- Pages 2–87: match the HAR magazine pages; currently considered correct.
- Pages 88–89: currently correct.
- Pages 90–91: two-page spread using `series-cover/explore_more.png`.
- Pages 96–97: two-page spread using `series-cover/insights.png`.
- Pages 112–113: two-page RARE Revolutionaries / Rare Youth spread using `series-cover/rare-youth.png`.
- Pages 138–141: community pictures from the repository `community/` collection; current reader paths need reconciliation.
- Page 197: leave as-is until its intended content is identified.
- Pages 198–199: insert two-page Resources spread using `series-cover/resources.png`.
- Existing content from page 198 onward shifts forward two pages after inserting the Resources spread.
- Page 205: replace the existing page with `series-cover/References.png`.
- Back cover: use exact page 88 from the attached `full-RRM.har`.
  - Verified from the HAR flatplan on 2026-08-23.
  - HAR page number: 88.
  - HAR page GUID: `b92d3c82-c4b2-4e6b-9d1a-8cd7fa264065`.
  - HAR page-image URL: `https://pages.pagesuite.com/b/9/b92d3c82-c4b2-4e6b-9d1a-8cd7fa264065/page.jpg`.
  - HAR PDF URL: `https://pages.pagesuite.com/b/9/b92d3c82-c4b2-4e6b-9d1a-8cd7fa264065/page.pdf`.

## Runnable package QA
- `RRM_RUNNABLE_1.0.5.zip` was reported as failing to start from PowerShell on Windows.
- `RRM_RUNNABLE_1.0.6.zip` corrected the Windows launcher, but visual review showed the approved front and back cover assets still were not rendered because the runnable source continued to use stale legacy/manifest cover paths.
- Root cause confirmed on 2026-08-23: the exact HAR cover assets existed in GitHub, but the runnable source was not wired to them.
- `RRM_RUNNABLE_1.0.7.zip` corrects the cover wiring:
  - closed front cover uses the exact GitHub HAR page-1 asset;
  - intro/first-open cover uses the exact GitHub HAR page-1 asset;
  - closed back cover uses the exact GitHub HAR page-88 asset;
  - stale reader-manifest cover paths no longer override the approved cover artwork.
  - ZIP integrity verified with `unzip -t`.
  - SHA-256: `d6c68341bc34f1b3ae371f1fef2bc0196c95a71826d38b9c595916977139ead8`.
- Full dependency installation/build could not be completed in the current execution environment; do not mark the Vite build itself verified until a clean install/build succeeds.

## Purpose
This branch is the persistent handoff location when the execution container is temporary or unavailable between turns.

## Connector verification
- 2026-08-23: GitHub read/write access verified from ChatGPT on the `chatgpt-work` branch.
