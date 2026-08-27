from pathlib import Path

path = Path('src/app/components/ReadingView.tsx')
text = path.read_text(encoding='utf-8')

anchor = '''          .series-themed-page.series-article-page [class*="overflow-y-auto"],\n          .series-themed-page.series-article-page [class*="overscroll-contain"] {\n            background: var(--series-accent) !important;\n            scrollbar-color: #000000 rgba(255,255,255,0.28) !important;\n          }\n'''

addition = '''          .series-themed-page.series-article-page [class*="overflow-y-auto"],\n          .series-themed-page.series-article-page [class*="overscroll-contain"] {\n            background: var(--series-accent) !important;\n            scrollbar-color: #000000 rgba(255,255,255,0.28) !important;\n          }\n          .series-themed-page.series-article-page[data-series-theme="people-of-rare"] [class*="overflow-y-auto"],\n          .series-themed-page.series-article-page[data-series-theme="people-of-rare"] [class*="overscroll-contain"] {\n            background: #111111 !important;\n            background-color: #111111 !important;\n          }\n          .series-themed-page.series-article-page[data-series-theme="people-of-rare"] [class*="overflow-y-auto"] > div,\n          .series-themed-page.series-article-page[data-series-theme="people-of-rare"] [class*="overscroll-contain"] > div {\n            background: transparent !important;\n          }\n'''

if addition not in text:
    if anchor not in text:
        raise SystemExit('AP background CSS anchor not found')
    text = text.replace(anchor, addition, 1)

path.write_text(text, encoding='utf-8')
