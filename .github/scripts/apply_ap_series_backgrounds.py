from pathlib import Path

path = Path('src/app/components/ReadingView.tsx')
text = path.read_text(encoding='utf-8')

helper_marker = 'const PageContent = ({\n'
helper = r'''const isArticlePage = (page: MagazinePage) => {
  const layoutId = String(page.layoutId || "").toLowerCase();
  const identity = getPageIdentity(page);

  return (
    layoutId.includes("archive") ||
    layoutId.includes("scroll") ||
    layoutId.includes("quarter") ||
    layoutId.includes("middle") ||
    layoutId.includes("final") ||
    layoutId === "editors-letters-right" ||
    identity.includes("article-page")
  );
};

'''
if 'const isArticlePage = ' not in text:
    if helper_marker not in text:
        raise SystemExit('PageContent marker not found')
    text = text.replace(helper_marker, helper + helper_marker, 1)

old_state = '''  const isRareInsightsSeriesPage = seriesTheme?.key === "rare-insights";\n  const isSeriesRightPage = page.pageNumber % 2 !== 0;\n'''
new_state = '''  const isRareInsightsSeriesPage = seriesTheme?.key === "rare-insights";\n  const isArticlePageView = isArticlePage(page);\n  const isSeriesRightPage = page.pageNumber % 2 !== 0;\n'''
if new_state not in text:
    if old_state not in text:
        raise SystemExit('Series state insertion point not found')
    text = text.replace(old_state, new_state, 1)

old_class = '''        className={`series-themed-page relative h-full w-full overflow-hidden ${\n          isSeriesRightPage ? "series-right-page" : "series-left-page"\n        } ${rareInsightsTitleColor ? "rare-insights-matched-background" : ""}`}\n'''
new_class = '''        className={`series-themed-page relative h-full w-full overflow-hidden ${\n          isSeriesRightPage ? "series-right-page" : "series-left-page"\n        } ${isArticlePageView ? "series-article-page" : ""} ${\n          rareInsightsTitleColor ? "rare-insights-matched-background" : ""\n        }`}\n'''
if new_class not in text:
    if old_class not in text:
        raise SystemExit('Layout wrapper class block not found')
    text = text.replace(old_class, new_class, 1)

css_anchor = '''          .series-themed-page.series-right-page .shrink-0 > p:first-of-type,\n          .series-themed-page.series-right-page header > p:first-of-type {\n            color: var(--series-accent) !important;\n          }\n'''
css_add = '''          .series-themed-page.series-right-page .shrink-0 > p:first-of-type,\n          .series-themed-page.series-right-page header > p:first-of-type {\n            color: var(--series-accent) !important;\n          }\n          .series-themed-page.series-article-page [class*="overflow-y-auto"],\n          .series-themed-page.series-article-page [class*="overscroll-contain"] {\n            background: var(--series-accent) !important;\n          }\n'''
if css_add not in text:
    if css_anchor not in text:
        raise SystemExit('Series CSS insertion point not found')
    text = text.replace(css_anchor, css_add, 1)

path.write_text(text, encoding='utf-8')
