export interface AnalyticsService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface AnalyticsPrinciple {
  number: string;
  title: string;
  description: string;
}

export const analyticsServices: AnalyticsService[] = [
  {
    number: "01",
    title: "Business Intelligence",
    href: "/services/data-analytics/business-intelligence/",
    description:
      "Bring information from operational systems together so decision-makers can understand performance, trends and business conditions more clearly.",
    capabilities: [
      "Data consolidation",
      "Operational analysis",
      "Management visibility",
      "Decision support",
    ],
  },
  {
    number: "02",
    title: "Dashboards",
    href: "/services/data-analytics/dashboards/",
    description:
      "Interactive views that make important operational, financial, sales and performance information easier to understand and act on.",
    capabilities: [
      "Executive dashboards",
      "Operational dashboards",
      "Real-time views",
      "Role-based reporting",
    ],
  },
  {
    number: "03",
    title: "Reports",
    href: "/services/data-analytics/reports/",
    description:
      "Structured reporting systems that reduce manual preparation and deliver consistent business information when it is needed.",
    capabilities: [
      "Automated reports",
      "Scheduled reporting",
      "Management reports",
      "Custom reporting",
    ],
  },
  {
    number: "04",
    title: "KPI Tracking",
    href: "/services/data-analytics/kpi-tracking/",
    description:
      "Define and monitor the indicators that matter to the organisation instead of collecting metrics without business context.",
    capabilities: [
      "KPI definition",
      "Target tracking",
      "Performance trends",
      "Exception visibility",
    ],
  },
];

export const analyticsPrinciples: AnalyticsPrinciple[] = [
  {
    number: "01",
    title: "Start with the decision",
    description:
      "Analytics should begin with what the organisation needs to understand or decide, not with producing as many charts as possible.",
  },
  {
    number: "02",
    title: "Use trustworthy data",
    description:
      "Poor source data, inconsistent definitions and duplicate records undermine even the most polished dashboard.",
  },
  {
    number: "03",
    title: "Keep context visible",
    description:
      "Numbers require definitions, time periods, targets and business context before they become useful information.",
  },
  {
    number: "04",
    title: "Make insight operational",
    description:
      "The objective is not simply reporting. The objective is helping people recognise conditions and take better action.",
  },
];
