# RRM NPM Source 1.0.8

This package replaces the PowerShell launcher workflow with a plain source package intended to be run directly with npm.

## Run

From the extracted package folder:

```powershell
npm install
npm run build
npm run dev
```

## Packaging changes

- `package.json` is at the package root.
- No `.ps1` or `.cmd` launcher is required.
- `package-lock.json` is intentionally omitted so `npm install` creates a fresh lock file on the user's Node/npm environment.
- `node_modules` and build output are not included.
- The source includes the 1.0.7 page and cover wiring changes.
- The Recharts 2.15.2 deprecation message is an npm warning and should not be treated as a startup failure.

## Package QA

- ZIP: `RRM_NPM_SOURCE_1.0.8.zip`
- ZIP integrity test: passed
- SHA-256: `ac6c8c0f3b4725d5f181a7ef10e6c3dd99916542b3250e2cbf44696892264080`
