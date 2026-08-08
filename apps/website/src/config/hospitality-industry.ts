export interface HospitalityChallenge {
  number: string;
  title: string;
  description: string;
}

export interface HospitalityCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface HospitalityPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface HospitalityJourney {
  number: string;
  title: string;
  description: string;
}

export const hospitalityChallenges: HospitalityChallenge[] = [
  {
    number: "01",
    title: "Third-party booking dependence reduces control",
    description:
      "Hospitality businesses often rely heavily on external booking platforms, which can reduce ownership of the customer relationship and compress margins.",
  },
  {
    number: "02",
    title: "Guest communication is repetitive",
    description:
      "Availability questions, confirmations, check-in details, directions and follow-up messages consume staff time when every interaction is handled manually.",
  },
  {
    number: "03",
    title: "Property information needs to stay consistent",
    description:
      "Rooms, rates, amenities, policies and availability can become inconsistent across the website, booking channels and messaging conversations.",
  },
  {
    number: "04",
    title: "Marketing needs to connect to bookings",
    description:
      "Traffic and social engagement have limited value if campaigns are not connected to a clear booking path and measurable conversion activity.",
  },
];

export const hospitalityCapabilities: HospitalityCapability[] = [
  {
    number: "01",
    title: "Hospitality Websites",
    href: "/services/web-development/business-websites/",
    description:
      "Professional websites for hotels, villas, guesthouses, serviced apartments and accommodation providers that clearly present the property and encourage direct enquiries or bookings.",
    outcomes: [
      "Property presentation",
      "Direct enquiries",
      "Mobile experience",
      "Search foundations",
    ],
  },
  {
    number: "02",
    title: "Booking Websites",
    href: "/services/web-development/booking-websites/",
    description:
      "Online booking experiences that support availability, reservations and guest journeys around the property's operating model.",
    outcomes: [
      "Direct bookings",
      "Availability",
      "Reservation flow",
      "Guest convenience",
    ],
  },
  {
    number: "03",
    title: "E-commerce & Payments",
    href: "/services/web-development/ecommerce-websites/",
    description:
      "Support deposits, booking payments, gift vouchers or other approved online transactions through suitable payment integrations.",
    outcomes: [
      "Online payments",
      "Deposits",
      "Transaction records",
      "Reduced friction",
    ],
  },
  {
    number: "04",
    title: "Digital Marketing",
    href: "/services/digital-marketing/",
    description:
      "Use search, paid campaigns, social media and content to improve visibility and create more measurable booking demand.",
    outcomes: [
      "Direct demand",
      "Campaign visibility",
      "Search traffic",
      "Booking acquisition",
    ],
  },
  {
    number: "05",
    title: "SEO & Local Visibility",
    href: "/services/digital-marketing/",
    description:
      "Strengthen organic and local search visibility around accommodation, destination and location-specific demand.",
    outcomes: [
      "Local discovery",
      "Organic visibility",
      "Destination searches",
      "Qualified traffic",
    ],
  },
  {
    number: "06",
    title: "Guest Communication Automation",
    href: "/services/business-automation/",
    description:
      "Automate predictable communications such as confirmations, reminders, pre-arrival instructions and selected post-stay follow-up.",
    outcomes: [
      "Faster responses",
      "Guest reminders",
      "Reduced administration",
      "Consistent messaging",
    ],
  },
  {
    number: "07",
    title: "API & Platform Integration",
    href: "/services/api-integration/",
    description:
      "Connect supported booking, payment, messaging, CRM or property systems where reliable integration methods are available.",
    outcomes: [
      "Connected systems",
      "Reduced duplication",
      "Data exchange",
      "Operational consistency",
    ],
  },
  {
    number: "08",
    title: "Data & Analytics",
    href: "/services/data-analytics/",
    description:
      "Build reporting and dashboards around bookings, enquiries, campaign performance, occupancy-related information and management visibility.",
    outcomes: [
      "Booking insight",
      "Campaign reporting",
      "Management visibility",
      "Performance tracking",
    ],
  },
];

export const hospitalityPrinciples: HospitalityPrinciple[] = [
  {
    number: "01",
    title: "Direct booking should be easy",
    description:
      "A potential guest should not have to work harder on the property's own website than on a third-party platform.",
  },
  {
    number: "02",
    title: "Show the property accurately",
    description:
      "Photography, room details, amenities, policies and pricing context should create confidence rather than exaggerating what the guest will receive.",
  },
  {
    number: "03",
    title: "Automate predictable communication",
    description:
      "Routine messages can be automated while keeping staff involvement available for exceptions, questions and higher-value guest interactions.",
  },
  {
    number: "04",
    title: "Measure bookings, not vanity metrics",
    description:
      "Traffic, reach and engagement matter only when they can be related to actual enquiries, reservations or other meaningful commercial outcomes.",
  },
];

export const hospitalityJourney: HospitalityJourney[] = [
  {
    number: "01",
    title: "Discover",
    description:
      "The guest finds the property through search, advertising, social media, referrals or another discovery channel.",
  },
  {
    number: "02",
    title: "Evaluate",
    description:
      "Rooms, amenities, location, policies, imagery and reviews help the guest decide whether the property fits the stay.",
  },
  {
    number: "03",
    title: "Book",
    description:
      "The guest completes a direct reservation or enquiry through a clear, low-friction booking path.",
  },
  {
    number: "04",
    title: "Prepare",
    description:
      "Confirmation, arrival information and selected reminders are communicated before the stay.",
  },
  {
    number: "05",
    title: "Stay",
    description:
      "Operational systems support staff with the information needed to deliver the guest experience.",
  },
  {
    number: "06",
    title: "Return",
    description:
      "Post-stay communication, direct relationships and reputation signals can support repeat business and future discovery.",
  },
];
