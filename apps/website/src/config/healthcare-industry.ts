export interface HealthcareChallenge {
  number: string;
  title: string;
  description: string;
}

export interface HealthcareCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface HealthcarePrinciple {
  number: string;
  title: string;
  description: string;
}

export interface HealthcareWorkflow {
  number: string;
  title: string;
  description: string;
}

export const healthcareChallenges: HealthcareChallenge[] = [
  {
    number: "01",
    title: "Sensitive information requires controlled access",
    description:
      "Healthcare systems may contain confidential patient, staff and operational information, so authentication, permissions and data handling need deliberate controls.",
  },
  {
    number: "02",
    title: "Operational continuity matters",
    description:
      "Appointments, records, billing, internal coordination and communications often depend on technology being available when staff need it.",
  },
  {
    number: "03",
    title: "Workflows cross multiple teams",
    description:
      "Reception, practitioners, administration, finance and management may all interact with the same operational process from different perspectives.",
  },
  {
    number: "04",
    title: "Disconnected systems create avoidable administration",
    description:
      "Repeated entry across booking tools, spreadsheets, billing platforms and communication channels increases manual work and the likelihood of inconsistent records.",
  },
];

export const healthcareCapabilities: HealthcareCapability[] = [
  {
    number: "01",
    title: "Healthcare & Clinic Management Systems",
    href: "/services/software-development/custom-software/",
    description:
      "Custom operational platforms for appointments, patient administration, staff workflows, service records and management visibility.",
    outcomes: [
      "Structured records",
      "Role-based access",
      "Operational workflows",
      "Management visibility",
    ],
  },
  {
    number: "02",
    title: "Booking & Appointment Platforms",
    href: "/services/web-development/booking-websites/",
    description:
      "Online booking experiences that help patients or customers request and manage appointments while reducing repetitive scheduling administration.",
    outcomes: [
      "Online bookings",
      "Availability",
      "Notifications",
      "Scheduling workflows",
    ],
  },
  {
    number: "03",
    title: "Healthcare Websites",
    href: "/services/web-development/business-websites/",
    description:
      "Clear, accessible websites for clinics, practices and healthcare organisations that need to communicate services, locations and patient information professionally.",
    outcomes: [
      "Service information",
      "Responsive access",
      "Patient enquiries",
      "Search foundations",
    ],
  },
  {
    number: "04",
    title: "API & System Integration",
    href: "/services/api-integration/",
    description:
      "Connect approved healthcare, billing, communications and operational systems where suitable integration methods are available.",
    outcomes: [
      "Connected systems",
      "Reduced duplication",
      "Data exchange",
      "Workflow continuity",
    ],
  },
  {
    number: "05",
    title: "Business Automation",
    href: "/services/business-automation/",
    description:
      "Automate predictable administrative processes such as reminders, internal notifications and recurring operational tasks.",
    outcomes: [
      "Appointment reminders",
      "Workflow triggers",
      "Less manual administration",
      "Consistent processes",
    ],
  },
  {
    number: "06",
    title: "Cybersecurity",
    href: "/services/cybersecurity/",
    description:
      "Strengthen healthcare technology environments through security reviews, hardening, recovery planning and practical risk controls.",
    outcomes: [
      "Access protection",
      "Risk reduction",
      "Recovery planning",
      "System hardening",
    ],
  },
  {
    number: "07",
    title: "Cloud & Hosting",
    href: "/services/cloud-hosting/",
    description:
      "Support public websites and approved business systems with infrastructure designed around reliability, monitoring and controlled operation.",
    outcomes: [
      "Reliable hosting",
      "Monitoring",
      "Backups",
      "Operational support",
    ],
  },
  {
    number: "08",
    title: "Data & Analytics",
    href: "/services/data-analytics/",
    description:
      "Convert operational information into dashboards and reports for management oversight without exposing information unnecessarily.",
    outcomes: [
      "Operational reporting",
      "Service visibility",
      "Capacity insights",
      "Management dashboards",
    ],
  },
];

export const healthcarePrinciples: HealthcarePrinciple[] = [
  {
    number: "01",
    title: "Access should follow responsibility",
    description:
      "Users should receive only the level of system access needed for their role rather than broad access by default.",
  },
  {
    number: "02",
    title: "Do not collect data without a purpose",
    description:
      "Systems should avoid storing sensitive or unnecessary information simply because technically they can.",
  },
  {
    number: "03",
    title: "Design for operational continuity",
    description:
      "Backups, monitoring, recovery planning and dependable infrastructure matter when technology becomes part of daily healthcare operations.",
  },
  {
    number: "04",
    title: "Audit important actions",
    description:
      "Systems handling sensitive operational information benefit from traceability around important changes, access and workflow events.",
  },
];

export const healthcareWorkflows: HealthcareWorkflow[] = [
  {
    number: "01",
    title: "Enquiry & booking",
    description:
      "Patients or customers discover services, request appointments and receive confirmation through a clear digital journey.",
  },
  {
    number: "02",
    title: "Reception & administration",
    description:
      "Staff manage schedules, records, communications and recurring administrative work from structured systems.",
  },
  {
    number: "03",
    title: "Service delivery",
    description:
      "Authorised users access the operational information appropriate to their responsibilities.",
  },
  {
    number: "04",
    title: "Billing & follow-up",
    description:
      "Approved workflows can support invoicing, payment records, reminders and post-service administration.",
  },
  {
    number: "05",
    title: "Management oversight",
    description:
      "Operational dashboards and reports provide visibility without requiring managers to assemble information manually.",
  },
];
