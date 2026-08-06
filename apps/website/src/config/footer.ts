export interface FooterLink {
  label: string;
  href: string;
}

export interface SocialLink extends FooterLink {
  platform: "linkedin" | "facebook" | "instagram" | "x" | "youtube" | "tiktok";
}

export const footerServices: FooterLink[] = [
  {
    label: "Web Development",
    href: "/services/web-development",
  },
  {
    label: "Software Development",
    href: "/services/software-development",
  },
  {
    label: "Mobile App Development",
    href: "/services/mobile-app-development",
  },
  {
    label: "AI Solutions",
    href: "/services/ai-solutions",
  },
  {
    label: "Digital Marketing",
    href: "/services/digital-marketing",
  },
  {
    label: "Branding & Design",
    href: "/services/branding-design",
  },
  {
    label: "Cloud & Hosting",
    href: "/services/cloud-hosting",
  },
  {
    label: "IT Consultancy",
    href: "/services/it-consultancy",
  },
  {
    label: "Cybersecurity",
    href: "/services/cybersecurity",
  },
  {
    label: "API & Integration",
    href: "/services/api-integration",
  },
  {
    label: "Business Automation",
    href: "/services/business-automation",
  },
  {
    label: "Data & Analytics",
    href: "/services/data-analytics",
  },
  {
    label: "Maintenance & Support",
    href: "/services/maintenance-support",
  },
];

export const footerKeyPages: FooterLink[] = [
  {
    label: "About Us",
    href: "/about",
  },
  {
    label: "Industries",
    href: "/industries",
  },
  {
    label: "Case Studies",
    href: "/case-studies",
  },
  {
    label: "Portfolio",
    href: "/portfolio",
  },
  {
    label: "Insights",
    href: "/insights",
  },
  {
    label: "Pricing",
    href: "/pricing",
  },
  {
    label: "Testimonials",
    href: "/testimonials",
  },
  {
    label: "Careers",
    href: "/about/careers",
  },
  {
    label: "Contact Us",
    href: "/contact",
  },
  {
    label: "Get a Quote",
    href: "/get-a-quote",
  },
];

export const footerLegalLinks: FooterLink[] = [
  {
    label: "Terms & Conditions",
    href: "/legal/terms-conditions",
  },
  {
    label: "Privacy Policy",
    href: "/legal/privacy-policy",
  },
  {
    label: "Cookie Policy",
    href: "/legal/cookie-policy",
  },
  {
    label: "Refund Policy",
    href: "/legal/refund-policy",
  },
];

export const footerSocialLinks: SocialLink[] = [
  {
    platform: "linkedin",
    label: "LinkedIn",
    href: "https://www.linkedin.com/company/lkprofessionals",
  },
  {
    platform: "facebook",
    label: "Facebook",
    href: "https://web.facebook.com/lkprofessionals",
  },
  {
    platform: "instagram",
    label: "Instagram",
    href: "https://www.instagram.com/lkprofessionalspvtltd/",
  },
  {
    platform: "x",
    label: "X",
    href: "https://x.com/lkprofess",
  },
  {
    platform: "youtube",
    label: "YouTube",
    href: "https://www.youtube.com/@lkprofessionals",
  },
  {
    platform: "tiktok",
    label: "TikTok",
    href: "https://www.tiktok.com/@lkprofessionals",
  },
];

export const footerContact = {
  address: "6/7, Vidhan's Lane, Eachchamoddai, Jaffna - 40000, Sri Lanka",
  email: "info@lkprofessionals.com",
  whatsappDisplay: "+94 76 123 4321",
  whatsappHref: "https://wa.me/94761234321",
} as const;
