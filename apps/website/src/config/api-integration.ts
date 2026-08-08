export interface IntegrationService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface IntegrationPrinciple {
  number: string;
  title: string;
  description: string;
}

export const integrationServices: IntegrationService[] = [
  {
    number: "01",
    title: "Payment Gateway",
    href: "/services/api-integration/payment-gateway/",
    description:
      "Connect websites, applications and business systems with payment providers while keeping transaction flow, status handling and operational requirements clear.",
    capabilities: [
      "Payment APIs",
      "Transaction status",
      "Webhook handling",
      "Payment workflows",
    ],
  },
  {
    number: "02",
    title: "WhatsApp API",
    href: "/services/api-integration/whatsapp-api/",
    description:
      "Integrate WhatsApp messaging into customer, support and operational workflows using suitable business messaging infrastructure.",
    capabilities: [
      "Business messaging",
      "Status notifications",
      "Workflow triggers",
      "Customer communications",
    ],
  },
  {
    number: "03",
    title: "SMS Gateway",
    href: "/services/api-integration/sms-gateway/",
    description:
      "Connect applications and operational systems to SMS providers for alerts, confirmations, reminders and transactional communication.",
    capabilities: [
      "Transactional SMS",
      "OTP workflows",
      "Status updates",
      "Automated reminders",
    ],
  },
  {
    number: "04",
    title: "CRM Integration",
    href: "/services/api-integration/crm-integration/",
    description:
      "Connect CRM platforms with websites, lead sources, communications and internal systems so customer information moves with less duplication.",
    capabilities: [
      "Lead synchronisation",
      "Customer data flow",
      "Pipeline integration",
      "Event triggers",
    ],
  },
  {
    number: "05",
    title: "ERP Integration",
    href: "/services/api-integration/erp-integration/",
    description:
      "Integrate ERP platforms with operational applications, ecommerce, inventory, finance or external services where reliable data exchange is required.",
    capabilities: [
      "Operational sync",
      "Inventory integration",
      "Finance data flow",
      "Business system links",
    ],
  },
];

export const integrationPrinciples: IntegrationPrinciple[] = [
  {
    number: "01",
    title: "Define the source of truth",
    description:
      "Every integration needs clarity about which system owns each piece of information and which systems only consume or mirror it.",
  },
  {
    number: "02",
    title: "Design for failure",
    description:
      "External services become unavailable, requests time out and data can be rejected. Reliable integrations need explicit error and retry behaviour.",
  },
  {
    number: "03",
    title: "Protect credentials and data",
    description:
      "API keys, tokens, customer information and transaction data should be handled according to appropriate security boundaries.",
  },
  {
    number: "04",
    title: "Keep integrations observable",
    description:
      "Logs, statuses and operational visibility matter because silent integration failures can disrupt business processes without obvious symptoms.",
  },
];
