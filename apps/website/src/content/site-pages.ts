export interface SitePage {
  title: string;
  path: string;
  eyebrow: string;
  summary: string;
  parentPath: string | null;
  childPaths: string[];
  noindex: boolean;
}

export const sitePages: SitePage[] = [
  {
    title: "About Us",
    path: "about",
    eyebrow: "Company",
    summary:
      "Learn about LKProfessionals, our history, principles, team and approach to reliable technology delivery.",
    parentPath: null,
    childPaths: [
      "about/our-story",
      "about/mission-vision",
      "about/why-choose-lkp",
      "about/our-process",
      "about/our-team",
      "about/careers",
      "about/contact",
    ],
    noindex: false,
  },
  {
    title: "Our Story",
    path: "about/our-story",
    eyebrow: "About Us",
    summary:
      "Learn more about our story within the LKProfessionals about us section.",
    parentPath: "about",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Our Mission & Vision",
    path: "about/mission-vision",
    eyebrow: "About Us",
    summary:
      "Learn more about our mission & vision within the LKProfessionals about us section.",
    parentPath: "about",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Why Choose LKP",
    path: "about/why-choose-lkp",
    eyebrow: "About Us",
    summary:
      "Learn more about why choose lkp within the LKProfessionals about us section.",
    parentPath: "about",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Our Process",
    path: "about/our-process",
    eyebrow: "About Us",
    summary:
      "Learn more about our process within the LKProfessionals about us section.",
    parentPath: "about",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Our Team",
    path: "about/our-team",
    eyebrow: "About Us",
    summary:
      "Learn more about our team within the LKProfessionals about us section.",
    parentPath: "about",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Careers",
    path: "about/careers",
    eyebrow: "About Us",
    summary:
      "Learn more about careers within the LKProfessionals about us section.",
    parentPath: "about",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Contact Us",
    path: "about/contact",
    eyebrow: "About Us",
    summary:
      "Learn more about contact us within the LKProfessionals about us section.",
    parentPath: "about",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Services",
    path: "services",
    eyebrow: "Capabilities",
    summary:
      "Explore technology, software, digital growth, infrastructure and business support services from LKProfessionals.",
    parentPath: null,
    childPaths: [
      "services/web-development",
      "services/software-development",
      "services/mobile-app-development",
      "services/ai-solutions",
      "services/digital-marketing",
      "services/branding-design",
      "services/cloud-hosting",
      "services/it-consultancy",
      "services/cybersecurity",
      "services/api-integration",
      "services/business-automation",
      "services/data-analytics",
      "services/maintenance-support",
    ],
    noindex: false,
  },
  {
    title: "Web Development",
    path: "services/web-development",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals web development services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/web-development/business-websites",
      "services/web-development/corporate-websites",
      "services/web-development/ecommerce-websites",
      "services/web-development/landing-pages",
      "services/web-development/booking-websites",
      "services/web-development/custom-web-applications",
      "services/web-development/website-redesign",
      "services/web-development/website-maintenance",
    ],
    noindex: false,
  },
  {
    title: "Business Websites",
    path: "services/web-development/business-websites",
    eyebrow: "Web Development",
    summary:
      "Learn more about business websites within the LKProfessionals web development section.",
    parentPath: "services/web-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Corporate Websites",
    path: "services/web-development/corporate-websites",
    eyebrow: "Web Development",
    summary:
      "Learn more about corporate websites within the LKProfessionals web development section.",
    parentPath: "services/web-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "E-commerce Websites",
    path: "services/web-development/ecommerce-websites",
    eyebrow: "Web Development",
    summary:
      "Learn more about e-commerce websites within the LKProfessionals web development section.",
    parentPath: "services/web-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Landing Pages",
    path: "services/web-development/landing-pages",
    eyebrow: "Web Development",
    summary:
      "Learn more about landing pages within the LKProfessionals web development section.",
    parentPath: "services/web-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Booking Websites",
    path: "services/web-development/booking-websites",
    eyebrow: "Web Development",
    summary:
      "Learn more about booking websites within the LKProfessionals web development section.",
    parentPath: "services/web-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Custom Web Applications",
    path: "services/web-development/custom-web-applications",
    eyebrow: "Web Development",
    summary:
      "Learn more about custom web applications within the LKProfessionals web development section.",
    parentPath: "services/web-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Website Redesign",
    path: "services/web-development/website-redesign",
    eyebrow: "Web Development",
    summary:
      "Learn more about website redesign within the LKProfessionals web development section.",
    parentPath: "services/web-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Website Maintenance",
    path: "services/web-development/website-maintenance",
    eyebrow: "Web Development",
    summary:
      "Learn more about website maintenance within the LKProfessionals web development section.",
    parentPath: "services/web-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Software Development",
    path: "services/software-development",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals software development services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/software-development/custom-software",
      "services/software-development/erp-development",
      "services/software-development/crm-development",
      "services/software-development/pos-systems",
      "services/software-development/inventory-systems",
      "services/software-development/hrm-systems",
      "services/software-development/accounting-systems",
      "services/software-development/saas-development",
    ],
    noindex: false,
  },
  {
    title: "Custom Software",
    path: "services/software-development/custom-software",
    eyebrow: "Software Development",
    summary:
      "Learn more about custom software within the LKProfessionals software development section.",
    parentPath: "services/software-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "ERP Development",
    path: "services/software-development/erp-development",
    eyebrow: "Software Development",
    summary:
      "Learn more about erp development within the LKProfessionals software development section.",
    parentPath: "services/software-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "CRM Development",
    path: "services/software-development/crm-development",
    eyebrow: "Software Development",
    summary:
      "Learn more about crm development within the LKProfessionals software development section.",
    parentPath: "services/software-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "POS Systems",
    path: "services/software-development/pos-systems",
    eyebrow: "Software Development",
    summary:
      "Learn more about pos systems within the LKProfessionals software development section.",
    parentPath: "services/software-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Inventory Systems",
    path: "services/software-development/inventory-systems",
    eyebrow: "Software Development",
    summary:
      "Learn more about inventory systems within the LKProfessionals software development section.",
    parentPath: "services/software-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "HRM Systems",
    path: "services/software-development/hrm-systems",
    eyebrow: "Software Development",
    summary:
      "Learn more about hrm systems within the LKProfessionals software development section.",
    parentPath: "services/software-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Accounting Systems",
    path: "services/software-development/accounting-systems",
    eyebrow: "Software Development",
    summary:
      "Learn more about accounting systems within the LKProfessionals software development section.",
    parentPath: "services/software-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "SaaS Development",
    path: "services/software-development/saas-development",
    eyebrow: "Software Development",
    summary:
      "Learn more about saas development within the LKProfessionals software development section.",
    parentPath: "services/software-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Mobile App Development",
    path: "services/mobile-app-development",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals mobile app development services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/mobile-app-development/android-apps",
      "services/mobile-app-development/ios-apps",
      "services/mobile-app-development/cross-platform-apps",
      "services/mobile-app-development/business-apps",
    ],
    noindex: false,
  },
  {
    title: "Android Apps",
    path: "services/mobile-app-development/android-apps",
    eyebrow: "Mobile App Development",
    summary:
      "Learn more about android apps within the LKProfessionals mobile app development section.",
    parentPath: "services/mobile-app-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "iOS Apps",
    path: "services/mobile-app-development/ios-apps",
    eyebrow: "Mobile App Development",
    summary:
      "Learn more about ios apps within the LKProfessionals mobile app development section.",
    parentPath: "services/mobile-app-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Cross Platform Apps",
    path: "services/mobile-app-development/cross-platform-apps",
    eyebrow: "Mobile App Development",
    summary:
      "Learn more about cross platform apps within the LKProfessionals mobile app development section.",
    parentPath: "services/mobile-app-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Business Apps",
    path: "services/mobile-app-development/business-apps",
    eyebrow: "Mobile App Development",
    summary:
      "Learn more about business apps within the LKProfessionals mobile app development section.",
    parentPath: "services/mobile-app-development",
    childPaths: [],
    noindex: false,
  },
  {
    title: "AI Solutions",
    path: "services/ai-solutions",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals ai solutions services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/ai-solutions/ai-chatbots",
      "services/ai-solutions/ai-automation",
      "services/ai-solutions/ai-assistants",
      "services/ai-solutions/ai-integration",
      "services/ai-solutions/custom-ai-solutions",
    ],
    noindex: false,
  },
  {
    title: "AI Chatbots",
    path: "services/ai-solutions/ai-chatbots",
    eyebrow: "AI Solutions",
    summary:
      "Learn more about ai chatbots within the LKProfessionals ai solutions section.",
    parentPath: "services/ai-solutions",
    childPaths: [],
    noindex: false,
  },
  {
    title: "AI Automation",
    path: "services/ai-solutions/ai-automation",
    eyebrow: "AI Solutions",
    summary:
      "Learn more about ai automation within the LKProfessionals ai solutions section.",
    parentPath: "services/ai-solutions",
    childPaths: [],
    noindex: false,
  },
  {
    title: "AI Assistants",
    path: "services/ai-solutions/ai-assistants",
    eyebrow: "AI Solutions",
    summary:
      "Learn more about ai assistants within the LKProfessionals ai solutions section.",
    parentPath: "services/ai-solutions",
    childPaths: [],
    noindex: false,
  },
  {
    title: "AI Integration",
    path: "services/ai-solutions/ai-integration",
    eyebrow: "AI Solutions",
    summary:
      "Learn more about ai integration within the LKProfessionals ai solutions section.",
    parentPath: "services/ai-solutions",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Custom AI Solutions",
    path: "services/ai-solutions/custom-ai-solutions",
    eyebrow: "AI Solutions",
    summary:
      "Learn more about custom ai solutions within the LKProfessionals ai solutions section.",
    parentPath: "services/ai-solutions",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Digital Marketing",
    path: "services/digital-marketing",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals digital marketing services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/digital-marketing/seo",
      "services/digital-marketing/local-seo",
      "services/digital-marketing/google-ads",
      "services/digital-marketing/social-media-marketing",
      "services/digital-marketing/email-marketing",
      "services/digital-marketing/content-marketing",
      "services/digital-marketing/marketing-automation",
    ],
    noindex: false,
  },
  {
    title: "SEO",
    path: "services/digital-marketing/seo",
    eyebrow: "Digital Marketing",
    summary:
      "Learn more about seo within the LKProfessionals digital marketing section.",
    parentPath: "services/digital-marketing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Local SEO",
    path: "services/digital-marketing/local-seo",
    eyebrow: "Digital Marketing",
    summary:
      "Learn more about local seo within the LKProfessionals digital marketing section.",
    parentPath: "services/digital-marketing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Google Ads",
    path: "services/digital-marketing/google-ads",
    eyebrow: "Digital Marketing",
    summary:
      "Learn more about google ads within the LKProfessionals digital marketing section.",
    parentPath: "services/digital-marketing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Social Media Marketing",
    path: "services/digital-marketing/social-media-marketing",
    eyebrow: "Digital Marketing",
    summary:
      "Learn more about social media marketing within the LKProfessionals digital marketing section.",
    parentPath: "services/digital-marketing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Email Marketing",
    path: "services/digital-marketing/email-marketing",
    eyebrow: "Digital Marketing",
    summary:
      "Learn more about email marketing within the LKProfessionals digital marketing section.",
    parentPath: "services/digital-marketing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Content Marketing",
    path: "services/digital-marketing/content-marketing",
    eyebrow: "Digital Marketing",
    summary:
      "Learn more about content marketing within the LKProfessionals digital marketing section.",
    parentPath: "services/digital-marketing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Marketing Automation",
    path: "services/digital-marketing/marketing-automation",
    eyebrow: "Digital Marketing",
    summary:
      "Learn more about marketing automation within the LKProfessionals digital marketing section.",
    parentPath: "services/digital-marketing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Branding & Design",
    path: "services/branding-design",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals branding & design services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/branding-design/logo-design",
      "services/branding-design/brand-identity",
      "services/branding-design/ui-ux-design",
      "services/branding-design/graphic-design",
    ],
    noindex: false,
  },
  {
    title: "Logo Design",
    path: "services/branding-design/logo-design",
    eyebrow: "Branding & Design",
    summary:
      "Learn more about logo design within the LKProfessionals branding & design section.",
    parentPath: "services/branding-design",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Brand Identity",
    path: "services/branding-design/brand-identity",
    eyebrow: "Branding & Design",
    summary:
      "Learn more about brand identity within the LKProfessionals branding & design section.",
    parentPath: "services/branding-design",
    childPaths: [],
    noindex: false,
  },
  {
    title: "UI/UX Design",
    path: "services/branding-design/ui-ux-design",
    eyebrow: "Branding & Design",
    summary:
      "Learn more about ui/ux design within the LKProfessionals branding & design section.",
    parentPath: "services/branding-design",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Graphic Design",
    path: "services/branding-design/graphic-design",
    eyebrow: "Branding & Design",
    summary:
      "Learn more about graphic design within the LKProfessionals branding & design section.",
    parentPath: "services/branding-design",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Cloud & Hosting",
    path: "services/cloud-hosting",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals cloud & hosting services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/cloud-hosting/web-hosting",
      "services/cloud-hosting/vps-hosting",
      "services/cloud-hosting/domain-registration",
      "services/cloud-hosting/business-email",
      "services/cloud-hosting/ssl-certificates",
    ],
    noindex: false,
  },
  {
    title: "Web Hosting",
    path: "services/cloud-hosting/web-hosting",
    eyebrow: "Cloud & Hosting",
    summary:
      "Learn more about web hosting within the LKProfessionals cloud & hosting section.",
    parentPath: "services/cloud-hosting",
    childPaths: [],
    noindex: false,
  },
  {
    title: "VPS Hosting",
    path: "services/cloud-hosting/vps-hosting",
    eyebrow: "Cloud & Hosting",
    summary:
      "Learn more about vps hosting within the LKProfessionals cloud & hosting section.",
    parentPath: "services/cloud-hosting",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Domain Registration",
    path: "services/cloud-hosting/domain-registration",
    eyebrow: "Cloud & Hosting",
    summary:
      "Learn more about domain registration within the LKProfessionals cloud & hosting section.",
    parentPath: "services/cloud-hosting",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Business Email",
    path: "services/cloud-hosting/business-email",
    eyebrow: "Cloud & Hosting",
    summary:
      "Learn more about business email within the LKProfessionals cloud & hosting section.",
    parentPath: "services/cloud-hosting",
    childPaths: [],
    noindex: false,
  },
  {
    title: "SSL Certificates",
    path: "services/cloud-hosting/ssl-certificates",
    eyebrow: "Cloud & Hosting",
    summary:
      "Learn more about ssl certificates within the LKProfessionals cloud & hosting section.",
    parentPath: "services/cloud-hosting",
    childPaths: [],
    noindex: false,
  },
  {
    title: "IT Consultancy",
    path: "services/it-consultancy",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals it consultancy services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/it-consultancy/digital-transformation",
      "services/it-consultancy/technology-consulting",
      "services/it-consultancy/system-integration",
      "services/it-consultancy/project-consulting",
    ],
    noindex: false,
  },
  {
    title: "Digital Transformation",
    path: "services/it-consultancy/digital-transformation",
    eyebrow: "IT Consultancy",
    summary:
      "Learn more about digital transformation within the LKProfessionals it consultancy section.",
    parentPath: "services/it-consultancy",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Technology Consulting",
    path: "services/it-consultancy/technology-consulting",
    eyebrow: "IT Consultancy",
    summary:
      "Learn more about technology consulting within the LKProfessionals it consultancy section.",
    parentPath: "services/it-consultancy",
    childPaths: [],
    noindex: false,
  },
  {
    title: "System Integration",
    path: "services/it-consultancy/system-integration",
    eyebrow: "IT Consultancy",
    summary:
      "Learn more about system integration within the LKProfessionals it consultancy section.",
    parentPath: "services/it-consultancy",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Project Consulting",
    path: "services/it-consultancy/project-consulting",
    eyebrow: "IT Consultancy",
    summary:
      "Learn more about project consulting within the LKProfessionals it consultancy section.",
    parentPath: "services/it-consultancy",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Cybersecurity",
    path: "services/cybersecurity",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals cybersecurity services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/cybersecurity/security-audit",
      "services/cybersecurity/website-security",
      "services/cybersecurity/backup-recovery",
      "services/cybersecurity/security-hardening",
    ],
    noindex: false,
  },
  {
    title: "Security Audit",
    path: "services/cybersecurity/security-audit",
    eyebrow: "Cybersecurity",
    summary:
      "Learn more about security audit within the LKProfessionals cybersecurity section.",
    parentPath: "services/cybersecurity",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Website Security",
    path: "services/cybersecurity/website-security",
    eyebrow: "Cybersecurity",
    summary:
      "Learn more about website security within the LKProfessionals cybersecurity section.",
    parentPath: "services/cybersecurity",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Backup & Recovery",
    path: "services/cybersecurity/backup-recovery",
    eyebrow: "Cybersecurity",
    summary:
      "Learn more about backup & recovery within the LKProfessionals cybersecurity section.",
    parentPath: "services/cybersecurity",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Security Hardening",
    path: "services/cybersecurity/security-hardening",
    eyebrow: "Cybersecurity",
    summary:
      "Learn more about security hardening within the LKProfessionals cybersecurity section.",
    parentPath: "services/cybersecurity",
    childPaths: [],
    noindex: false,
  },
  {
    title: "API & Integration",
    path: "services/api-integration",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals api & integration services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/api-integration/payment-gateway",
      "services/api-integration/whatsapp-api",
      "services/api-integration/sms-gateway",
      "services/api-integration/crm-integration",
      "services/api-integration/erp-integration",
    ],
    noindex: false,
  },
  {
    title: "Payment Gateway",
    path: "services/api-integration/payment-gateway",
    eyebrow: "API & Integration",
    summary:
      "Learn more about payment gateway within the LKProfessionals api & integration section.",
    parentPath: "services/api-integration",
    childPaths: [],
    noindex: false,
  },
  {
    title: "WhatsApp API",
    path: "services/api-integration/whatsapp-api",
    eyebrow: "API & Integration",
    summary:
      "Learn more about whatsapp api within the LKProfessionals api & integration section.",
    parentPath: "services/api-integration",
    childPaths: [],
    noindex: false,
  },
  {
    title: "SMS Gateway",
    path: "services/api-integration/sms-gateway",
    eyebrow: "API & Integration",
    summary:
      "Learn more about sms gateway within the LKProfessionals api & integration section.",
    parentPath: "services/api-integration",
    childPaths: [],
    noindex: false,
  },
  {
    title: "CRM Integration",
    path: "services/api-integration/crm-integration",
    eyebrow: "API & Integration",
    summary:
      "Learn more about crm integration within the LKProfessionals api & integration section.",
    parentPath: "services/api-integration",
    childPaths: [],
    noindex: false,
  },
  {
    title: "ERP Integration",
    path: "services/api-integration/erp-integration",
    eyebrow: "API & Integration",
    summary:
      "Learn more about erp integration within the LKProfessionals api & integration section.",
    parentPath: "services/api-integration",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Business Automation",
    path: "services/business-automation",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals business automation services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/business-automation/workflow-automation",
      "services/business-automation/crm-automation",
      "services/business-automation/hr-automation",
      "services/business-automation/document-automation",
    ],
    noindex: false,
  },
  {
    title: "Workflow Automation",
    path: "services/business-automation/workflow-automation",
    eyebrow: "Business Automation",
    summary:
      "Learn more about workflow automation within the LKProfessionals business automation section.",
    parentPath: "services/business-automation",
    childPaths: [],
    noindex: false,
  },
  {
    title: "CRM Automation",
    path: "services/business-automation/crm-automation",
    eyebrow: "Business Automation",
    summary:
      "Learn more about crm automation within the LKProfessionals business automation section.",
    parentPath: "services/business-automation",
    childPaths: [],
    noindex: false,
  },
  {
    title: "HR Automation",
    path: "services/business-automation/hr-automation",
    eyebrow: "Business Automation",
    summary:
      "Learn more about hr automation within the LKProfessionals business automation section.",
    parentPath: "services/business-automation",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Document Automation",
    path: "services/business-automation/document-automation",
    eyebrow: "Business Automation",
    summary:
      "Learn more about document automation within the LKProfessionals business automation section.",
    parentPath: "services/business-automation",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Data & Analytics",
    path: "services/data-analytics",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals data & analytics services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/data-analytics/business-intelligence",
      "services/data-analytics/dashboards",
      "services/data-analytics/reports",
      "services/data-analytics/kpi-tracking",
    ],
    noindex: false,
  },
  {
    title: "Business Intelligence",
    path: "services/data-analytics/business-intelligence",
    eyebrow: "Data & Analytics",
    summary:
      "Learn more about business intelligence within the LKProfessionals data & analytics section.",
    parentPath: "services/data-analytics",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Dashboards",
    path: "services/data-analytics/dashboards",
    eyebrow: "Data & Analytics",
    summary:
      "Learn more about dashboards within the LKProfessionals data & analytics section.",
    parentPath: "services/data-analytics",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Reports",
    path: "services/data-analytics/reports",
    eyebrow: "Data & Analytics",
    summary:
      "Learn more about reports within the LKProfessionals data & analytics section.",
    parentPath: "services/data-analytics",
    childPaths: [],
    noindex: false,
  },
  {
    title: "KPI Tracking",
    path: "services/data-analytics/kpi-tracking",
    eyebrow: "Data & Analytics",
    summary:
      "Learn more about kpi tracking within the LKProfessionals data & analytics section.",
    parentPath: "services/data-analytics",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Maintenance & Support",
    path: "services/maintenance-support",
    eyebrow: "Services",
    summary:
      "Explore LKProfessionals maintenance & support services, capabilities and delivery approach.",
    parentPath: "services",
    childPaths: [
      "services/maintenance-support/website-maintenance",
      "services/maintenance-support/software-maintenance",
      "services/maintenance-support/performance-optimization",
      "services/maintenance-support/technical-support",
    ],
    noindex: false,
  },
  {
    title: "Website Maintenance",
    path: "services/maintenance-support/website-maintenance",
    eyebrow: "Maintenance & Support",
    summary:
      "Learn more about website maintenance within the LKProfessionals maintenance & support section.",
    parentPath: "services/maintenance-support",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Software Maintenance",
    path: "services/maintenance-support/software-maintenance",
    eyebrow: "Maintenance & Support",
    summary:
      "Learn more about software maintenance within the LKProfessionals maintenance & support section.",
    parentPath: "services/maintenance-support",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Performance Optimization",
    path: "services/maintenance-support/performance-optimization",
    eyebrow: "Maintenance & Support",
    summary:
      "Learn more about performance optimization within the LKProfessionals maintenance & support section.",
    parentPath: "services/maintenance-support",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Technical Support",
    path: "services/maintenance-support/technical-support",
    eyebrow: "Maintenance & Support",
    summary:
      "Learn more about technical support within the LKProfessionals maintenance & support section.",
    parentPath: "services/maintenance-support",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Industries",
    path: "industries",
    eyebrow: "Industry Experience",
    summary:
      "Technology services adapted to the operating realities of different industries.",
    parentPath: null,
    childPaths: [
      "industries/small-business",
      "industries/enterprise",
      "industries/healthcare",
      "industries/education",
      "industries/hospitality",
      "industries/retail-ecommerce",
      "industries/manufacturing",
      "industries/construction",
      "industries/logistics",
      "industries/finance",
      "industries/government",
      "industries/non-profit",
    ],
    noindex: false,
  },
  {
    title: "Small Business",
    path: "industries/small-business",
    eyebrow: "Industries",
    summary:
      "Learn more about small business within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Enterprise",
    path: "industries/enterprise",
    eyebrow: "Industries",
    summary:
      "Learn more about enterprise within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Healthcare",
    path: "industries/healthcare",
    eyebrow: "Industries",
    summary:
      "Learn more about healthcare within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Education",
    path: "industries/education",
    eyebrow: "Industries",
    summary:
      "Learn more about education within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Hospitality",
    path: "industries/hospitality",
    eyebrow: "Industries",
    summary:
      "Learn more about hospitality within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Retail & E-commerce",
    path: "industries/retail-ecommerce",
    eyebrow: "Industries",
    summary:
      "Learn more about retail & e-commerce within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Manufacturing",
    path: "industries/manufacturing",
    eyebrow: "Industries",
    summary:
      "Learn more about manufacturing within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Construction",
    path: "industries/construction",
    eyebrow: "Industries",
    summary:
      "Learn more about construction within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Logistics",
    path: "industries/logistics",
    eyebrow: "Industries",
    summary:
      "Learn more about logistics within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Finance",
    path: "industries/finance",
    eyebrow: "Industries",
    summary:
      "Learn more about finance within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Government",
    path: "industries/government",
    eyebrow: "Industries",
    summary:
      "Learn more about government within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Non-profit",
    path: "industries/non-profit",
    eyebrow: "Industries",
    summary:
      "Learn more about non-profit within the LKProfessionals industries section.",
    parentPath: "industries",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Case Studies",
    path: "case-studies",
    eyebrow: "Our Work",
    summary:
      "Selected examples of business challenges, technical decisions and results delivered by LKProfessionals.",
    parentPath: null,
    childPaths: [
      "case-studies/web-development",
      "case-studies/software-development",
      "case-studies/seo",
      "case-studies/digital-marketing",
      "case-studies/mobile-apps",
    ],
    noindex: false,
  },
  {
    title: "Web Development",
    path: "case-studies/web-development",
    eyebrow: "Case Studies",
    summary:
      "Learn more about web development within the LKProfessionals case studies section.",
    parentPath: "case-studies",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Software Development",
    path: "case-studies/software-development",
    eyebrow: "Case Studies",
    summary:
      "Learn more about software development within the LKProfessionals case studies section.",
    parentPath: "case-studies",
    childPaths: [],
    noindex: false,
  },
  {
    title: "SEO",
    path: "case-studies/seo",
    eyebrow: "Case Studies",
    summary:
      "Learn more about seo within the LKProfessionals case studies section.",
    parentPath: "case-studies",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Digital Marketing",
    path: "case-studies/digital-marketing",
    eyebrow: "Case Studies",
    summary:
      "Learn more about digital marketing within the LKProfessionals case studies section.",
    parentPath: "case-studies",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Mobile Apps",
    path: "case-studies/mobile-apps",
    eyebrow: "Case Studies",
    summary:
      "Learn more about mobile apps within the LKProfessionals case studies section.",
    parentPath: "case-studies",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Insights",
    path: "insights",
    eyebrow: "Knowledge",
    summary:
      "Practical articles, company updates and technical guidance for business leaders and delivery teams.",
    parentPath: null,
    childPaths: [
      "insights/blog",
      "insights/news",
      "insights/seo-tips",
      "insights/ai",
      "insights/web-development",
      "insights/software-development",
      "insights/digital-marketing",
      "insights/business-growth",
      "insights/tutorials",
    ],
    noindex: false,
  },
  {
    title: "Blog",
    path: "insights/blog",
    eyebrow: "Insights",
    summary:
      "Learn more about blog within the LKProfessionals insights section.",
    parentPath: "insights",
    childPaths: [],
    noindex: false,
  },
  {
    title: "News",
    path: "insights/news",
    eyebrow: "Insights",
    summary:
      "Learn more about news within the LKProfessionals insights section.",
    parentPath: "insights",
    childPaths: [],
    noindex: false,
  },
  {
    title: "SEO Tips",
    path: "insights/seo-tips",
    eyebrow: "Insights",
    summary:
      "Learn more about seo tips within the LKProfessionals insights section.",
    parentPath: "insights",
    childPaths: [],
    noindex: false,
  },
  {
    title: "AI",
    path: "insights/ai",
    eyebrow: "Insights",
    summary: "Learn more about ai within the LKProfessionals insights section.",
    parentPath: "insights",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Web Development",
    path: "insights/web-development",
    eyebrow: "Insights",
    summary:
      "Learn more about web development within the LKProfessionals insights section.",
    parentPath: "insights",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Software Development",
    path: "insights/software-development",
    eyebrow: "Insights",
    summary:
      "Learn more about software development within the LKProfessionals insights section.",
    parentPath: "insights",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Digital Marketing",
    path: "insights/digital-marketing",
    eyebrow: "Insights",
    summary:
      "Learn more about digital marketing within the LKProfessionals insights section.",
    parentPath: "insights",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Business Growth",
    path: "insights/business-growth",
    eyebrow: "Insights",
    summary:
      "Learn more about business growth within the LKProfessionals insights section.",
    parentPath: "insights",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Tutorials",
    path: "insights/tutorials",
    eyebrow: "Insights",
    summary:
      "Learn more about tutorials within the LKProfessionals insights section.",
    parentPath: "insights",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Portfolio",
    path: "portfolio",
    eyebrow: "Portfolio",
    summary:
      "Explore selected websites, software, mobile applications, branding and marketing work.",
    parentPath: null,
    childPaths: [
      "portfolio/websites",
      "portfolio/software",
      "portfolio/mobile-apps",
      "portfolio/branding",
      "portfolio/marketing",
    ],
    noindex: false,
  },
  {
    title: "Websites",
    path: "portfolio/websites",
    eyebrow: "Portfolio",
    summary:
      "Learn more about websites within the LKProfessionals portfolio section.",
    parentPath: "portfolio",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Software",
    path: "portfolio/software",
    eyebrow: "Portfolio",
    summary:
      "Learn more about software within the LKProfessionals portfolio section.",
    parentPath: "portfolio",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Mobile Apps",
    path: "portfolio/mobile-apps",
    eyebrow: "Portfolio",
    summary:
      "Learn more about mobile apps within the LKProfessionals portfolio section.",
    parentPath: "portfolio",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Branding",
    path: "portfolio/branding",
    eyebrow: "Portfolio",
    summary:
      "Learn more about branding within the LKProfessionals portfolio section.",
    parentPath: "portfolio",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Marketing",
    path: "portfolio/marketing",
    eyebrow: "Portfolio",
    summary:
      "Learn more about marketing within the LKProfessionals portfolio section.",
    parentPath: "portfolio",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Pricing",
    path: "pricing",
    eyebrow: "Pricing",
    summary:
      "Review structured service options or request a quotation based on specific requirements.",
    parentPath: null,
    childPaths: [
      "pricing/website-packages",
      "pricing/seo-packages",
      "pricing/digital-marketing-packages",
      "pricing/maintenance-packages",
      "pricing/custom-quote",
    ],
    noindex: false,
  },
  {
    title: "Website Packages",
    path: "pricing/website-packages",
    eyebrow: "Pricing",
    summary:
      "Learn more about website packages within the LKProfessionals pricing section.",
    parentPath: "pricing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "SEO Packages",
    path: "pricing/seo-packages",
    eyebrow: "Pricing",
    summary:
      "Learn more about seo packages within the LKProfessionals pricing section.",
    parentPath: "pricing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Digital Marketing Packages",
    path: "pricing/digital-marketing-packages",
    eyebrow: "Pricing",
    summary:
      "Learn more about digital marketing packages within the LKProfessionals pricing section.",
    parentPath: "pricing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Maintenance Packages",
    path: "pricing/maintenance-packages",
    eyebrow: "Pricing",
    summary:
      "Learn more about maintenance packages within the LKProfessionals pricing section.",
    parentPath: "pricing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Custom Quote",
    path: "pricing/custom-quote",
    eyebrow: "Pricing",
    summary:
      "Learn more about custom quote within the LKProfessionals pricing section.",
    parentPath: "pricing",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Testimonials",
    path: "testimonials",
    eyebrow: "Client Experience",
    summary: "Read feedback from clients who have worked with LKProfessionals.",
    parentPath: null,
    childPaths: [],
    noindex: false,
  },
  {
    title: "Frequently Asked Questions",
    path: "faq",
    eyebrow: "FAQ",
    summary:
      "Answers about services, delivery, pricing, support and working with LKProfessionals.",
    parentPath: null,
    childPaths: [],
    noindex: false,
  },
  {
    title: "Resources",
    path: "resources",
    eyebrow: "Resources",
    summary:
      "Practical material supporting better technology and digital business decisions.",
    parentPath: null,
    childPaths: [
      "resources/downloads",
      "resources/guides",
      "resources/checklists",
      "resources/templates",
    ],
    noindex: false,
  },
  {
    title: "Downloads",
    path: "resources/downloads",
    eyebrow: "Resources",
    summary:
      "Learn more about downloads within the LKProfessionals resources section.",
    parentPath: "resources",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Guides",
    path: "resources/guides",
    eyebrow: "Resources",
    summary:
      "Learn more about guides within the LKProfessionals resources section.",
    parentPath: "resources",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Checklists",
    path: "resources/checklists",
    eyebrow: "Resources",
    summary:
      "Learn more about checklists within the LKProfessionals resources section.",
    parentPath: "resources",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Templates",
    path: "resources/templates",
    eyebrow: "Resources",
    summary:
      "Learn more about templates within the LKProfessionals resources section.",
    parentPath: "resources",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Get a Quote",
    path: "get-a-quote",
    eyebrow: "Start a Project",
    summary:
      "Tell us about your requirements and receive a practical quotation.",
    parentPath: null,
    childPaths: [],
    noindex: false,
  },
  {
    title: "Book a Consultation",
    path: "book-a-consultation",
    eyebrow: "Consultation",
    summary:
      "Arrange a focused discussion about your requirements and practical next steps.",
    parentPath: null,
    childPaths: [],
    noindex: false,
  },
  {
    title: "Contact Us",
    path: "contact",
    eyebrow: "Contact",
    summary:
      "Contact LKProfessionals for sales, support and general enquiries.",
    parentPath: null,
    childPaths: ["contact/general-enquiry", "contact/support", "contact/sales"],
    noindex: false,
  },
  {
    title: "General Enquiry",
    path: "contact/general-enquiry",
    eyebrow: "Contact Us",
    summary:
      "Learn more about general enquiry within the LKProfessionals contact us section.",
    parentPath: "contact",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Support",
    path: "contact/support",
    eyebrow: "Contact Us",
    summary:
      "Learn more about support within the LKProfessionals contact us section.",
    parentPath: "contact",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Sales",
    path: "contact/sales",
    eyebrow: "Contact Us",
    summary:
      "Learn more about sales within the LKProfessionals contact us section.",
    parentPath: "contact",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Client Portal",
    path: "client-portal",
    eyebrow: "Client Access",
    summary:
      "Secure client access to projects, invoices, support requests and shared documents.",
    parentPath: null,
    childPaths: [
      "client-portal/login",
      "client-portal/dashboard",
      "client-portal/projects",
      "client-portal/invoices",
      "client-portal/support-tickets",
      "client-portal/documents",
    ],
    noindex: true,
  },
  {
    title: "Login",
    path: "client-portal/login",
    eyebrow: "Client Portal",
    summary:
      "Learn more about login within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Dashboard",
    path: "client-portal/dashboard",
    eyebrow: "Client Portal",
    summary:
      "Learn more about dashboard within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Projects",
    path: "client-portal/projects",
    eyebrow: "Client Portal",
    summary:
      "Learn more about projects within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Invoices",
    path: "client-portal/invoices",
    eyebrow: "Client Portal",
    summary:
      "Learn more about invoices within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Support Tickets",
    path: "client-portal/support-tickets",
    eyebrow: "Client Portal",
    summary:
      "Learn more about support tickets within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Documents",
    path: "client-portal/documents",
    eyebrow: "Client Portal",
    summary:
      "Learn more about documents within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Legal",
    path: "legal",
    eyebrow: "Legal",
    summary:
      "Policies and terms governing LKProfessionals websites and commercial engagements.",
    parentPath: null,
    childPaths: [
      "legal/privacy-policy",
      "legal/terms-conditions",
      "legal/cookie-policy",
      "legal/refund-policy",
      "legal/sitemap",
    ],
    noindex: false,
  },
  {
    title: "Privacy Policy",
    path: "legal/privacy-policy",
    eyebrow: "Legal",
    summary:
      "Learn more about privacy policy within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Terms & Conditions",
    path: "legal/terms-conditions",
    eyebrow: "Legal",
    summary:
      "Learn more about terms & conditions within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Cookie Policy",
    path: "legal/cookie-policy",
    eyebrow: "Legal",
    summary:
      "Learn more about cookie policy within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Refund Policy",
    path: "legal/refund-policy",
    eyebrow: "Legal",
    summary:
      "Learn more about refund policy within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Sitemap",
    path: "legal/sitemap",
    eyebrow: "Legal",
    summary:
      "Learn more about sitemap within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
];

export const sitePageByPath = new Map(
  sitePages.map((page) => [page.path, page]),
);
