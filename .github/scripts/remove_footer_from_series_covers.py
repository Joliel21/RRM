from pathlib import Path

path = Path('src/app/components/ReadingView.tsx')
text = path.read_text(encoding='utf-8')

old_helper = '''const isSeriesTitleSpread = (page: MagazinePage) => {\n  const identity = getPageIdentity(page);\n  return [\n    "rare-insights-spread-title-page",\n    "people-of-rare-spread-title-page",\n    "digital-spotlight-spread-title-page",\n    "rare-reports-spread-title-page",\n    "rare-charities-spread",\n    "resources-spread-page",\n    "series-cover/resources.png",\n  ].some((token) => identity.includes(token)) ||\n    identity.includes("intro-page") ||\n    identity.includes("title-page");\n};\n'''

new_helper = '''const isMajorSeriesCoverSpread = (page: MagazinePage) => {\n  const identity = getPageIdentity(page);\n  return [\n    "rare-insights-spread-title-page",\n    "people-of-rare-spread-title-page",\n    "digital-spotlight-spread-title-page",\n    "rare-reports-spread-title-page",\n    "rare-charities-spread",\n    "resources-spread-page",\n    "series-cover/resources.png",\n  ].some((token) => identity.includes(token));\n};\n\nconst isSeriesTitleSpread = (page: MagazinePage) => {\n  const identity = getPageIdentity(page);\n  return (\n    isMajorSeriesCoverSpread(page) ||\n    identity.includes("intro-page") ||\n    identity.includes("title-page")\n  );\n};\n'''

if old_helper not in text:
    raise SystemExit('Series-title helper block not found')
text = text.replace(old_helper, new_helper, 1)

old_state = '''  const seriesTheme = getSeriesThemeRule(page);\n  const isSeriesTitleSpreadPage = isSeriesTitleSpread(page);\n  const isRareInsightsSeriesPage = seriesTheme?.key === "rare-insights";\n'''
new_state = '''  const seriesTheme = getSeriesThemeRule(page);\n  const isSeriesTitleSpreadPage = isSeriesTitleSpread(page);\n  const isMajorSeriesCoverSpreadPage = isMajorSeriesCoverSpread(page);\n  const isRareInsightsSeriesPage = seriesTheme?.key === "rare-insights";\n'''
if old_state not in text:
    raise SystemExit('Series state block not found')
text = text.replace(old_state, new_state, 1)

old_condition = 'seriesTheme && (isRareInsightsSeriesPage || !isSeriesTitleSpreadPage)'
new_condition = 'seriesTheme && (isRareInsightsSeriesPage ? !isMajorSeriesCoverSpreadPage : !isSeriesTitleSpreadPage)'
count = text.count(old_condition)
if count != 2:
    raise SystemExit(f'Expected two footer conditions, found {count}')
text = text.replace(old_condition, new_condition)

path.write_text(text, encoding='utf-8')
