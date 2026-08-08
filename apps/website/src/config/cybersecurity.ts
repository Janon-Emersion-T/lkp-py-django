export interface CybersecurityService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface SecurityPrinciple {
  number: string;
  title: string;
  description: string;
}

export const cybersecurityServices: CybersecurityService[] = [
  {
    number: "01",
    title: "Security Audit",
    href: "/services/cybersecurity/security-audit/",
    description:
      "Review systems, configurations, access, dependencies and operating practices to identify security weaknesses and practical areas for improvement.",
    capabilities: [
      "Security review",
      "Configuration assessment",
      "Risk identification",
      "Improvement recommendations",
    ],
  },
  {
    number: "02",
    title: "Website Security",
    href: "/services/cybersecurity/website-security/",
    description:
      "Improve the security posture of websites and web applications through configuration, updates, access controls and technical review.",
    capabilities: [
      "Application security",
      "Access controls",
      "Dependency review",
      "Security configuration",
    ],
  },
  {
    number: "03",
    title: "Backup & Recovery",
    href: "/services/cybersecurity/backup-recovery/",
    description:
      "Design practical backup and recovery arrangements so critical systems and data can be restored when failures or incidents occur.",
    capabilities: [
      "Backup strategy",
      "Recovery planning",
      "Restore validation",
      "Business continuity",
    ],
  },
  {
    number: "04",
    title: "Security Hardening",
    href: "/services/cybersecurity/security-hardening/",
    description:
      "Reduce unnecessary attack surface by strengthening servers, applications, access rules, services and deployment configurations.",
    capabilities: [
      "Server hardening",
      "Application hardening",
      "Access restrictions",
      "Configuration control",
    ],
  },
];

export const securityPrinciples: SecurityPrinciple[] = [
  {
    number: "01",
    title: "Reduce unnecessary exposure",
    description:
      "Every unused service, excessive permission and unnecessary public interface increases the surface that needs protecting.",
  },
  {
    number: "02",
    title: "Assume failures will happen",
    description:
      "Security planning should include recovery and continuity, not only prevention.",
  },
  {
    number: "03",
    title: "Limit access by responsibility",
    description:
      "People and systems should receive only the level of access required for their role or function.",
  },
  {
    number: "04",
    title: "Keep systems maintained",
    description:
      "Outdated software, forgotten accounts and unmanaged dependencies create avoidable risk over time.",
  },
];
