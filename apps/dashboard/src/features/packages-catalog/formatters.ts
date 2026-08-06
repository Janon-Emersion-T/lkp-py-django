import type {
  BillingCycle,
  PackageCategory,
  PackageStatus,
  PricingType,
} from "./types";

export const packageCategoryLabels: Record<PackageCategory, string> = {
  website: "Website",
  seo: "SEO",
  marketing: "Marketing",
  software: "Software",
  mobile_app: "Mobile App",
  hosting: "Hosting",
  maintenance: "Maintenance",
  consulting: "Consulting",
  other: "Other",
};

export const packageStatusLabels: Record<PackageStatus, string> = {
  draft: "Draft",
  scheduled: "Scheduled",
  published: "Published",
  archived: "Archived",
};

export const pricingTypeLabels: Record<PricingType, string> = {
  fixed: "Fixed",
  starting_from: "Starting From",
  custom_quote: "Custom Quote",
  free: "Free",
};

export const billingCycleLabels: Record<BillingCycle, string> = {
  one_time: "One Time",
  monthly: "Monthly",
  quarterly: "Quarterly",
  half_yearly: "Half Yearly",
  yearly: "Yearly",
};

export function formatDateTime(value: string | null): string {
  if (!value) {
    return "—";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function formatPackagePrice({
  pricingType,
  price,
  currency,
}: {
  pricingType: PricingType;
  price: string;
  currency: string;
}): string {
  if (pricingType === "custom_quote") {
    return "Custom quote";
  }

  if (pricingType === "free") {
    return "Free";
  }

  const amount = Number(price);

  const formatted = Number.isFinite(amount)
    ? new Intl.NumberFormat(undefined, {
        maximumFractionDigits: 2,
      }).format(amount)
    : price;

  return pricingType === "starting_from"
    ? `From ${currency} ${formatted}`
    : `${currency} ${formatted}`;
}

export function statusClasses(status: PackageStatus): string {
  if (status === "published") {
    return "border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300";
  }

  if (status === "scheduled") {
    return "border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-900 dark:bg-blue-950/40 dark:text-blue-300";
  }

  if (status === "archived") {
    return "border-slate-300 bg-slate-100 text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300";
  }

  return "border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-300";
}
