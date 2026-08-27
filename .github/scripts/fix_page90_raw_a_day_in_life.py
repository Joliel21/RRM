from pathlib import Path

# Page 90: use the raw A Day in the Life PNG directly.
app_path = Path('src/app/App.tsx')
app = app_path.read_text(encoding='utf-8')

old = '''          // Pre-shift pages 88–89 render as final printed pages 90–91 after\n          // the blank inside cover and blank page 1 are inserted below.\n          // The approved content is the Explore More two-page spread.\n          for (let pageNumber = 88; pageNumber <= 89; pageNumber++) {\n            const importedPageId = `explore-more-spread-page-${pageNumber}`;\n            finalPages.push({\n              id: importedPageId,\n              pageNumber,\n              type: "image",\n              imageUrl: resolveRepositoryRootAssetUrl("/images/explore-more.png"),\n              alt: `Explore More series spread page ${pageNumber + 2}`,\n              hotspots: [],\n            });\n          }\n'''

new = '''          // Pre-shift page 88 renders as final printed page 90 after\n          // the blank inside cover and blank page 1 are inserted below.\n          // Render the approved A Day in the Life title artwork directly.\n          finalPages.push({\n            id: "a-day-in-life-page-90",\n            pageNumber: 88,\n            type: "image",\n            imageUrl: resolveRepositoryRootAssetUrl(\n              "/series/rare-insights/a-day-in-a-life.png",\n            ),\n            alt: "RARE INSIGHTS A Day in the Life title page",\n            hotspots: [],\n          });\n\n          // Pre-shift page 89 remains the existing final printed page 91 content.\n          finalPages.push({\n            id: "explore-more-spread-page-89",\n            pageNumber: 89,\n            type: "image",\n            imageUrl: resolveRepositoryRootAssetUrl("/images/explore-more.png"),\n            alt: "Explore More series spread page 91",\n            hotspots: [],\n          });\n'''

if old in app:
    app = app.replace(old, new, 1)
elif 'id: "a-day-in-life-page-90"' not in app:
    raise SystemExit('Could not locate current page 90 mapping block in App.tsx')

app_path.write_text(app, encoding='utf-8')

# Remove the old page-specific replacement text overlay so the source PNG is
# displayed exactly as stored in the repository with no white HTML text box.
reading_path = Path('src/app/components/ReadingView.tsx')
reading = reading_path.read_text(encoding='utf-8')
start_marker = '      {page.id === "a-day-in-life-intro-page" ? ('
start = reading.find(start_marker)
if start != -1:
    next_markers = [
        '\n      {seriesTheme &&',
        '\n{seriesTheme &&',
    ]
    ends = [reading.find(marker, start) for marker in next_markers]
    ends = [idx for idx in ends if idx != -1]
    if not ends:
        raise SystemExit('Found A Day in the Life overlay but could not locate its end')
    end = min(ends)
    reading = reading[:start] + reading[end:]

reading_path.write_text(reading, encoding='utf-8')
