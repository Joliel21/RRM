from pathlib import Path
import json
import re

ROOT = Path('.')
layouts_path = ROOT / 'src/app/components/MagazinePageLayouts.tsx'
component_path = ROOT / 'src/app/components/SeriesArticlePage.tsx'
manifest_path = ROOT / 'magazine-source/public/series/rare-insights/manifest.json'
readme_path = ROOT / 'magazine-source/public/series/rare-insights/README.md'
articles_path = ROOT / 'magazine-source/public/series/rare-insights/a-day-in-a-life/articles.json'

layouts = layouts_path.read_text(encoding='utf-8')

# Extract the existing A Day in the Life content before removing the hardcoded array.
array_match = re.search(
    r'const A_DAY_IN_LIFE_ITEMS\s*=\s*\[(.*?)\]\s*as const;\s*',
    layouts,
    flags=re.S,
)
if not array_match:
    raise SystemExit('A_DAY_IN_LIFE_ITEMS array not found')

array_body = array_match.group(1)
entry_pattern = re.compile(
    r'\{\s*"title"\s*:\s*"((?:\\.|[^"\\])*)"\s*,\s*'
    r'"date"\s*:\s*"((?:\\.|[^"\\])*)"\s*,\s*'
    r'"url"\s*:\s*"((?:\\.|[^"\\])*)"\s*,\s*'
    r'"image"\s*:\s*resolveRepositoryAssetUrl\("((?:\\.|[^"\\])*)"\)\s*\}',
    flags=re.S,
)


def decode_js_string(value: str) -> str:
    return json.loads('"' + value + '"')


def slug_from_url(url: str) -> str:
    parts = [part for part in url.rstrip('/').split('/') if part]
    return parts[-1] if parts else url

articles = []
for match in entry_pattern.finditer(array_body):
    title, date, url, image = [decode_js_string(value) for value in match.groups()]
    articles.append({
        'id': slug_from_url(url),
        'title': title,
        'author': None,
        'date': date,
        'url': url,
        'image': image.lstrip('/'),
        'series': 'A Day in the Life',
        'titlePageAsset': 'series/rare-insights/a-day-in-a-life.png',
        'metadataStatus': 'partial',
    })

if not articles:
    raise SystemExit('No A Day in the Life article records were extracted')

articles_path.parent.mkdir(parents=True, exist_ok=True)
payload = {
    'schemaVersion': 1,
    'series': 'A Day in the Life',
    'slug': 'a-day-in-a-life',
    'articlePage': {
        'eyebrow': 'A Day in the Life',
        'heading': 'Explore the series',
        'summary': '{count} personal perspectives from everyday rare life',
        'maxTitleLength': 58,
    },
    'articles': articles,
}
articles_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Add the reusable data-driven AP renderer.
component_path.write_text(r'''import { useEffect, useMemo, useState } from "react";
import { resolveRepositoryAssetUrl } from "@/app/config/repository-assets";

type ArticleRecord = {
  id?: string;
  title: string | null;
  author?: string | null;
  date?: string | null;
  url: string | null;
  image: string | null;
  series?: string;
  titlePageAsset?: string;
  metadataStatus?: "complete" | "partial" | "pending-migration" | string;
};

type ArticlePageConfig = {
  eyebrow?: string;
  heading?: string;
  summary?: string;
  maxTitleLength?: number;
};

type SeriesArticlesPayload = {
  schemaVersion?: number;
  series: string;
  slug?: string;
  articlePage?: ArticlePageConfig;
  articles: ArticleRecord[];
};

type SeriesArticlePageProps = {
  sourcePath: string;
  fallbackSeriesName: string;
  ariaLabel?: string;
};

const shortenTitle = (title: string, maxLength: number) => {
  if (title.length <= maxLength) return title;
  const shortened = title.slice(0, maxLength - 3).replace(/\s+\S*$/, "");
  return `${shortened}...`;
};

const articleImageUrl = (value?: string | null) => {
  const rawValue = String(value || "").trim();
  if (!rawValue) return "";
  return resolveRepositoryAssetUrl(rawValue);
};

export const SeriesArticlePage = ({
  sourcePath,
  fallbackSeriesName,
  ariaLabel,
}: SeriesArticlePageProps) => {
  const [payload, setPayload] = useState<SeriesArticlesPayload | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();
    const sourceUrl = resolveRepositoryAssetUrl(sourcePath);

    setPayload(null);
    setError(null);

    fetch(sourceUrl, { signal: controller.signal, cache: "no-cache" })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Article inventory returned ${response.status}`);
        }
        return response.json() as Promise<SeriesArticlesPayload>;
      })
      .then((data) => {
        if (cancelled) return;
        if (!data || !Array.isArray(data.articles)) {
          throw new Error("Article inventory is missing an articles array");
        }
        setPayload(data);
      })
      .catch((reason) => {
        if (cancelled || reason?.name === "AbortError") return;
        console.warn(`Could not load article inventory ${sourcePath}`, reason);
        setError("Article information could not be loaded.");
      });

    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [sourcePath]);

  const seriesName = payload?.series || fallbackSeriesName;
  const display = payload?.articlePage || {};
  const articles = useMemo(
    () => (payload?.articles || []).filter((article) => article?.title && article?.url),
    [payload],
  );
  const maxTitleLength = display.maxTitleLength || 58;
  const summary = (display.summary || "{count} articles")
    .replace("{count}", String(articles.length));

  return (
    <div className="relative flex h-full w-full flex-col overflow-hidden bg-[#f4f9fb] text-[#17384b]">
      <div className="shrink-0 border-b border-[#d5e7ed] bg-white px-8 pb-5 pt-7">
        <p className="mb-1 text-[9px] font-bold uppercase tracking-[0.27em] text-[#2b9bc0]">
          {display.eyebrow || seriesName}
        </p>
        <h2 className="text-[28px] font-light leading-none tracking-[-0.035em] text-[#222d33]">
          {display.heading || "Explore the series"}
        </h2>
        <p className="mt-2 text-[11px] text-[#54707d]">
          {payload ? summary : error || "Loading articles…"}
        </p>
      </div>

      <div
        className="series-data-article-scroll min-h-0 flex-1 overflow-y-auto overscroll-contain px-5 py-5"
        onWheel={(event) => event.stopPropagation()}
        onWheelCapture={(event) => event.stopPropagation()}
        onTouchMove={(event) => event.stopPropagation()}
        aria-label={ariaLabel || `${seriesName} article archive`}
      >
        {error ? (
          <div className="rounded-[10px] border border-[#d5e7ed] bg-white p-5 text-[11px] text-[#54707d]">
            {error}
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4 pb-8">
            {articles.map((item, index) => {
              const title = String(item.title || "");
              const image = articleImageUrl(item.image);
              return (
                <a
                  key={item.id || item.url || `${seriesName}-${index}`}
                  href={String(item.url)}
                  target="_blank"
                  rel="noopener noreferrer"
                  title={title}
                  aria-label={`Open ${title} in a new tab`}
                  className="group flex h-[250px] min-h-[250px] max-h-[250px] flex-col overflow-hidden rounded-[10px] border border-[#d5e7ed] bg-white no-underline shadow-[0_2px_10px_rgba(20,60,75,0.07)] transition-transform hover:-translate-y-0.5 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#2b9bc0]"
                >
                  <div className="flex h-[170px] min-h-[170px] max-h-[170px] shrink-0 items-center justify-center overflow-hidden bg-[#edf4f6] p-1">
                    {image ? (
                      <img
                        src={image}
                        alt=""
                        className="h-full w-full object-contain scale-[1.08]"
                        loading={index < 4 ? "eager" : "lazy"}
                        draggable={false}
                      />
                    ) : null}
                  </div>
                  <div className="flex h-[80px] min-h-[80px] max-h-[80px] flex-col overflow-hidden px-3 pb-3 pt-2.5">
                    <span className="mb-1.5 text-[8px] font-semibold uppercase tracking-[0.12em] text-[#2b9bc0]">
                      {seriesName}
                    </span>
                    <h3 className="text-[11px] font-semibold leading-[1.28] text-[#203b48]">
                      {shortenTitle(title, maxTitleLength)}
                    </h3>
                  </div>
                </a>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
''', encoding='utf-8')

# Import the reusable component.
import_anchor = 'import travelSeriesJoeRumneyImage from "@/assets/travel-series-joe-rumney.png";\n'
import_line = 'import { SeriesArticlePage } from "./SeriesArticlePage";\n'
if import_line not in layouts:
    if import_anchor not in layouts:
        raise SystemExit('Import anchor not found')
    layouts = layouts.replace(import_anchor, import_anchor + import_line, 1)

# Remove the hardcoded records and their title-specific helper.
layouts = layouts[:array_match.start()] + layouts[array_match.end():]
layouts = re.sub(
    r'const shortenDayInLifeTitle\s*=\s*\(title: string, maxLength = 58\)\s*=>\s*\{.*?\};\s*',
    '',
    layouts,
    count=1,
    flags=re.S,
)

# Replace only the A Day in the Life AP implementation with the generic renderer.
layout_start = layouts.find('const ADayInLifeScrollLayout = () => (')
layout_end_marker = '\nconst CHARITY_ADVOCACY_URL ='
layout_end = layouts.find(layout_end_marker, layout_start)
if layout_start == -1 or layout_end == -1:
    raise SystemExit('A Day in the Life AP layout block not found')
replacement = '''const ADayInLifeScrollLayout = () => (\n  <SeriesArticlePage\n    sourcePath="/series/rare-insights/a-day-in-a-life/articles.json"\n    fallbackSeriesName="A Day in the Life"\n    ariaLabel="Scrollable gallery of A Day in the Life articles"\n  />\n);\n'''
layouts = layouts[:layout_start] + replacement + layouts[layout_end:]
layouts_path.write_text(layouts, encoding='utf-8')

# Connect the manifest entry to the AP inventory.
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
found = False
for entry in manifest.get('entries', []):
    if entry.get('slug') == 'a-day-in-a-life':
        entry['articlesFile'] = 'series/rare-insights/a-day-in-a-life/articles.json'
        entry['articlePageRenderer'] = 'data-driven'
        found = True
        break
if not found:
    raise SystemExit('A Day in the Life manifest entry not found')
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Update canonical documentation without claiming other series have migrated.
readme = readme_path.read_text(encoding='utf-8')
old_status = ('Step 4 establishes the canonical structure only. Article inventories and article-level metadata are handled in the next metadata migration step. No article metadata should be described as migrated until it has actually been verified and written to the appropriate series inventory.')
new_status = ('A Day in the Life is the first migrated, data-driven AP and reads from `a-day-in-a-life/articles.json`. Other series remain pending migration until their verified article inventories are created and connected to the reusable AP renderer.')
if old_status in readme:
    readme = readme.replace(old_status, new_status)
elif new_status not in readme:
    readme += '\n\n## Current AP migration\n\n' + new_status + '\n'
readme_path.write_text(readme, encoding='utf-8')

print(f'Migrated {len(articles)} A Day in the Life articles to {articles_path}')
