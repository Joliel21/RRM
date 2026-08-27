from pathlib import Path

path = Path('src/app/components/ReadingView.tsx')
text = path.read_text(encoding='utf-8')

# Page 98 only: make the replacement copy modestly larger than the baked copy,
# keep it inside the page, and cover the original text cleanly.
start_token = 'page.id === "a-day-in-life-intro-page"'
end_token = '\n{seriesTheme && !isSeriesTitleSpreadPage ? ('
start = text.find(start_token)
if start == -1:
    raise SystemExit('Page 98 overlay block not found')
end = text.find(end_token, start)
if end == -1:
    raise SystemExit('Page 98 overlay end marker not found')

block = text[start:end]
replacements = {
    'left: "9.5%"': 'left: "7%"',
    'right: "7.5%"': 'right: "5.5%"',
    'top: "55.7%"': 'top: "55.2%"',
    'gridTemplateColumns: "52% 48%"': 'gridTemplateColumns: "55% 45%"',
    'fontSize: "15px"': 'fontSize: "10px"',
    'lineHeight: 1.36': 'lineHeight: 1.4',
    'paddingRight: "24px"': 'paddingRight: "16px"',
    'marginBottom: "14px"': 'marginBottom: "9px"',
    'marginTop: "14px"': 'marginTop: "9px"',
    'paddingTop: "12px"': 'paddingTop: "8px"',
    'fontSize: "22px"': 'fontSize: "16px"',
    'paddingLeft: "30px"': 'paddingLeft: "20px"',
}
for old, new in replacements.items():
    if old not in block:
        raise SystemExit(f'Expected page 98 style not found: {old}')
    block = block.replace(old, new)
text = text[:start] + block + text[end:]

# Global rule: all series intro/title pages are title pages. They do not get
# the added series bottom bar. Interior/gallery/archive pages still do.
old_helper_tail = '''    "series-cover/resources.png",\n  ].some((token) => identity.includes(token));\n};'''
new_helper_tail = '''    "series-cover/resources.png",\n  ].some((token) => identity.includes(token)) ||\n    identity.includes("intro-page") ||\n    identity.includes("title-page");\n};'''
if new_helper_tail not in text:
    if old_helper_tail not in text:
        raise SystemExit('Series title-spread helper tail not found')
    text = text.replace(old_helper_tail, new_helper_tail, 1)

# Ensure the interior-page bar paints above scroll/gallery/layout content on
# both left and right pages.
text = text.replace('z-[150] h-[10px]', 'z-[9999] h-[10px]')

path.write_text(text, encoding='utf-8')
