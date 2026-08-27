import { getDataUrl, getOrganizationRawBaseUrl } from "@/app/config/data-source";

const REMOVED_ASSET_PATHS = new Set([
  "images/tea.png",
  "series-cover/resources.png",
]);

const normalizeRepositoryPath = (value: string) =>
  value
    .replace(/^public\//i, "")
    .replace(/^\/+/, "");

const isRemovedAssetPath = (value: string) =>
  REMOVED_ASSET_PATHS.has(normalizeRepositoryPath(value));

/** Resolve assets stored under magazine-source/public. */
export function resolveRepositoryAssetUrl(value?: string | null): string {
  const rawValue = String(value || "").trim();
  if (!rawValue) return "";

  if (/^(?:https?:|data:|blob:)/i.test(rawValue) || rawValue.startsWith("//")) {
    return rawValue;
  }

  if (isRemovedAssetPath(rawValue)) return "";

  let normalizedPath = normalizeRepositoryPath(rawValue);
  if (normalizedPath === "images/bsyndro.png") {
    normalizedPath = "images/bardet_biedl_syndrome.png";
  }

  // During local RRM development these assets are in this same repository.
  return `/magazine-source/public/${normalizedPath}`;
}

/** Resolve assets stored at the RRM repository root. */
export function resolveRepositoryRootAssetUrl(value?: string | null): string {
  const rawValue = String(value || "").trim();
  if (!rawValue) return "";

  if (/^(?:https?:|data:|blob:)/i.test(rawValue) || rawValue.startsWith("//")) {
    return rawValue;
  }

  if (isRemovedAssetPath(rawValue)) return "";
  return `/${normalizeRepositoryPath(rawValue)}`;
}

/** Resolve an organization-owned logo, sponsor image, or issue asset. */
export function resolveOrganizationAssetUrl(value?: string | null): string {
  const rawValue = String(value || "").trim();
  if (!rawValue) return "";

  if (/^(?:https?:|data:|blob:)/i.test(rawValue) || rawValue.startsWith("//")) {
    return rawValue;
  }

  const organizationBase = getOrganizationRawBaseUrl();
  if (!organizationBase) return resolveRepositoryAssetUrl(rawValue);
  return `${organizationBase}${rawValue.replace(/^\/+/, "")}`;
}
