export interface RetailChallenge {
  number: string;
  title: string;
  description: string;
}

export interface RetailCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface RetailPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface RetailJourney {
  number: string;
  title: string;
  description: string;
}

export const retailChallenges: RetailChallenge[] = [
  {
    number: "01",
    title: "Product discovery can break before checkout",
    description:
      "Customers need clear categories, search, product information, pricing and navigation before payment or conversion optimisation can matter.",
  },
  {
    number: "02",
    title: "Stock and order data often become fragmented",
    description:
      "Retail teams can end up maintaining product, inventory and order information across storefronts, spreadsheets, POS systems and messaging channels.",
  },
  {
    number: "03",
    title: "Checkout friction directly affects revenue",
    description:
      "Slow pages, unclear delivery rules, unnecessary steps and poorly integrated payments create avoidable abandonment.",
  },
  {
    number: "04",
    title: "Growth increases fulfilment complexity",
    description:
      "As orders increase, manual processing, stock updates, notifications and customer follow-up become harder to manage consistently.",
  },
];

export const retailCapabilities: RetailCapability[] = [
  {
    number: "01",
    title: "E-commerce Websites",
    href: "/services/web-development/ecommerce-websites/",
    description:
      "Build online stores around product discovery, mobile usability, checkout, payment and the operational workflows behind each order.",
    outcomes: [
      "Online sales",
      "Product catalogue",
      "Checkout",
      "Mobile commerce",
    ],
  },
  {
    number: "02",
    title: "Custom Commerce Applications",
    href: "/services/web-development/custom-web-applications/",
    description:
      "Develop tailored commerce platforms when standard store software cannot support required pricing, workflows, integrations or business rules.",
    outcomes: [
      "Custom workflows",
      "Business rules",
      "Customer accounts",
      "Scalable commerce",
    ],
  },
  {
    number: "03",
    title: "Inventory & POS Systems",
    href: "/services/software-development/",
    description:
      "Connect stock, products, transactions and operational records across retail environments through structured software systems.",
    outcomes: [
      "Inventory visibility",
      "Product control",
      "Sales records",
      "Operational consistency",
    ],
  },
  {
    number: "04",
    title: "Payment Integration",
    href: "/services/api-integration/",
    description:
      "Integrate supported payment gateways and transaction services into approved checkout and order workflows.",
    outcomes: [
      "Online payments",
      "Transaction status",
      "Reduced checkout friction",
      "Payment workflows",
    ],
  },
  {
    number: "05",
    title: "Order & Customer Automation",
    href: "/services/business-automation/",
    description:
      "Automate predictable events around orders, status changes, notifications, customer follow-up and internal administration.",
    outcomes: [
      "Order notifications",
      "Status automation",
      "Customer follow-up",
      "Less manual work",
    ],
  },
  {
    number: "06",
    title: "SEO & Digital Marketing",
    href: "/services/digital-marketing/",
    description:
      "Increase product and category discovery through organic search, paid acquisition, content and measurable campaign activity.",
    outcomes: [
      "Product visibility",
      "Paid acquisition",
      "Organic traffic",
      "Customer growth",
    ],
  },
  {
    number: "07",
    title: "CRM & Customer Data",
    href: "/services/software-development/crm-development/",
    description:
      "Centralise customer interactions, enquiries and commercial history where the business needs more structured relationship management.",
    outcomes: [
      "Customer records",
      "Sales visibility",
      "Lead tracking",
      "Retention workflows",
    ],
  },
  {
    number: "08",
    title: "Retail Analytics",
    href: "/services/data-analytics/",
    description:
      "Create dashboards and reports around sales, products, orders, campaigns and customer behaviour for better operational decisions.",
    outcomes: [
      "Sales reporting",
      "Product performance",
      "Campaign insight",
      "Management visibility",
    ],
  },
];

export const retailPrinciples: RetailPrinciple[] = [
  {
    number: "01",
    title: "Make discovery easy before adding complexity",
    description:
      "Good commerce begins with customers finding and understanding the right product quickly, not with adding more features to checkout.",
  },
  {
    number: "02",
    title: "Keep product data authoritative",
    description:
      "Product names, pricing, stock, variants and related information should have clear ownership rather than drifting across disconnected systems.",
  },
  {
    number: "03",
    title: "Automate stable order events",
    description:
      "Confirmation, status notifications and recurring fulfilment actions can be automated when the underlying rules are predictable.",
  },
  {
    number: "04",
    title: "Measure revenue paths, not traffic alone",
    description:
      "Retail analytics should connect acquisition and product discovery to carts, orders, repeat customers and other commercial outcomes.",
  },
];

export const retailJourney: RetailJourney[] = [
  {
    number: "01",
    title: "Discover",
    description:
      "The customer arrives through search, advertising, social media, direct traffic or another acquisition channel.",
  },
  {
    number: "02",
    title: "Browse",
    description:
      "Categories, search, filters, product information and pricing help the customer evaluate available options.",
  },
  {
    number: "03",
    title: "Convert",
    description:
      "Cart, delivery information and checkout reduce uncertainty and move the customer towards a completed transaction.",
  },
  {
    number: "04",
    title: "Pay",
    description:
      "Supported payment services complete the transaction and return a reliable status to the commerce workflow.",
  },
  {
    number: "05",
    title: "Fulfil",
    description:
      "Order, stock, status and staff workflows support processing, delivery or collection.",
  },
  {
    number: "06",
    title: "Retain",
    description:
      "Customer records, communication and service quality can support repeat purchasing without relying on intrusive messaging.",
  },
];
