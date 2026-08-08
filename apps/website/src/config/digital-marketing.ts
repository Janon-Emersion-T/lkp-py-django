export interface DigitalMarketingService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface MarketingPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface MarketingStage {
  number: string;
  title: string;
  description: string;
}

export const digitalMarketingServices: DigitalMarketingService[] = [
  {
    number: "01",
    title: "SEO",
    href: "/services/digital-marketing/seo/",
    description:
      "Improve organic search visibility through technical foundations, relevant content, on-page optimisation and sustainable search strategy.",
    capabilities: [
      "Technical SEO",
      "On-page SEO",
      "Keyword strategy",
      "Organic growth",
    ],
  },
  {
    number: "02",
    title: "Local SEO",
    href: "/services/digital-marketing/local-seo/",
    description:
      "Strengthen visibility for businesses that need to be discovered by customers searching within specific locations and service areas.",
    capabilities: [
      "Local visibility",
      "Google Business Profile",
      "Local signals",
      "Location strategy",
    ],
  },
  {
    number: "03",
    title: "Google Ads",
    href: "/services/digital-marketing/google-ads/",
    description:
      "Build and manage paid search campaigns around commercial intent, controlled targeting and measurable conversion outcomes.",
    capabilities: [
      "Search campaigns",
      "Keyword targeting",
      "Conversion tracking",
      "Campaign optimisation",
    ],
  },
  {
    number: "04",
    title: "Social Media Marketing",
    href: "/services/digital-marketing/social-media-marketing/",
    description:
      "Use social channels strategically to build awareness, communicate expertise and maintain meaningful visibility with relevant audiences.",
    capabilities: [
      "Channel strategy",
      "Content planning",
      "Campaigns",
      "Audience growth",
    ],
  },
  {
    number: "05",
    title: "Email Marketing",
    href: "/services/digital-marketing/email-marketing/",
    description:
      "Develop permission-based email communication that supports lead nurturing, customer relationships and repeat engagement.",
    capabilities: [
      "Email campaigns",
      "Audience segmentation",
      "Lead nurturing",
      "Performance tracking",
    ],
  },
  {
    number: "06",
    title: "Content Marketing",
    href: "/services/digital-marketing/content-marketing/",
    description:
      "Create useful content around customer questions, commercial intent and subject expertise rather than publishing simply for volume.",
    capabilities: [
      "Content strategy",
      "Editorial planning",
      "Search content",
      "Authority building",
    ],
  },
  {
    number: "07",
    title: "Marketing Automation",
    href: "/services/digital-marketing/marketing-automation/",
    description:
      "Connect marketing activities and customer journeys so appropriate follow-up can happen consistently without unnecessary manual work.",
    capabilities: [
      "Lead workflows",
      "CRM integration",
      "Automated follow-up",
      "Journey automation",
    ],
  },
];

export const marketingPrinciples: MarketingPrinciple[] = [
  {
    number: "01",
    title: "Start with commercial intent",
    description:
      "Traffic is useful only when it brings the organisation closer to a meaningful business objective.",
  },
  {
    number: "02",
    title: "Measure beyond impressions",
    description:
      "Reach and visibility matter, but enquiries, qualified leads, conversion quality and revenue context matter more.",
  },
  {
    number: "03",
    title: "Own the foundation",
    description:
      "Websites, analytics, customer data and conversion infrastructure should remain controlled business assets rather than unexplained vendor dependencies.",
  },
  {
    number: "04",
    title: "Build compounding channels",
    description:
      "Paid acquisition can create immediate reach while search, content and customer relationships build longer-term marketing value.",
  },
];

export const marketingStages: MarketingStage[] = [
  {
    number: "01",
    title: "Discover",
    description:
      "Understand the business, customer, market, offer and current acquisition environment.",
  },
  {
    number: "02",
    title: "Position",
    description:
      "Clarify what should be communicated, to whom and why the audience should care.",
  },
  {
    number: "03",
    title: "Acquire",
    description:
      "Use suitable organic and paid channels to reach people with relevant intent.",
  },
  {
    number: "04",
    title: "Convert",
    description:
      "Reduce friction between attention and a meaningful enquiry, purchase or business action.",
  },
  {
    number: "05",
    title: "Retain",
    description:
      "Continue useful communication after the first interaction instead of repeatedly starting from zero.",
  },
  {
    number: "06",
    title: "Improve",
    description:
      "Use actual performance evidence to refine targeting, content, campaigns and conversion paths.",
  },
];
