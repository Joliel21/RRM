from pathlib import Path

path = Path('src/app/components/ReadingView.tsx')
text = path.read_text(encoding='utf-8')

state_old = '''  const seriesTheme = getSeriesThemeRule(page);\n  const isSeriesTitleSpreadPage = isSeriesTitleSpread(page);\n  const isSeriesRightPage = page.pageNumber % 2 !== 0;\n'''
state_new = '''  const seriesTheme = getSeriesThemeRule(page);\n  const isSeriesTitleSpreadPage = isSeriesTitleSpread(page);\n  const isRareInsightsSeriesPage = seriesTheme?.key === "rare-insights";\n  const isSeriesRightPage = page.pageNumber % 2 !== 0;\n'''
if state_new not in text:
    if state_old not in text:
        raise SystemExit('Series state block not found')
    text = text.replace(state_old, state_new, 1)

layout_old = '''        {seriesTheme && !isSeriesTitleSpreadPage ? (\n          <div\n            className="pointer-events-none absolute bottom-0 left-0 right-0 z-[9999] h-[10px]"\n            style={{ backgroundColor: seriesTheme.color }}\n            aria-hidden="true"\n          />\n        ) : null}\n'''
layout_new = '''        {seriesTheme && (isRareInsightsSeriesPage || !isSeriesTitleSpreadPage) ? (\n          <div\n            className="pointer-events-none absolute bottom-0 left-0 right-0 z-[9999]"\n            style={{\n              backgroundColor: seriesTheme.color,\n              height: isRareInsightsSeriesPage ? "4.4%" : "10px",\n            }}\n            aria-hidden="true"\n          />\n        ) : null}\n'''
if layout_new not in text:
    if layout_old not in text:
        raise SystemExit('Layout series bar block not found')
    text = text.replace(layout_old, layout_new, 1)

static_old = '''{seriesTheme && !isSeriesTitleSpreadPage ? (\n  <>\n    <style>{`\n      .series-themed-page * {\n        scrollbar-color: var(--series-accent) rgba(255,255,255,0.18) !important;\n      }\n      .series-themed-page *::-webkit-scrollbar-thumb {\n        background: var(--series-accent) !important;\n        border-color: transparent !important;\n      }\n      .series-themed-page.series-right-page .shrink-0 > p:first-of-type,\n      .series-themed-page.series-right-page header > p:first-of-type {\n        color: var(--series-accent) !important;\n      }\n    `}</style>\n    <div\n      className="static-series-bottom-bar pointer-events-none absolute bottom-0 left-0 right-0 z-[9999] h-[10px]"\n      style={{ backgroundColor: seriesTheme.color }}\n      aria-hidden="true"\n    />\n  </>\n) : null}\n'''
static_new = '''{seriesTheme && (isRareInsightsSeriesPage || !isSeriesTitleSpreadPage) ? (\n  <>\n    <style>{`\n      .series-themed-page * {\n        scrollbar-color: var(--series-accent) rgba(255,255,255,0.18) !important;\n      }\n      .series-themed-page *::-webkit-scrollbar-thumb {\n        background: var(--series-accent) !important;\n        border-color: transparent !important;\n      }\n      .series-themed-page.series-right-page .shrink-0 > p:first-of-type,\n      .series-themed-page.series-right-page header > p:first-of-type {\n        color: var(--series-accent) !important;\n      }\n    `}</style>\n    <div\n      className="static-series-bottom-bar pointer-events-none absolute bottom-0 left-0 right-0 z-[9999]"\n      style={{\n        backgroundColor: seriesTheme.color,\n        height: isRareInsightsSeriesPage ? "4.4%" : "10px",\n      }}\n      aria-hidden="true"\n    />\n  </>\n) : null}\n'''
if static_new not in text:
    if static_old not in text:
        raise SystemExit('Static series bar block not found')
    text = text.replace(static_old, static_new, 1)

path.write_text(text, encoding='utf-8')
