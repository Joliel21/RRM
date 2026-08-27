from pathlib import Path

path = Path('src/app/components/MagazinePageLayouts.tsx')
text = path.read_text(encoding='utf-8')

if 'const RARE_INSIGHTS_FOOTER_LAYOUT_IDS' in text:
    raise SystemExit('RARE INSIGHTS footer row wrapper already exists')

append = r'''

// RARE INSIGHTS pages use a dedicated footer row so the gold band cannot be
// hidden by scrollable/archive layout content. Static image title pages are
// handled by ReadingView; these are the HTML/layout pages in the section.
const RARE_INSIGHTS_FOOTER_LAYOUT_IDS = new Set([
  "rare-insights-page-92",
  "rare-insights-page-93",
  "rare-insights-page-94",
  "rare-insights-page-95",
  "a-day-in-life-intro",
  "a-day-in-life-scroll",
  "charity-advocacy-intro",
  "charity-advocacy-archive",
  "industry-insights-intro",
  "industry-insights-archive",
  "news-press-intro",
  "news-press-quarter",
  "news-press-middle",
  "news-press-final",
  "medical-intro",
  "medical-archive",
  "editors-letters-left",
  "editors-letters-right",
  "patient-voice-intro",
  "patient-voice-archive",
  "rare-caregiving-intro",
  "rare-caregiving-archive",
  "rare-ramblings-intro",
  "rare-ramblings-archive",
  "rare-rev-inar-intro",
  "rare-rev-inar-archive",
  "reviews-intro",
  "reviews-archive",
  "science-tech-intro",
  "science-tech-archive",
  "sunday-sessions-intro",
  "sunday-sessions-archive",
  "travel-series-intro",
  "travel-series-archive",
  "turning-the-tide-intro",
  "turning-the-tide-archive-one",
  "turning-the-tide-archive-two",
]);

const withRareInsightsFooterRow = (
  LayoutComponent: React.ComponentType<PageLayoutProps>,
): React.ComponentType<PageLayoutProps> => {
  const RareInsightsFooterLayout = (props: PageLayoutProps) => (
    <div className="grid h-full w-full grid-rows-[minmax(0,1fr)_29px] overflow-hidden">
      <div className="min-h-0 min-w-0 overflow-hidden">
        <LayoutComponent {...props} />
      </div>
      <div
        className="h-[29px] w-full shrink-0 bg-[#C99B38]"
        aria-hidden="true"
      />
    </div>
  );

  return RareInsightsFooterLayout;
};

RARE_INSIGHTS_FOOTER_LAYOUT_IDS.forEach((layoutId) => {
  const LayoutComponent = LAYOUT_REGISTRY[layoutId];
  if (LayoutComponent) {
    LAYOUT_REGISTRY[layoutId] = withRareInsightsFooterRow(LayoutComponent);
  }
});
'''

text = text.rstrip() + append + '\n'
path.write_text(text, encoding='utf-8')
