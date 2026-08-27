from pathlib import Path

path = Path('src/app/components/ReadingView.tsx')
text = path.read_text(encoding='utf-8')

# 1) Page 98 only: reduce the replacement body copy so it is just one step
# larger than the original and remains fully inside the page.
start_token = 'page.id === "a-day-in-life-intro-page"'
end_token = '\n{seriesTheme ? ('
start = text.find(start_token)
if start == -1:
    raise SystemExit('Page 98 overlay block not found')
end = text.find(end_token, start)
if end == -1:
    raise SystemExit('Page 98 overlay end marker not found')

block = text[start:end]
replacements = {
    'fontSize: "19px"': 'fontSize: "15px"',
    'lineHeight: 1.43': 'lineHeight: 1.36',
    'paddingRight: "30px"': 'paddingRight: "24px"',
    'marginBottom: "22px"': 'marginBottom: "14px"',
    'marginTop: "22px"': 'marginTop: "14px"',
    'paddingTop: "16px"': 'paddingTop: "12px"',
    'fontSize: "27px"': 'fontSize: "22px"',
    'paddingLeft: "38px"': 'paddingLeft: "30px"',
}
for old, new in replacements.items():
    block = block.replace(old, new)
text = text[:start] + block + text[end:]

# 2) Global series rule: major two-page series title/opening spreads do not
# receive the added bottom bar. Interior pages in the series still do.
helper = '''\nconst isSeriesTitleSpread = (page: MagazinePage) => {\n  const identity = getPageIdentity(page);\n  return [\n    "rare-insights-spread-title-page",\n    "people-of-rare-spread-title-page",\n    "digital-spotlight-spread-title-page",\n    "rare-reports-spread-title-page",\n    "rare-charities-spread",\n    "resources-spread-page",\n    "series-cover/resources.png",\n  ].some((token) => identity.includes(token));\n};\n\n'''

page_content_marker = 'const PageContent = ({\n'
if 'const isSeriesTitleSpread = ' not in text:
    if page_content_marker not in text:
        raise SystemExit('PageContent marker not found')
    text = text.replace(page_content_marker, helper + page_content_marker, 1)

state_old = '  const seriesTheme = getSeriesThemeRule(page);\n  const isSeriesRightPage = page.pageNumber % 2 !== 0;\n'
state_new = '  const seriesTheme = getSeriesThemeRule(page);\n  const isSeriesTitleSpreadPage = isSeriesTitleSpread(page);\n  const isSeriesRightPage = page.pageNumber % 2 !== 0;\n'
if state_new not in text:
    if state_old not in text:
        raise SystemExit('Series theme state block not found')
    text = text.replace(state_old, state_new, 1)

# There are two added bar renderers: layout pages and static/image pages.
# Suppress both on major title spreads only.
old_condition = '{seriesTheme ? ('
new_condition = '{seriesTheme && !isSeriesTitleSpreadPage ? ('
count = text.count(old_condition)
if count < 2:
    raise SystemExit(f'Expected at least two seriesTheme bar conditions, found {count}')
text = text.replace(old_condition, new_condition, 2)

path.write_text(text, encoding='utf-8')
