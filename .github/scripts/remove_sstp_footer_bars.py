from pathlib import Path

# 1) Global renderer rule: no generated footer bar on any SSTP.
reading_path = Path('src/app/components/ReadingView.tsx')
reading = reading_path.read_text(encoding='utf-8')
old = '(isRareInsightsSeriesPage ? !isMajorSeriesCoverSpreadPage : !isSeriesTitleSpreadPage)'
if old in reading:
    reading = reading.replace(old, '!isSeriesTitleSpreadPage')
else:
    # Accept already-normalized state, but fail if neither form is present.
    if 'seriesTheme && !isSeriesTitleSpreadPage' not in reading:
        raise SystemExit('Could not locate SSTP footer render condition in ReadingView.tsx')
reading_path.write_text(reading, encoding='utf-8')

# 2) RARE INSIGHTS has a dedicated layout footer wrapper. Prevent it from
# wrapping intro/title layouts (SSTPs); archive/content layouts (APs) keep it.
layouts_path = Path('src/app/components/MagazinePageLayouts.tsx')
layouts = layouts_path.read_text(encoding='utf-8')
old_loop = '''RARE_INSIGHTS_FOOTER_LAYOUT_IDS.forEach((layoutId) => {\n  const LayoutComponent = LAYOUT_REGISTRY[layoutId];\n  if (LayoutComponent) {\n    LAYOUT_REGISTRY[layoutId] = withRareInsightsFooterRow(LayoutComponent);\n  }\n});'''
new_loop = '''RARE_INSIGHTS_FOOTER_LAYOUT_IDS.forEach((layoutId) => {\n  // SSTPs never receive a generated footer bar.\n  if (layoutId.includes("intro") || layoutId.includes("title")) return;\n\n  const LayoutComponent = LAYOUT_REGISTRY[layoutId];\n  if (LayoutComponent) {\n    LAYOUT_REGISTRY[layoutId] = withRareInsightsFooterRow(LayoutComponent);\n  }\n});'''
if new_loop not in layouts:
    if old_loop not in layouts:
        raise SystemExit('Could not locate RARE INSIGHTS footer wrapper loop')
    layouts = layouts.replace(old_loop, new_loop, 1)
layouts_path.write_text(layouts, encoding='utf-8')
