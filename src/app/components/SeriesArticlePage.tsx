import { useEffect, useMemo, useState } from "react";
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
  variant?: "default" | "charity-advocacy";
  archiveUrl?: string;
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
  variant = "default",
  archiveUrl,
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
  const isCharityAdvocacy = variant === "charity-advocacy";
  const accentClass = isCharityAdvocacy ? "text-[#30b0be]" : "text-[#2b9bc0]";
  const focusRingClass = isCharityAdvocacy
    ? "focus-visible:ring-[#30b0be]"
    : "focus-visible:ring-[#2b9bc0]";

  return (
    <div
      className={`relative flex h-full w-full flex-col overflow-hidden ${
        isCharityAdvocacy ? "bg-[#f6fafb]" : "bg-[#f4f9fb]"
      } text-[#17384b]`}
    >
      {isCharityAdvocacy ? (
        <style>{`
          .series-themed-page.series-article-page .charity-advocacy-scroll.charity-advocacy-scroll {
            scrollbar-width: thin !important;
            scrollbar-color: #30b0be #e9f0f2 !important;
          }
          .series-themed-page.series-article-page .charity-advocacy-scroll.charity-advocacy-scroll::-webkit-scrollbar {
            width: 8px !important;
          }
          .series-themed-page.series-article-page .charity-advocacy-scroll.charity-advocacy-scroll::-webkit-scrollbar-track {
            background: #e9f0f2 !important;
            border-radius: 999px;
          }
          .series-themed-page.series-article-page .charity-advocacy-scroll.charity-advocacy-scroll::-webkit-scrollbar-thumb {
            background: #30b0be !important;
            border: 2px solid #e9f0f2 !important;
            border-radius: 999px;
          }
        `}</style>
      ) : null}

      <div
        className={`shrink-0 border-b ${
          isCharityAdvocacy ? "border-[#d8e7ea]" : "border-[#d5e7ed]"
        } bg-white px-8 pb-5 pt-7`}
      >
        <p
          className={`mb-1 text-[9px] font-bold uppercase tracking-[0.27em] ${accentClass}`}
        >
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
        className={`${
          isCharityAdvocacy ? "charity-advocacy-scroll" : "series-data-article-scroll"
        } min-h-0 flex-1 overflow-y-auto overscroll-contain px-5 py-5`}
        onWheel={(event) => event.stopPropagation()}
        onWheelCapture={(event) => event.stopPropagation()}
        onTouchMove={(event) => event.stopPropagation()}
        aria-label={ariaLabel || `${seriesName} article archive`}
      >
        {error ? (
          <div
            className={`rounded-[10px] border ${
              isCharityAdvocacy ? "border-[#d7e7e9]" : "border-[#d5e7ed]"
            } bg-white p-5 text-[11px] text-[#54707d]`}
          >
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
                  className={`group flex h-[250px] min-h-[250px] max-h-[250px] flex-col overflow-hidden rounded-[10px] border ${
                    isCharityAdvocacy ? "border-[#d7e7e9]" : "border-[#d5e7ed]"
                  } bg-white no-underline shadow-[0_2px_10px_rgba(20,60,75,0.07)] transition-transform hover:-translate-y-0.5 focus:outline-none focus-visible:ring-2 ${focusRingClass}`}
                >
                  <div
                    className={`flex h-[170px] min-h-[170px] max-h-[170px] shrink-0 items-center justify-center overflow-hidden ${
                      isCharityAdvocacy ? "bg-[#eef3f4] p-2" : "bg-[#edf4f6] p-1"
                    }`}
                  >
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
                    <span
                      className={`mb-1.5 text-[8px] font-semibold uppercase tracking-[0.12em] ${accentClass}`}
                    >
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

        {archiveUrl ? (
          <a
            href={archiveUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={`mx-auto mb-8 flex w-fit rounded-full bg-[#17384b] px-5 py-2.5 text-[9px] font-bold uppercase tracking-[0.14em] text-white no-underline transition-opacity hover:opacity-90 focus:outline-none focus-visible:ring-2 ${focusRingClass}`}
          >
            Open full archive
          </a>
        ) : null}
      </div>
    </div>
  );
};
