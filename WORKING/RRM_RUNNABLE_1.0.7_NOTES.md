# RRM Runnable 1.0.7

Correction after Windows visual review of 1.0.6.

## Cover wiring fix

The exact approved HAR cover files already exist on `chatgpt-work`:

- Front cover: `magazine-source/public/covers/rrm-front-cover-har-page-1.jpg`
- Back cover: `magazine-source/public/covers/rrm-back-cover-har-page-88.jpg`

The runnable source had not actually been wired to those files. Version 1.0.7 corrects that by forcing the closed front cover, intro/first-open cover, and closed back cover to use the approved GitHub cover assets instead of stale legacy/manifest cover paths.

Direct runtime assets used by 1.0.7:

- `https://raw.githubusercontent.com/Joliel21/RRM/chatgpt-work/magazine-source/public/covers/rrm-front-cover-har-page-1.jpg`
- `https://raw.githubusercontent.com/Joliel21/RRM/chatgpt-work/magazine-source/public/covers/rrm-back-cover-har-page-88.jpg`

## Package QA

- Package: `RRM_RUNNABLE_1.0.7.zip`
- ZIP integrity: passed (`unzip -t`)
- SHA-256: `d6c68341bc34f1b3ae371f1fef2bc0196c95a71826d38b9c595916977139ead8`
- Full npm dependency install/build remains unverified in the current execution environment because network dependency installation is unavailable/times out here.
