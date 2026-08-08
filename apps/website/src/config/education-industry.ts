export interface EducationChallenge {
  number: string;
  title: string;
  description: string;
}

export interface EducationCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface EducationPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface EducationWorkflow {
  number: string;
  title: string;
  description: string;
}

export const educationChallenges: EducationChallenge[] = [
  {
    number: "01",
    title: "Admissions create repeated administration",
    description:
      "Enquiries, applications, document collection, eligibility checks and onboarding can become fragmented when handled across forms, email, messaging and spreadsheets.",
  },
  {
    number: "02",
    title: "Student information needs one reliable source",
    description:
      "Attendance, payments, classes, contact details and academic or administrative records become difficult to manage when maintained in disconnected systems.",
  },
  {
    number: "03",
    title: "Communication has many audiences",
    description:
      "Students, parents, teachers, administrators and management often need different information at different stages of the education journey.",
  },
  {
    number: "04",
    title: "Growth exposes scheduling and reporting gaps",
    description:
      "As enrolments, classes and staff increase, informal scheduling and manual reporting become harder to operate consistently.",
  },
];

export const educationCapabilities: EducationCapability[] = [
  {
    number: "01",
    title: "Student & Education Management Systems",
    href: "/services/software-development/custom-software/",
    description:
      "Custom systems for student records, classes, attendance, admissions, payments, staff workflows and management reporting.",
    outcomes: [
      "Student records",
      "Attendance",
      "Class management",
      "Operational reporting",
    ],
  },
  {
    number: "02",
    title: "Admissions & Application Workflows",
    href: "/services/business-automation/",
    description:
      "Structure enquiries, applications, document collection, review and onboarding into a controlled digital process.",
    outcomes: [
      "Application tracking",
      "Document workflows",
      "Status visibility",
      "Less manual follow-up",
    ],
  },
  {
    number: "03",
    title: "Education Websites",
    href: "/services/web-development/business-websites/",
    description:
      "Websites for schools, training providers, academies and education organisations that clearly present programmes, admissions and important information.",
    outcomes: [
      "Programme discovery",
      "Admissions information",
      "Responsive access",
      "Search foundations",
    ],
  },
  {
    number: "04",
    title: "Student Portals & Web Applications",
    href: "/services/web-development/custom-web-applications/",
    description:
      "Authenticated portals for students, staff or parents where access to information and workflows needs to be controlled.",
    outcomes: [
      "Secure access",
      "Self-service",
      "Student information",
      "Staff workflows",
    ],
  },
  {
    number: "05",
    title: "Mobile Applications",
    href: "/services/mobile-app-development/",
    description:
      "Mobile experiences for communication, schedules, learning support and approved student or staff workflows.",
    outcomes: [
      "Mobile access",
      "Notifications",
      "Schedules",
      "User engagement",
    ],
  },
  {
    number: "06",
    title: "Payments & Integration",
    href: "/services/api-integration/",
    description:
      "Connect approved payment gateways, messaging services, learning platforms and operational systems where supported integrations exist.",
    outcomes: [
      "Online payments",
      "Connected systems",
      "Reduced duplication",
      "Automated updates",
    ],
  },
  {
    number: "07",
    title: "Communication Automation",
    href: "/services/business-automation/",
    description:
      "Automate predictable reminders and notifications around admissions, attendance, classes, payments and other recurring events.",
    outcomes: [
      "Reminders",
      "Notifications",
      "Faster follow-up",
      "Consistent communication",
    ],
  },
  {
    number: "08",
    title: "Data & Analytics",
    href: "/services/data-analytics/",
    description:
      "Create dashboards and reports for enrolment, attendance, revenue, utilisation and operational management.",
    outcomes: [
      "Enrolment visibility",
      "Attendance reporting",
      "Management dashboards",
      "Operational insight",
    ],
  },
];

export const educationPrinciples: EducationPrinciple[] = [
  {
    number: "01",
    title: "Keep student data purposeful",
    description:
      "Only collect and retain information required for defined educational, administrative or operational responsibilities.",
  },
  {
    number: "02",
    title: "Separate access by role",
    description:
      "Students, staff, parents and administrators should see only the information and actions relevant to their responsibilities.",
  },
  {
    number: "03",
    title: "Do not automate unclear processes",
    description:
      "Admissions and academic administration should be understood and standardised before automation is introduced.",
  },
  {
    number: "04",
    title: "Design for academic cycles",
    description:
      "Systems should account for terms, intakes, recurring classes, promotions, completion and other time-based education workflows.",
  },
];

export const educationWorkflows: EducationWorkflow[] = [
  {
    number: "01",
    title: "Discover",
    description:
      "Prospective students or parents find programmes, schedules, fees and admissions information.",
  },
  {
    number: "02",
    title: "Apply",
    description:
      "Applications, documents and required information are collected through a structured process.",
  },
  {
    number: "03",
    title: "Enrol",
    description:
      "Approved applicants become active students and are assigned to programmes, classes or cohorts.",
  },
  {
    number: "04",
    title: "Attend",
    description:
      "Attendance, schedules, communication and recurring class administration are managed consistently.",
  },
  {
    number: "05",
    title: "Manage",
    description:
      "Staff oversee payments, records, reporting and operational exceptions from a central system.",
  },
  {
    number: "06",
    title: "Progress",
    description:
      "Student status, completion and subsequent academic or administrative stages are recorded and managed.",
  },
];
