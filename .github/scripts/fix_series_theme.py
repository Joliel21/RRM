from pathlib import Path
import re

path = Path('src/app/components/ReadingView.tsx')
text = path.read_text(encoding='utf-8')

replacement = r'''const RARE_INSIGHTS_TITLE_ART_BY_TOKEN = [
  { tokens: ["a-day-in-life"], asset: "/series/rare-insights/a-day-in-a-life.png" },
  { tokens: ["charity-advocacy"], asset: "/series/rare-insights/charity-and-advocacy.png" },
  { tokens: ["industry-insights"], asset: "/series/rare-insights/industry-insights.png" },
  { tokens: ["editors-letters"], asset: "/series/rare-insights/editors-letters.png" },
  { tokens: ["medical"], asset: "/series/rare-insights/medical.png" },
  { tokens: ["news-press"], asset: "/series/rare-insights/news-and-press-releases.png" },
  { tokens: ["patient-voice"], asset: "/series/rare-insights/patient-voice.png" },
  { tokens: ["rare-caregiving"], asset: "/series/rare-insights/rare-caregiving.png" },
  { tokens: ["rare-ramblings"], asset: "/series/rare-insights/rare-ramblings.png" },
  { tokens: ["rare-rev-inar"], asset: "/series/rare-insights/rare-rev-inar.png" },
  { tokens: ["reviews"], asset: "/series/rare-insights/reviews.png" },
  { tokens: ["science-and-tech"], asset: "/series/rare-insights/science-and-tech.png" },
  { tokens: ["sunday-sessions"], asset: "/series/rare-insights/sunday-sessions.png" },
  { tokens: ["travel-series"], asset: "/series/rare-insights/travel-series.png" },
  { tokens: ["turning-the-tide"], asset: "/series/rare-insights/turning-the-tide.png" },
] as const;

const getPageIdentity = (page: MagazinePage) =>
  [page.id, page.layoutId, page.imageUrl, page.alt]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();

const getRareInsightsTitleArt = (page: MagazinePage) => {
  const identity = getPageIdentity(page);
  const match = RARE_INSIGHTS_TITLE_ART_BY_TOKEN.find(({ tokens }) =>
    tokens.some((token) => identity.includes(token)),
  );
  return match ? resolveRepositoryRootAssetUrl(match.asset) : "";
};

const rareInsightsBackgroundCache = new Map<string, string>();

const useRareInsightsTitleColor = (page: MagazinePage) => {
  const source = getRareInsightsTitleArt(page);
  const [color, setColor] = useState<string | null>(() =>
    source ? rareInsightsBackgroundCache.get(source) || null : null,
  );

  useEffect(() => {
    if (!source) {
      setColor(null);
      return;
    }

    const cached = rareInsightsBackgroundCache.get(source);
    if (cached) {
      setColor(cached);
      return;
    }

    let cancelled = false;
    const image = new Image();
    image.decoding = "async";
    image.crossOrigin = "anonymous";
    image.onload = () => {
      if (cancelled) return;
      try {
        const canvas = document.createElement("canvas");
        canvas.width = 24;
        canvas.height = 24;
        const ctx = canvas.getContext("2d", { willReadFrequently: true });
        if (!ctx) return;
        ctx.drawImage(image, 0, 0, 24, 24);
        const data = ctx.getImageData(0, 0, 24, 24).data;
        const groups = new Map<string, { n: number; r: number; g: number; b: number }>();

        for (let y = 0; y < 24; y += 1) {
          for (let x = 0; x < 24; x += 1) {
            const i = (y * 24 + x) * 4;
            if (data[i + 3] < 200) continue;
            const edge = x < 5 || x > 18 || y < 5 || y > 18;
            const weight = edge ? 5 : 1;
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            const key = [Math.round(r / 24), Math.round(g / 24), Math.round(b / 24)].join("-");
            const group = groups.get(key) || { n: 0, r: 0, g: 0, b: 0 };
            group.n += weight;
            group.r += r * weight;
            group.g += g * weight;
            group.b += b * weight;
            groups.set(key, group);
          }
        }

        const best = Array.from(groups.values()).sort((a, b) => b.n - a.n)[0];
        if (!best || !best.n) return;
        const sampled = `rgb(${Math.round(best.r / best.n)}, ${Math.round(best.g / best.n)}, ${Math.round(best.b / best.n)})`;
        rareInsightsBackgroundCache.set(source, sampled);
        if (!cancelled) setColor(sampled);
      } catch (error) {
        console.warn("Could not sample RARE INSIGHTS title-page color", error);
      }
    };
    image.src = source;
    return () => {
      cancelled = true;
    };
  }, [source]);

  return color;
};

'''

pattern = re.compile(
    r'const RARE_INSIGHTS_ARCHIVE_TITLE_ART: Record<number, string> = \{.*?\n\};\n\nconst rareInsightsBackgroundCache.*?\n\};\n\n\n',
    re.S,
)
text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'Expected to replace one old RARE INSIGHTS color block, replaced {count}')

text = text.replace(
    'Boolean(RARE_INSIGHTS_ARCHIVE_TITLE_ART[page.pageNumber])',
    'Boolean(getRareInsightsTitleArt(page))',
)
text = text.replace(
    'const rareInsightsTitleColor = useRareInsightsTitleColor(page.pageNumber);',
    'const rareInsightsTitleColor = useRareInsightsTitleColor(page);',
)

old_root = '''    <div
      ref={pageContainerRef}
      className="relative w-full h-full overflow-hidden"
      data-static-community-page={
'''
new_root = '''    <div
      ref={pageContainerRef}
      className={`relative w-full h-full overflow-hidden ${
        seriesTheme ? "series-themed-page" : ""
      } ${seriesTheme && isSeriesRightPage ? "series-right-page" : ""}`}
      data-series-theme={seriesTheme?.key}
      style={{
        "--series-accent": seriesTheme?.color || undefined,
      } as CSSProperties}
      data-static-community-page={
'''
if old_root not in text:
    raise SystemExit('Static page root was not found')
text = text.replace(old_root, new_root, 1)

text = text.replace(
    '.rare-insights-matched-background > div {\n            background: var(--rare-insights-title-color) !important;\n          }',
    '.rare-insights-matched-background > div,\n          .rare-insights-matched-background > div > .shrink-0 {\n            background: var(--rare-insights-title-color) !important;\n          }',
    1,
)

path.write_text(text, encoding='utf-8')
