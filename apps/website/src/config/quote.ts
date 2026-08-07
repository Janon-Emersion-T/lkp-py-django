export const quoteServices = [
  "Website Development",
  "E-commerce Development",
  "Custom Software Development",
  "Mobile App Development",
  "ERP Development",
  "CRM Development",
  "UI/UX Design",
  "Website Redesign",
  "Website Maintenance",
  "SEO Services",
  "Digital Marketing",
  "Google Ads Management",
  "Hosting & Domain",
  "IT Consultation",
  "Other",
] as const;

export const preferredContactMethods = [
  {
    value: "email",
    label: "Email",
  },
  {
    value: "whatsapp",
    label: "WhatsApp",
  },
] as const;

export const contactTimes = [
  {
    value: "",
    label: "Select a time",
  },
  {
    value: "morning",
    label: "Morning",
  },
  {
    value: "afternoon",
    label: "Afternoon",
  },
  {
    value: "evening",
    label: "Evening",
  },
  {
    value: "anytime",
    label: "Anytime",
  },
] as const;
