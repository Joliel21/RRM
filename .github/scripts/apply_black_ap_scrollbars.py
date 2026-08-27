from pathlib import Path

path = Path('src/app/components/ReadingView.tsx')
text = path.read_text(encoding='utf-8')

old = '''          .series-themed-page.series-article-page [class*="overflow-y-auto"],\n          .series-themed-page.series-article-page [class*="overscroll-contain"] {\n            background: var(--series-accent) !important;\n          }\n'''
new = '''          .series-themed-page.series-article-page [class*="overflow-y-auto"],\n          .series-themed-page.series-article-page [class*="overscroll-contain"] {\n            background: var(--series-accent) !important;\n            scrollbar-color: #000000 rgba(255,255,255,0.28) !important;\n          }\n          .series-themed-page.series-article-page [class*="overflow-y-auto"]::-webkit-scrollbar-thumb,\n          .series-themed-page.series-article-page [class*="overscroll-contain"]::-webkit-scrollbar-thumb {\n            background: #000000 !important;\n            border-color: transparent !important;\n          }\n          .series-themed-page.series-article-page [class*="overflow-y-auto"]::-webkit-scrollbar-button,\n          .series-themed-page.series-article-page [class*="overscroll-contain"]::-webkit-scrollbar-button {\n            background-color: #000000 !important;\n          }\n          .series-themed-page.series-article-page [class*="overflow-y-auto"]::-webkit-scrollbar-button:single-button:vertical:decrement,\n          .series-themed-page.series-article-page [class*="overscroll-contain"]::-webkit-scrollbar-button:single-button:vertical:decrement {\n            background-color: #000000 !important;\n          }\n          .series-themed-page.series-article-page [class*="overflow-y-auto"]::-webkit-scrollbar-button:single-button:vertical:increment,\n          .series-themed-page.series-article-page [class*="overscroll-contain"]::-webkit-scrollbar-button:single-button:vertical:increment {\n            background-color: #000000 !important;\n          }\n'''

if new in text:
    raise SystemExit('Black AP scrollbar styles already applied')
if old not in text:
    raise SystemExit('AP article-field CSS block not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
