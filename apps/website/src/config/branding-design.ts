export interface BrandingDesignService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface DesignPrinciple {
  number: string;
  title: string;
  description: string;
}

export const brandingDesignServices: BrandingDesignService[] = [
  {
    number: "01",
    title: "Logo Design",
    href: "/services/branding-design/logo-design/",
    description:
      "Create a distinctive visual mark that represents the organisation clearly and works across practical business applications.",
    capabilities: [
      "Logo concepts",
      "Primary marks",
      "Logo variations",
      "Usage-ready assets",
    ],
  },
  {
    number: "02",
    title: "Brand Identity",
    href: "/services/branding-design/brand-identity/",
    description:
      "Build a coherent visual system around the brand so colour, typography, imagery and communication feel consistent across channels.",
    capabilities: [
      "Visual identity",
      "Colour systems",
      "Typography",
      "Brand guidelines",
    ],
  },
  {
    number: "03",
    title: "UI/UX Design",
    href: "/services/branding-design/ui-ux-design/",
    description:
      "Design digital interfaces around user tasks, business requirements and clear interaction rather than decoration alone.",
    capabilities: [
      "User flows",
      "Interface design",
      "Responsive UX",
      "Design systems",
    ],
  },
  {
    number: "04",
    title: "Graphic Design",
    href: "/services/branding-design/graphic-design/",
    description:
      "Create business and marketing materials that apply the brand consistently across digital and physical communication.",
    capabilities: [
      "Marketing graphics",
      "Business collateral",
      "Social creatives",
      "Campaign assets",
    ],
  },
];

export const designPrinciples: DesignPrinciple[] = [
  {
    number: "01",
    title: "Design has a job",
    description:
      "Every visual decision should support recognition, communication, usability or another defined business purpose.",
  },
  {
    number: "02",
    title: "Consistency builds recognition",
    description:
      "A brand becomes familiar when its visual language remains coherent across websites, documents, advertising and communication.",
  },
  {
    number: "03",
    title: "Clarity before decoration",
    description:
      "A polished design that confuses users or weakens the message has failed regardless of how visually impressive it looks.",
  },
  {
    number: "04",
    title: "Build systems, not isolated files",
    description:
      "Reusable rules and components make branding and digital design easier to maintain as the organisation grows.",
  },
];
