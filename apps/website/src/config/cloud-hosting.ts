export interface CloudHostingService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface InfrastructurePrinciple {
  number: string;
  title: string;
  description: string;
}

export const cloudHostingServices: CloudHostingService[] = [
  {
    number: "01",
    title: "Web Hosting",
    href: "/services/cloud-hosting/web-hosting/",
    description:
      "Managed hosting environments for business websites and web applications with attention to availability, configuration, security and maintainability.",
    capabilities: [
      "Website hosting",
      "Application hosting",
      "Environment configuration",
      "Operational support",
    ],
  },
  {
    number: "02",
    title: "VPS Hosting",
    href: "/services/cloud-hosting/vps-hosting/",
    description:
      "Virtual private server environments for businesses that require greater control, isolation, custom configuration or application-specific infrastructure.",
    capabilities: [
      "Server provisioning",
      "Linux environments",
      "Application deployment",
      "Server management",
    ],
  },
  {
    number: "03",
    title: "Domain Registration",
    href: "/services/cloud-hosting/domain-registration/",
    description:
      "Domain registration and management with clear ownership, DNS configuration and operational control.",
    capabilities: [
      "Domain registration",
      "DNS management",
      "Domain renewals",
      "Domain configuration",
    ],
  },
  {
    number: "04",
    title: "Business Email",
    href: "/services/cloud-hosting/business-email/",
    description:
      "Professional email setup and configuration using organisation-owned domains and suitable business email platforms.",
    capabilities: [
      "Mailbox setup",
      "Domain email",
      "DNS configuration",
      "Email migration",
    ],
  },
  {
    number: "05",
    title: "SSL Certificates",
    href: "/services/cloud-hosting/ssl-certificates/",
    description:
      "SSL/TLS certificate configuration and renewal so websites and applications can communicate securely over HTTPS.",
    capabilities: [
      "Certificate installation",
      "HTTPS configuration",
      "Renewal management",
      "Certificate troubleshooting",
    ],
  },
];

export const infrastructurePrinciples: InfrastructurePrinciple[] = [
  {
    number: "01",
    title: "Ownership must remain clear",
    description:
      "Domains, hosting accounts, credentials and infrastructure should have identifiable ownership rather than depending on undocumented third-party access.",
  },
  {
    number: "02",
    title: "Availability requires maintenance",
    description:
      "Infrastructure cannot be treated as permanent once deployed. Updates, renewals, monitoring and configuration still require attention.",
  },
  {
    number: "03",
    title: "Backups need a recovery purpose",
    description:
      "A backup strategy should consider what must be restored, how quickly and who is responsible when recovery is required.",
  },
  {
    number: "04",
    title: "Infrastructure should fit the workload",
    description:
      "The most expensive server is not automatically the right solution. Capacity, traffic, application behaviour and growth should guide the environment.",
  },
];
