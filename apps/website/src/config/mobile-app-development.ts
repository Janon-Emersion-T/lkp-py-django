export interface MobileAppService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface MobileAppPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface MobileAppStage {
  number: string;
  title: string;
  description: string;
}

export const mobileAppServices: MobileAppService[] = [
  {
    number: "01",
    title: "Android Apps",
    href: "/services/mobile-app-development/android-apps/",
    description:
      "Android applications designed around real user journeys, device requirements and the operational systems behind the experience.",
    capabilities: [
      "Android development",
      "Business applications",
      "API integration",
      "Play Store readiness",
    ],
  },
  {
    number: "02",
    title: "iOS Apps",
    href: "/services/mobile-app-development/ios-apps/",
    description:
      "iPhone and iPad applications developed with careful attention to interface behaviour, platform expectations and backend integration.",
    capabilities: [
      "iPhone apps",
      "iPad apps",
      "Apple ecosystem",
      "App Store readiness",
    ],
  },
  {
    number: "03",
    title: "Cross Platform Apps",
    href: "/services/mobile-app-development/cross-platform-apps/",
    description:
      "Shared-code mobile applications for organisations that need Android and iOS delivery without maintaining completely separate product codebases.",
    capabilities: [
      "Flutter applications",
      "Shared codebase",
      "Android & iOS",
      "Responsive interfaces",
    ],
  },
  {
    number: "04",
    title: "Business Apps",
    href: "/services/mobile-app-development/business-apps/",
    description:
      "Purpose-built mobile tools for employees, customers and operational teams where mobility is part of the business workflow.",
    capabilities: [
      "Internal apps",
      "Field operations",
      "Customer portals",
      "Workflow integration",
    ],
  },
];

export const mobileAppPrinciples: MobileAppPrinciple[] = [
  {
    number: "01",
    title: "Mobile is a working environment",
    description:
      "Small screens, unreliable connectivity, touch input and real-world movement create requirements that cannot simply be copied from desktop software.",
  },
  {
    number: "02",
    title: "The backend still matters",
    description:
      "A polished app depends on reliable APIs, authentication, data integrity and the systems operating behind the interface.",
  },
  {
    number: "03",
    title: "Design around user tasks",
    description:
      "The interface should prioritise what users need to accomplish quickly rather than trying to expose every available system function.",
  },
  {
    number: "04",
    title: "Plan for release and maintenance",
    description:
      "Store policies, operating-system changes, dependencies and device updates continue after the first application release.",
  },
];

export const mobileAppStages: MobileAppStage[] = [
  {
    number: "01",
    title: "Discover",
    description:
      "Understand users, business objectives, device context and the processes the application must support.",
  },
  {
    number: "02",
    title: "Define",
    description:
      "Establish features, permissions, integrations, data requirements and the appropriate mobile architecture.",
  },
  {
    number: "03",
    title: "Design",
    description:
      "Create user flows and interfaces around mobile interaction rather than shrinking a desktop experience.",
  },
  {
    number: "04",
    title: "Build",
    description:
      "Develop the application and backend integrations in modular, testable stages.",
  },
  {
    number: "05",
    title: "Validate",
    description:
      "Test functionality, devices, edge cases, authentication and the end-to-end user journey.",
  },
  {
    number: "06",
    title: "Release",
    description:
      "Prepare distribution, production services and operational monitoring for real users.",
  },
];
