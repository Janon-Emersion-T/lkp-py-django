import {
  serviceFamilies,
  serviceGroups,
  servicePrinciples,
} from "../config/services";
import {
  aboutNavigation,
  caseStudiesNavigation,
  headerNavigation,
  industryNavigation,
  insightNavigation,
} from "../config/navigation";
import type { SitePage } from "./site-pages";

export interface FoundationPageSection {
  title: string;
  body: string;
}

export interface FoundationPageChecklist {
  title: string;
  items: string[];
}

export interface FoundationPageCta {
  title: string;
  body: string;
  primaryHref: string;
  primaryLabel: string;
  secondaryHref?: string;
  secondaryLabel?: string;
}

export interface FoundationPageContent {
  title: string;
  description: string;
  lead: string;
  contextLabel: string;
  overview: string[];
  highlights: FoundationPageChecklist[];
  sections: FoundationPageSection[];
  cta: FoundationPageCta;
}

const serviceFamilyByHref = new Map(
  serviceFamilies.map((family) => [
    family.href.replace(/^\/|\/$/g, ""),
    family,
  ]),
);

const serviceGroupByName = new Map(
  serviceGroups.map((group) => [group.name, group]),
);

const servicePageThemes: Record<
  string,
  {
    outcomes: string[];
    deliverables: string[];
    process: string[];
  }
> = {
  "business-websites": {
    outcomes: [
      "Present the company clearly to customers, partners and prospects.",
      "Support enquiries, consultation requests and structured lead capture.",
      "Create a website that staff can maintain without technical friction.",
    ],
    deliverables: [
      "Page structure aligned to the business offer.",
      "Lead capture forms, enquiry routes and content blocks.",
      "Performance, mobile and search-ready implementation.",
    ],
    process: [
      "Clarify audience, offers and trust signals.",
      "Translate the sales narrative into page structure and calls to action.",
      "Launch a maintainable site with measured improvements after release.",
    ],
  },
  "corporate-websites": {
    outcomes: [
      "Communicate credibility to stakeholders with a more formal structure.",
      "Support departments, leadership, services and investor-style information.",
      "Keep brand consistency across a large public-facing website.",
    ],
    deliverables: [
      "Structured information architecture for multi-section sites.",
      "Content patterns for governance, reputation and service clarity.",
      "Scalable implementation for updates across teams.",
    ],
    process: [
      "Review organisational structure and communication priorities.",
      "Design a hierarchy that helps different audiences find what matters.",
      "Build a resilient front-end with room for controlled growth.",
    ],
  },
  "ecommerce-websites": {
    outcomes: [
      "Make products easier to discover, compare and purchase.",
      "Reduce operational friction around catalogue, fulfilment and payments.",
      "Create a storefront that can support campaigns and repeat purchases.",
    ],
    deliverables: [
      "Product catalogue, collections and checkout flow.",
      "Payment, delivery and customer-notification integration.",
      "Operational support for stock, orders and reporting.",
    ],
    process: [
      "Map the buying journey from discovery to fulfilment.",
      "Connect the storefront to the business systems behind it.",
      "Improve conversion and operational handling after launch.",
    ],
  },
  "landing-pages": {
    outcomes: [
      "Support paid campaigns or single-offer promotions with focused messaging.",
      "Reduce distractions and push visitors toward one primary action.",
      "Make campaign performance easier to measure and improve.",
    ],
    deliverables: [
      "Single-goal page structure with strong calls to action.",
      "Conversion-focused content hierarchy and trust cues.",
      "Tracking support for campaign measurement.",
    ],
    process: [
      "Define the offer, audience and conversion action.",
      "Strip the page down to the arguments that matter.",
      "Refine based on campaign traffic and response patterns.",
    ],
  },
  "booking-websites": {
    outcomes: [
      "Allow customers to check availability and request or confirm bookings.",
      "Reduce manual coordination around appointments or reservations.",
      "Create a clearer experience for both staff and customers.",
    ],
    deliverables: [
      "Availability, booking and confirmation flows.",
      "Admin handling for requests, schedules or service slots.",
      "Notifications and follow-up touchpoints.",
    ],
    process: [
      "Map the booking workflow and operational rules.",
      "Build a front-end experience that matches staff capacity.",
      "Connect notifications and confirmations into the routine.",
    ],
  },
  "custom-web-applications": {
    outcomes: [
      "Handle browser-based workflows that go beyond brochure pages.",
      "Give teams secure access to operational features from anywhere.",
      "Create task-specific web tools without forcing a mobile download.",
    ],
    deliverables: [
      "Role-based workflow features and task-specific interfaces.",
      "Connection to APIs, databases and internal business rules.",
      "Operational reporting and extensible architecture.",
    ],
    process: [
      "Define the workflow, actors and business rules.",
      "Build the application around the operational sequence.",
      "Iterate with usage feedback once real work starts flowing through it.",
    ],
  },
  "website-redesign": {
    outcomes: [
      "Fix outdated messaging, structure or brand presentation.",
      "Improve conversion without losing established search or navigation value.",
      "Modernise the public experience while keeping business continuity.",
    ],
    deliverables: [
      "Audit of existing structure, friction points and opportunities.",
      "Reworked design direction, page hierarchy and content flow.",
      "Migration approach that protects core assets and user journeys.",
    ],
    process: [
      "Review what works and what creates friction today.",
      "Redesign around business objectives instead of cosmetic change alone.",
      "Launch with continuity, measurement and phased improvements.",
    ],
  },
  "website-maintenance": {
    outcomes: [
      "Keep the public website stable, current and safe to operate.",
      "Reduce the risk of ignored updates becoming larger failures later.",
      "Support incremental improvements without full rebuild cycles.",
    ],
    deliverables: [
      "Routine updates, issue response and content support.",
      "Monitoring for performance, uptime and basic reliability.",
      "Improvement backlog for practical ongoing changes.",
    ],
    process: [
      "Review the current stack and maintenance risks.",
      "Set a maintenance rhythm that suits the business.",
      "Track recurring fixes and convert them into durable improvements.",
    ],
  },
  "custom-software": {
    outcomes: [
      "Support workflows that off-the-shelf tools do not fit cleanly.",
      "Keep operational logic aligned to how the business actually works.",
      "Reduce manual work, duplication and workaround-heavy processes.",
    ],
    deliverables: [
      "Workflow-specific modules, permissions and business rules.",
      "Database structure and reporting suited to the operation.",
      "Implementation that can evolve with future needs.",
    ],
    process: [
      "Map responsibilities, approvals and data movement.",
      "Model the system around real operational decisions.",
      "Release in controlled phases to protect continuity.",
    ],
  },
  "erp-development": {
    outcomes: [
      "Bring finance, stock, projects or operations into a more unified system.",
      "Reduce fragmented spreadsheets and disconnected departmental processes.",
      "Improve visibility across multi-step business operations.",
    ],
    deliverables: [
      "Process mapping across departments and handoff points.",
      "ERP modules aligned to the business workflow.",
      "Structured reporting and operational visibility.",
    ],
    process: [
      "Define scope carefully to avoid overbuilding.",
      "Translate department-level responsibilities into system modules.",
      "Roll out in stages with training and migration support.",
    ],
  },
  "crm-development": {
    outcomes: [
      "Track leads, customers and follow-up activity more consistently.",
      "Make pipeline visibility clearer for sales or account teams.",
      "Reduce contact-history loss across staff changes or handovers.",
    ],
    deliverables: [
      "Lead, contact and account management workflows.",
      "Follow-up reminders, pipeline stages and visibility controls.",
      "Reporting for activity and response patterns.",
    ],
    process: [
      "Review how enquiries become qualified opportunities.",
      "Design stages and activity rules around the team’s reality.",
      "Connect the CRM to campaigns, forms or operational follow-up.",
    ],
  },
  "pos-systems": {
    outcomes: [
      "Support front-desk or retail transactions with better operational control.",
      "Improve handling of sales, receipts and basic stock visibility.",
      "Reduce reconciliation friction between point-of-sale and reporting.",
    ],
    deliverables: [
      "Transaction workflows and role-based checkout interfaces.",
      "Receipt, stock and reporting connections.",
      "Operational rules for discounts, returns or branches.",
    ],
    process: [
      "Understand how sales happen in the real environment.",
      "Design for speed, accuracy and staff usability.",
      "Connect POS activity to the wider business records.",
    ],
  },
  "inventory-systems": {
    outcomes: [
      "Track stock movement more reliably across procurement and fulfilment.",
      "Reduce stock uncertainty, over-ordering and avoidable shortages.",
      "Support operational planning with clearer inventory signals.",
    ],
    deliverables: [
      "Stock tracking, movement logs and adjustment workflows.",
      "Threshold logic and visibility across locations or categories.",
      "Reporting that supports procurement decisions.",
    ],
    process: [
      "Map how inventory enters, moves and leaves the operation.",
      "Design controls around accountability and exception handling.",
      "Monitor data quality after rollout to maintain trust in the system.",
    ],
  },
  "hrm-systems": {
    outcomes: [
      "Organise employee information and core HR workflows more consistently.",
      "Reduce ad hoc handling around leave, records and internal approvals.",
      "Support internal administration with better structure and access control.",
    ],
    deliverables: [
      "Employee records, leave handling and role-aware access.",
      "Approval flows and administrative reporting.",
      "Configurable workflows for internal operations.",
    ],
    process: [
      "Review HR administration pain points and controls.",
      "Build around routine actions staff and managers actually use.",
      "Keep the system clear enough for reliable day-to-day adoption.",
    ],
  },
  "accounting-systems": {
    outcomes: [
      "Improve visibility into invoices, payments and financial records.",
      "Reduce fragmented handling of recurring finance tasks.",
      "Support more consistent financial administration and reporting.",
    ],
    deliverables: [
      "Workflows for invoices, payment tracking and core records.",
      "Rules around statuses, approvals or recurring actions.",
      "Reporting views that support operational finance management.",
    ],
    process: [
      "Review the finance workflow and control requirements.",
      "Model records and statuses carefully before implementation.",
      "Roll out with clarity on roles, approvals and reconciliations.",
    ],
  },
  "saas-development": {
    outcomes: [
      "Package a repeatable digital service into a product others can use.",
      "Support growth beyond one client or one internal operation.",
      "Build for subscription, tenancy and product evolution.",
    ],
    deliverables: [
      "Tenant-aware architecture and role handling.",
      "Product workflows, billing hooks and admin controls.",
      "Foundations for iteration, onboarding and support.",
    ],
    process: [
      "Define the core product promise and user groups.",
      "Build the minimum platform that can support real customers.",
      "Expand through measured product learning rather than assumptions.",
    ],
  },
  "android-apps": {
    outcomes: [
      "Reach Android-heavy user bases with device-native convenience.",
      "Support field teams or customers who operate primarily from phones.",
      "Create mobile workflows matched to business context and usage.",
    ],
    deliverables: [
      "Android interfaces aligned to operational or customer tasks.",
      "Back-end connectivity, notifications and account flows.",
      "Release-ready structure for support and future updates.",
    ],
    process: [
      "Understand the mobile context of use first.",
      "Design for speed, clarity and constrained environments.",
      "Connect the app to the systems that keep it useful over time.",
    ],
  },
  "ios-apps": {
    outcomes: [
      "Provide a polished mobile experience for iPhone users.",
      "Support premium, consumer or internal mobile workflows on iOS.",
      "Keep performance and usability strong within the Apple ecosystem.",
    ],
    deliverables: [
      "iOS-focused user experience and account journeys.",
      "Integration with APIs, notifications and supporting systems.",
      "Release structure suitable for maintenance and iteration.",
    ],
    process: [
      "Define the job the app must perform on mobile.",
      "Shape the experience around that responsibility, not novelty.",
      "Launch with support for feedback-driven updates.",
    ],
  },
  "cross-platform-apps": {
    outcomes: [
      "Reach both Android and iOS without maintaining two separate products.",
      "Accelerate delivery when the core workflow is shared across platforms.",
      "Keep mobile strategy practical without unnecessary duplication.",
    ],
    deliverables: [
      "Shared mobile application logic across major platforms.",
      "Connected APIs, authentication and operational features.",
      "Reusable architecture that supports future growth.",
    ],
    process: [
      "Identify where shared mobile behaviour makes sense.",
      "Build around common workflows while protecting usability.",
      "Iterate from operational or customer feedback across devices.",
    ],
  },
  "business-apps": {
    outcomes: [
      "Support internal teams or customers with mobile workflows tied to real tasks.",
      "Move key actions closer to the point where work actually happens.",
      "Improve responsiveness for approvals, updates or field operations.",
    ],
    deliverables: [
      "Task-focused mobile flows for business activity.",
      "Back-office connections and permissions.",
      "Notification and status visibility where timing matters.",
    ],
    process: [
      "Review when staff or users need action away from desks.",
      "Shape the app around those moments of use.",
      "Connect mobile activity back into the core system of record.",
    ],
  },
  "ai-chatbots": {
    outcomes: [
      "Handle common enquiries faster and more consistently.",
      "Provide structured first-response support without replacing human judgment.",
      "Reduce repetitive communication overhead.",
    ],
    deliverables: [
      "Conversation flows aligned to common user intents.",
      "Knowledge integration and escalation rules.",
      "Reporting on questions, outcomes and handoff patterns.",
    ],
    process: [
      "Identify high-volume or repeatable conversations.",
      "Define what the chatbot should answer and when it should escalate.",
      "Refine from actual usage instead of speculative feature lists.",
    ],
  },
  "ai-automation": {
    outcomes: [
      "Reduce manual effort in repeatable decision or processing steps.",
      "Improve throughput where teams are slowed by routine work.",
      "Apply AI where it makes operations clearer, not noisier.",
    ],
    deliverables: [
      "Workflow automation with AI-assisted classification or handling.",
      "Human review points where risk or judgment matters.",
      "Operational visibility into automated outcomes.",
    ],
    process: [
      "Find repeatable work with clear patterns and measurable outcomes.",
      "Add AI only where it genuinely reduces effort or delay.",
      "Monitor reliability and keep escalation controls explicit.",
    ],
  },
  "ai-assistants": {
    outcomes: [
      "Help teams access information or complete routine work faster.",
      "Create internal assistance that reflects company-specific context.",
      "Reduce lookup time and task-switching around common needs.",
    ],
    deliverables: [
      "Assistant experience shaped around real internal or customer tasks.",
      "Context integration with documents, workflows or systems.",
      "Governance around what the assistant can and cannot do.",
    ],
    process: [
      "Define the assistant’s role clearly before implementation.",
      "Connect it to reliable information sources and workflows.",
      "Refine based on usage, accuracy and operational trust.",
    ],
  },
  "ai-integration": {
    outcomes: [
      "Introduce AI into existing systems without rebuilding everything.",
      "Connect models and automation into current workflows pragmatically.",
      "Keep AI adoption tied to specific business responsibilities.",
    ],
    deliverables: [
      "Integration of AI services into existing applications or processes.",
      "Prompt, workflow and review-layer design.",
      "Monitoring of outputs and operational fit.",
    ],
    process: [
      "Identify a narrow, valuable use case first.",
      "Connect AI services to the surrounding business logic safely.",
      "Measure usefulness in operation before expanding scope.",
    ],
  },
  "custom-ai-solutions": {
    outcomes: [
      "Solve business-specific problems that generic AI features do not address.",
      "Build AI capability around a defined workflow, dataset or decision context.",
      "Keep implementation aligned to operational constraints and review needs.",
    ],
    deliverables: [
      "Purpose-built AI workflow or application design.",
      "Integration with the systems and people around the use case.",
      "Controls for oversight, reliability and iteration.",
    ],
    process: [
      "Frame the exact business problem and success criteria.",
      "Design the surrounding workflow, not just the model interaction.",
      "Improve through measured operational feedback.",
    ],
  },
  "seo": {
    outcomes: [
      "Improve discoverability for high-intent search demand.",
      "Support long-term visibility instead of one-off traffic spikes.",
      "Align search performance with revenue-generating pages and topics.",
    ],
    deliverables: [
      "Search strategy, content priorities and technical guidance.",
      "Page optimisation around user intent and site structure.",
      "Measurement focused on business-relevant search outcomes.",
    ],
    process: [
      "Review search demand, site condition and competitive gaps.",
      "Optimise the pages and topics that matter commercially.",
      "Track performance over time and adjust with evidence.",
    ],
  },
  "local-seo": {
    outcomes: [
      "Increase visibility for location-based searches and service areas.",
      "Support calls, visits and enquiries from nearby demand.",
      "Strengthen local trust signals across search surfaces.",
    ],
    deliverables: [
      "Location-focused optimisation and profile alignment.",
      "Local landing page and visibility improvements.",
      "Guidance around consistency, reviews and local relevance.",
    ],
    process: [
      "Clarify target geographies and search behaviour.",
      "Optimise local presence across site and supporting channels.",
      "Refine based on search visibility and enquiry quality.",
    ],
  },
  "google-ads": {
    outcomes: [
      "Capture demand faster where paid search is commercially justified.",
      "Connect ad spend to stronger landing page and enquiry handling.",
      "Reduce waste by tightening offer, audience and conversion flow.",
    ],
    deliverables: [
      "Campaign structure aligned to offers and search intent.",
      "Landing page and conversion path recommendations.",
      "Measurement that supports budget decisions.",
    ],
    process: [
      "Define what should be promoted and to whom.",
      "Connect ads to pages that can actually convert interest.",
      "Adjust budgets and messaging using outcome data.",
    ],
  },
  "social-media-marketing": {
    outcomes: [
      "Strengthen visibility, recall and engagement across relevant platforms.",
      "Support brand presence with more consistent communication.",
      "Connect social activity to broader business goals.",
    ],
    deliverables: [
      "Platform-appropriate content direction and campaign support.",
      "Audience, message and posting-structure guidance.",
      "Measurement around engagement and response patterns.",
    ],
    process: [
      "Identify where the audience actually pays attention.",
      "Design a communication rhythm the business can sustain.",
      "Align social content with offers, trust and follow-up.",
    ],
  },
  "email-marketing": {
    outcomes: [
      "Stay visible to leads, customers or subscribers over time.",
      "Support nurturing, re-engagement and campaign follow-up.",
      "Turn owned communication into a more structured asset.",
    ],
    deliverables: [
      "Email campaign flows, segments and message structure.",
      "Newsletter or nurture planning linked to business context.",
      "Measurement around response and retention behaviour.",
    ],
    process: [
      "Define the audience segments that matter most.",
      "Build a communication sequence with clear purpose.",
      "Refine by response quality rather than volume alone.",
    ],
  },
  "content-marketing": {
    outcomes: [
      "Support trust and discoverability through useful content.",
      "Give the business more ways to explain expertise and solve objections.",
      "Create long-term assets that support sales and search.",
    ],
    deliverables: [
      "Topic planning connected to business priorities.",
      "Content structure across pages, articles or campaign assets.",
      "Editorial direction that supports authority and clarity.",
    ],
    process: [
      "Identify the questions and concerns the audience already has.",
      "Prioritise content with commercial relevance, not just volume.",
      "Build consistency over time instead of sporadic publication.",
    ],
  },
  "marketing-automation": {
    outcomes: [
      "Reduce manual follow-up and fragmented campaign handling.",
      "Connect forms, segments and triggered communication more effectively.",
      "Improve marketing responsiveness with clearer workflow design.",
    ],
    deliverables: [
      "Automated flows for lead handling or audience nurturing.",
      "System connections between campaign sources and follow-up actions.",
      "Operational logic around timing, segmentation and routing.",
    ],
    process: [
      "Map what currently requires repetitive coordination.",
      "Automate only the steps that improve consistency and speed.",
      "Review outcomes to keep the automation commercially useful.",
    ],
  },
  "logo-design": {
    outcomes: [
      "Create a recognisable mark that supports brand identity.",
      "Improve consistency across digital and physical touchpoints.",
      "Give the business a clearer visual anchor.",
    ],
    deliverables: [
      "Logo concepts refined around brand positioning and use cases.",
      "Practical variations for common applications.",
      "Guidance on how the mark should be used consistently.",
    ],
    process: [
      "Understand the business character and market context.",
      "Design for recognition and practical use, not decoration alone.",
      "Refine into an identity component that can scale with the brand.",
    ],
  },
  "brand-identity": {
    outcomes: [
      "Make the business appear more coherent and recognisable.",
      "Improve consistency across communications and customer touchpoints.",
      "Support trust through clearer brand presentation.",
    ],
    deliverables: [
      "Visual system including core identity rules and direction.",
      "Guidance on typography, colour and brand application.",
      "Identity structure that supports future marketing and product work.",
    ],
    process: [
      "Clarify the business character and positioning first.",
      "Translate that into a visual system with usable rules.",
      "Apply it across the places customers and stakeholders actually interact.",
    ],
  },
  "ui-ux-design": {
    outcomes: [
      "Make digital tools easier to understand and use.",
      "Reduce avoidable friction in important customer or staff journeys.",
      "Support implementation with clearer interface decisions.",
    ],
    deliverables: [
      "Flow design, interface structure and interaction thinking.",
      "Page or application layouts tied to task completion.",
      "Design direction that helps development stay aligned.",
    ],
    process: [
      "Map the journey before drawing screens.",
      "Design for clarity, hierarchy and successful task completion.",
      "Refine using user and operational feedback.",
    ],
  },
  "graphic-design": {
    outcomes: [
      "Support campaigns and communications with stronger visual clarity.",
      "Keep brand presentation more consistent across assets.",
      "Reduce the patchwork feel of ad hoc design materials.",
    ],
    deliverables: [
      "Design assets for campaigns, communications or collateral.",
      "Layouts aligned to message hierarchy and brand rules.",
      "Reusable visual treatment where repetition matters.",
    ],
    process: [
      "Clarify the message and medium first.",
      "Design for communication, not surface decoration alone.",
      "Keep assets aligned to the wider brand direction.",
    ],
  },
  "web-hosting": {
    outcomes: [
      "Keep websites available, maintainable and supported in production.",
      "Reduce hosting instability becoming a public-facing business problem.",
      "Match hosting choices to the site’s actual needs.",
    ],
    deliverables: [
      "Hosting setup and configuration aligned to workload.",
      "Operational guidance around deployment and access.",
      "Support for continuity, updates and ongoing reliability.",
    ],
    process: [
      "Assess the site’s technical and operational requirements.",
      "Set up hosting with clarity around ownership and access.",
      "Maintain the environment with visible responsibility.",
    ],
  },
  "vps-hosting": {
    outcomes: [
      "Support systems that need more control than basic shared hosting allows.",
      "Provide predictable infrastructure for business-critical applications.",
      "Give the business clearer control over runtime conditions.",
    ],
    deliverables: [
      "VPS setup, environment configuration and access structure.",
      "Deployment support suited to the application stack.",
      "Operational oversight for continuity and maintainability.",
    ],
    process: [
      "Clarify workload, traffic and control requirements.",
      "Configure infrastructure around security and maintainability.",
      "Keep access and deployment ownership explicit.",
    ],
  },
  "domain-registration": {
    outcomes: [
      "Keep domain ownership and renewal handling clear.",
      "Reduce business risk from unmanaged domain dependencies.",
      "Support clean setup for websites, email and related services.",
    ],
    deliverables: [
      "Domain registration or transfer support.",
      "DNS guidance aligned to the wider technical stack.",
      "Ownership clarity for continuity and future control.",
    ],
    process: [
      "Confirm the domain strategy and ownership requirements.",
      "Set up records to support the connected services properly.",
      "Document responsibility so control stays with the business.",
    ],
  },
  "business-email": {
    outcomes: [
      "Give the organisation a more credible communication channel.",
      "Support team coordination and external trust with domain-based email.",
      "Reduce dependence on informal personal-email workflows.",
    ],
    deliverables: [
      "Business email setup and account structure.",
      "Domain and service configuration.",
      "Operational guidance for access and continuity.",
    ],
    process: [
      "Review user needs, domains and administrative responsibilities.",
      "Configure the service with practical ownership and access rules.",
      "Support a cleaner transition into normal use.",
    ],
  },
  "ssl-certificates": {
    outcomes: [
      "Protect user trust and browser security expectations.",
      "Reduce avoidable warnings and insecure transport issues.",
      "Support safer handling of public web traffic.",
    ],
    deliverables: [
      "Certificate provisioning and renewal support.",
      "Configuration aligned to the site or application stack.",
      "Operational checks for continuity and expiry handling.",
    ],
    process: [
      "Confirm the environment and certificate requirement.",
      "Configure correctly for the deployment model in use.",
      "Keep renewal handling visible so it is not forgotten.",
    ],
  },
  "digital-transformation": {
    outcomes: [
      "Help the business rethink technology use across processes and teams.",
      "Reduce expensive guesswork before larger operational changes.",
      "Create a clearer path from current-state friction to future-state capability.",
    ],
    deliverables: [
      "Assessment of current workflows, systems and bottlenecks.",
      "Transformation priorities and phased recommendations.",
      "Guidance that connects change to actual business value.",
    ],
    process: [
      "Understand operational reality before proposing transformation.",
      "Prioritise the changes that unlock the most meaningful improvement.",
      "Sequence implementation to reduce disruption and confusion.",
    ],
  },
  "technology-consulting": {
    outcomes: [
      "Support better decisions before spending on the wrong tools or architecture.",
      "Clarify tradeoffs where multiple technical paths are possible.",
      "Strengthen planning around digital investments.",
    ],
    deliverables: [
      "Technical recommendations grounded in business context.",
      "Option analysis and practical decision support.",
      "Advisory input before significant commitments are made.",
    ],
    process: [
      "Define the decision that actually needs to be made.",
      "Compare options against business constraints and outcomes.",
      "Recommend a direction that the team can realistically own.",
    ],
  },
  "system-integration": {
    outcomes: [
      "Connect separate systems so data and actions move more reliably.",
      "Reduce repeated manual transfer between disconnected tools.",
      "Improve continuity across operational workflows.",
    ],
    deliverables: [
      "Integration planning and implementation guidance.",
      "Data movement, workflow and dependency analysis.",
      "Operational controls around reliability and failure handling.",
    ],
    process: [
      "Map the systems, events and data involved.",
      "Design the integration around business rules and edge cases.",
      "Monitor and harden the connection after release.",
    ],
  },
  "project-consulting": {
    outcomes: [
      "Bring more clarity to complex or risky technology projects.",
      "Reduce avoidable failure caused by scope confusion or weak planning.",
      "Help the team move forward with firmer technical direction.",
    ],
    deliverables: [
      "Project-level advisory support on scope, architecture or execution.",
      "Risk identification and planning guidance.",
      "Technical framing that supports delivery discipline.",
    ],
    process: [
      "Clarify the project outcome and the real constraints.",
      "Identify where technical decisions will create the most leverage or risk.",
      "Support execution with clearer structure and checkpoints.",
    ],
  },
  "security-audit": {
    outcomes: [
      "Identify practical weaknesses before they become incidents.",
      "Improve confidence in the systems handling business activity.",
      "Create a more explicit view of security priorities and responsibilities.",
    ],
    deliverables: [
      "Structured review of the relevant systems and configurations.",
      "Findings prioritised by practical risk and impact.",
      "Recommendations that can be acted on in sequence.",
    ],
    process: [
      "Scope the systems and the kind of risk that matters most.",
      "Review configuration, exposure and operational handling.",
      "Turn findings into an action plan instead of a static report.",
    ],
  },
  "website-security": {
    outcomes: [
      "Reduce the risk of common public-facing website vulnerabilities.",
      "Protect brand trust and availability on a visible channel.",
      "Strengthen the operational posture of the web stack.",
    ],
    deliverables: [
      "Website-focused security review and hardening measures.",
      "Access, update and exposure controls.",
      "Guidance around monitoring and ongoing protection.",
    ],
    process: [
      "Assess the current web stack and exposure points.",
      "Apply practical protections and tighten weak areas.",
      "Keep the site maintained so security does not decay over time.",
    ],
  },
  "backup-recovery": {
    outcomes: [
      "Reduce business disruption when systems fail or data is lost.",
      "Make restoration more predictable when problems occur.",
      "Turn backup from assumption into an operational capability.",
    ],
    deliverables: [
      "Backup planning and retention structure.",
      "Recovery approach aligned to system criticality.",
      "Guidance on verification, ownership and continuity.",
    ],
    process: [
      "Identify what must be recoverable and how fast.",
      "Design the backup model around those expectations.",
      "Review recovery readiness instead of trusting backups blindly.",
    ],
  },
  "security-hardening": {
    outcomes: [
      "Tighten systems that are functional but not sufficiently protected.",
      "Reduce attack surface through more disciplined configuration.",
      "Improve operational resilience without redesigning everything.",
    ],
    deliverables: [
      "Hardening measures for hosts, applications or access paths.",
      "Configuration review and tightened defaults.",
      "Operational recommendations for sustained security posture.",
    ],
    process: [
      "Identify the most exposed or weak areas first.",
      "Apply changes that materially reduce risk.",
      "Document the controls so they remain part of normal operations.",
    ],
  },
  "payment-gateway": {
    outcomes: [
      "Enable reliable online payment handling within the customer journey.",
      "Reduce manual payment coordination and confirmation delays.",
      "Support revenue flows with clearer system integration.",
    ],
    deliverables: [
      "Gateway integration tied to the relevant product or service flow.",
      "Handling for statuses, callbacks and business rules.",
      "Operational support for payment visibility and follow-up.",
    ],
    process: [
      "Map where payment happens in the wider user journey.",
      "Integrate with care around edge cases and confirmations.",
      "Monitor and refine the payment flow after launch.",
    ],
  },
  "whatsapp-api": {
    outcomes: [
      "Connect WhatsApp into business workflows more systematically.",
      "Reduce fragmented message handling where structured messaging matters.",
      "Support customer communication with clearer automation options.",
    ],
    deliverables: [
      "WhatsApp API integration aligned to use case and workflow.",
      "Message triggers, templates or routing logic as needed.",
      "Operational consideration for escalation and response handling.",
    ],
    process: [
      "Define what WhatsApp should accomplish in the business process.",
      "Connect messaging to the surrounding systems and rules.",
      "Refine for compliance, responsiveness and usability.",
    ],
  },
  "sms-gateway": {
    outcomes: [
      "Support alerts, confirmations or transactional communication through SMS.",
      "Improve reach where SMS remains operationally important.",
      "Add another reliable communication layer to business workflows.",
    ],
    deliverables: [
      "SMS integration connected to the relevant system events.",
      "Template, trigger and delivery-flow logic.",
      "Operational visibility around message sending and response patterns.",
    ],
    process: [
      "Define where SMS adds operational value.",
      "Connect messages to the right triggers and records.",
      "Monitor delivery and message usefulness over time.",
    ],
  },
  "crm-integration": {
    outcomes: [
      "Move lead and customer data into the CRM more reliably.",
      "Reduce manual copy-paste or delayed record creation.",
      "Improve follow-up quality through better system continuity.",
    ],
    deliverables: [
      "Integration between CRM and the relevant channels or systems.",
      "Field mapping, workflow rules and event handling.",
      "Operational logic around sync reliability and exceptions.",
    ],
    process: [
      "Map the source events and the CRM actions they should trigger.",
      "Build the integration around data quality and real follow-up needs.",
      "Review failures and edge cases after release.",
    ],
  },
  "erp-integration": {
    outcomes: [
      "Connect ERP workflows to surrounding business systems more effectively.",
      "Reduce operational delays caused by disconnected records and actions.",
      "Support a more unified process across departments.",
    ],
    deliverables: [
      "ERP integration planning and implementation.",
      "Data, workflow and exception handling rules.",
      "Visibility around system dependencies and operational impacts.",
    ],
    process: [
      "Clarify which ERP processes need external connections.",
      "Design integrations around business-critical flows and controls.",
      "Stabilise the integration with monitoring and review.",
    ],
  },
  "workflow-automation": {
    outcomes: [
      "Reduce repetitive coordination and manual task chasing.",
      "Make routine operational sequences more consistent and faster.",
      "Free teams from low-value handoff work.",
    ],
    deliverables: [
      "Automated workflow logic around triggers, actions and statuses.",
      "Routing and notification steps aligned to business rules.",
      "Operational visibility into process flow and bottlenecks.",
    ],
    process: [
      "Map the routine workflow in detail.",
      "Automate the parts that benefit from speed and consistency.",
      "Keep exceptions visible so automation does not hide problems.",
    ],
  },
  "crm-automation": {
    outcomes: [
      "Improve speed and consistency in lead or customer follow-up.",
      "Reduce missed actions caused by manual CRM handling.",
      "Support more disciplined commercial processes.",
    ],
    deliverables: [
      "CRM automations around lead routing, reminders or stage changes.",
      "Trigger logic tied to real sales or service workflows.",
      "Controls for visibility and exception handling.",
    ],
    process: [
      "Review the CRM process for repeated manual patterns.",
      "Automate the steps that improve response and tracking.",
      "Adjust based on how the team actually uses the system.",
    ],
  },
  "hr-automation": {
    outcomes: [
      "Reduce HR administration effort around routine internal processes.",
      "Improve consistency in approvals, reminders or record handling.",
      "Support smoother internal operations for managers and staff.",
    ],
    deliverables: [
      "Automated HR workflow steps and notifications.",
      "Rule-based handling for standard internal processes.",
      "Operational structure that reduces ad hoc follow-up.",
    ],
    process: [
      "Identify routine HR steps that repeatedly consume time.",
      "Automate carefully around approvals and accountability.",
      "Keep the process understandable to the teams using it.",
    ],
  },
  "document-automation": {
    outcomes: [
      "Reduce repetitive document preparation and handling effort.",
      "Improve consistency in templates, generation or approval flow.",
      "Support operational speed where documents are routine.",
    ],
    deliverables: [
      "Document generation or workflow automation aligned to business rules.",
      "Template, approval or dispatch structure as needed.",
      "Connections to the records or triggers behind the documents.",
    ],
    process: [
      "Map how documents are created, reviewed and sent today.",
      "Automate the repeatable parts while keeping control points explicit.",
      "Measure whether the process actually becomes faster and cleaner.",
    ],
  },
  "business-intelligence": {
    outcomes: [
      "Improve decision-making with more structured operational visibility.",
      "Reduce dependence on fragmented reporting and one-off spreadsheet work.",
      "Give leadership clearer signals about performance and movement.",
    ],
    deliverables: [
      "BI structure aligned to important business questions.",
      "Reporting logic and data presentation focused on actionability.",
      "A framework for ongoing visibility rather than isolated reports.",
    ],
    process: [
      "Define the business questions that reporting should answer.",
      "Structure the data and views around those decisions.",
      "Improve clarity through iteration, not just more charts.",
    ],
  },
  dashboards: {
    outcomes: [
      "Give teams faster visibility into the metrics they act on regularly.",
      "Reduce time spent assembling recurring operational views.",
      "Support quicker decisions with clearer presentation.",
    ],
    deliverables: [
      "Dashboard design around role-specific information needs.",
      "Connected data views and practical metric presentation.",
      "Usable interfaces for recurring operational review.",
    ],
    process: [
      "Clarify who needs the dashboard and why.",
      "Select the metrics that influence actual decisions.",
      "Refine layout and definitions so the dashboard stays trusted.",
    ],
  },
  reports: {
    outcomes: [
      "Make regular business reporting more structured and dependable.",
      "Reduce ad hoc compilation work around recurring updates.",
      "Support stakeholders with clearer, repeatable views.",
    ],
    deliverables: [
      "Report design and generation logic for recurring needs.",
      "Consistent data presentation tied to business context.",
      "A clearer reporting routine for leadership or operations.",
    ],
    process: [
      "Define the reporting cadence and audience first.",
      "Build the report around the decisions it supports.",
      "Improve consistency and reduce manual effort over time.",
    ],
  },
  "kpi-tracking": {
    outcomes: [
      "Keep key measures visible and tied to business priorities.",
      "Reduce confusion about what should actually be monitored.",
      "Support accountability around performance movement.",
    ],
    deliverables: [
      "KPI definition and visibility structure.",
      "Tracking views or reporting support around core indicators.",
      "A clearer rhythm for monitoring business performance.",
    ],
    process: [
      "Identify the indicators that truly reflect business movement.",
      "Structure visibility so teams can interpret the numbers correctly.",
      "Review whether the KPIs stay relevant as operations evolve.",
    ],
  },
  "software-maintenance": {
    outcomes: [
      "Keep custom software stable, secure and useful after launch.",
      "Reduce technical drift and avoidable operational disruption.",
      "Support improvements without re-entering full redevelopment cycles.",
    ],
    deliverables: [
      "Issue response, updates and improvement handling.",
      "Maintenance structure suited to the system’s operational role.",
      "Visibility around backlog, risk and recurring technical concerns.",
    ],
    process: [
      "Review the current system condition and support expectations.",
      "Establish a maintenance cadence with clear responsibility.",
      "Convert repeated issues into more permanent fixes.",
    ],
  },
  "performance-optimization": {
    outcomes: [
      "Improve speed, responsiveness or efficiency in existing systems.",
      "Reduce user frustration caused by slow or heavy workflows.",
      "Support better operational performance without rebuilding from zero.",
    ],
    deliverables: [
      "Assessment of performance bottlenecks and causes.",
      "Targeted optimisation work tied to measured issues.",
      "Recommendations for sustained performance handling.",
    ],
    process: [
      "Measure where performance is actually failing.",
      "Address the bottlenecks that matter most to users or operations.",
      "Recheck after changes to confirm the improvement is real.",
    ],
  },
  "technical-support": {
    outcomes: [
      "Give the business a clearer route for technical help when issues arise.",
      "Reduce downtime and confusion around ownership during problems.",
      "Support smoother ongoing use of live systems.",
    ],
    deliverables: [
      "Support handling structure for operational incidents or requests.",
      "Defined response paths and triage patterns.",
      "A more dependable relationship between users and technical support.",
    ],
    process: [
      "Define the kinds of support the business actually needs.",
      "Set a workable response structure and escalation path.",
      "Track recurring issues so support improves over time.",
    ],
  },
};

const sectionThemes: Record<
  string,
  {
    overview: string[];
    highlights: FoundationPageChecklist[];
    sections: FoundationPageSection[];
    cta: FoundationPageCta;
  }
> = {
  about: {
    overview: [
      "This page extends the LKProfessionals company story rather than repeating a generic agency summary.",
      "It is meant to clarify how the team works, what clients can expect, and where this page fits in the broader company narrative.",
    ],
    highlights: [
      {
        title: "What this section should communicate",
        items: [
          "Operational maturity and reliability.",
          "A realistic picture of the team and working style.",
          "Reasons a client or candidate would want to continue exploring.",
        ],
      },
    ],
    sections: [
      {
        title: "Why this page exists",
        body:
          "The About section should reduce uncertainty. Instead of broad claims, it should show how LKProfessionals thinks about delivery, accountability and long-term relationships.",
      },
      {
        title: "What visitors should understand next",
        body:
          "By the time someone leaves an About page, they should have a clearer sense of the company’s standards, operating style and where to go next for proof, services or contact.",
      },
    ],
    cta: {
      title: "Continue the company story",
      body:
        "If you are evaluating whether LKProfessionals is the right fit, move from background information into the service and contact paths that matter to your decision.",
      primaryHref: "/contact/",
      primaryLabel: "Talk to the team",
      secondaryHref: "/services/",
      secondaryLabel: "Explore services",
    },
  },
  insights: {
    overview: [
      "This page acts as a topic-level content hub within Insights.",
      "Its job is to set expectations around what kind of articles, updates or educational material belong under this route.",
    ],
    highlights: [
      {
        title: "What a strong insights hub should do",
        items: [
          "Frame the topic clearly for the reader.",
          "Show what kinds of questions or decisions the content will help with.",
          "Guide visitors into related categories or contact paths when needed.",
        ],
      },
    ],
    sections: [
      {
        title: "Content direction",
        body:
          "Topic hubs work best when they are organised around recurring business questions rather than loose publishing. That means the page should help readers understand the practical value of the subject area before they open individual articles.",
      },
      {
        title: "How this should support the wider website",
        body:
          "Insights should reinforce authority, answer objections and support search visibility. The goal is not to publish for its own sake, but to create content that helps people make better decisions.",
      },
    ],
    cta: {
      title: "Need guidance beyond reading?",
      body:
        "If the topic applies directly to your business situation, the next step is usually a conversation about requirements, priorities and implementation constraints.",
      primaryHref: "/contact/",
      primaryLabel: "Discuss your needs",
      secondaryHref: "/services/",
      secondaryLabel: "View service areas",
    },
  },
  portfolio: {
    overview: [
      "This route represents a portfolio category rather than a single proof point.",
      "Its purpose is to help visitors understand the kinds of work that belong in this category and what business outcomes they should expect to see.",
    ],
    highlights: [
      {
        title: "What this portfolio route should prove",
        items: [
          "The kind of problems LKProfessionals solves in this area.",
          "The execution standard visitors should expect.",
          "Why the category matters commercially, not just visually.",
        ],
      },
    ],
    sections: [
      {
        title: "How to use this page",
        body:
          "A strong portfolio category page should orient visitors before they evaluate individual projects. It should explain the business context, common goals and the indicators of strong work in this category.",
      },
      {
        title: "What should come next",
        body:
          "Once the category is clear, visitors should be able to move into project examples, relevant services or a conversation about similar requirements.",
      },
    ],
    cta: {
      title: "Looking for similar work?",
      body:
        "If this category is close to what you need, use it as a starting point for a more specific discussion about scope, timeline and constraints.",
      primaryHref: "/get-a-quote/",
      primaryLabel: "Request a quote",
      secondaryHref: "/contact/",
      secondaryLabel: "Start a conversation",
    },
  },
  resources: {
    overview: [
      "This page belongs to a resources library intended to support research, planning or internal business use.",
      "It should set expectations around the kinds of downloadable or reference material available under this route.",
    ],
    highlights: [
      {
        title: "What resource pages should achieve",
        items: [
          "Clarify who the resource is for.",
          "Explain what problem it helps with.",
          "Point the reader toward implementation help if needed.",
        ],
      },
    ],
    sections: [
      {
        title: "Practical usefulness matters most",
        body:
          "Resources should help visitors act, plan or assess more effectively. That means the page needs enough context to explain why the material exists and when it becomes useful in a real business setting.",
      },
      {
        title: "How this supports commercial trust",
        body:
          "Useful resources often work as early-stage trust builders. They show that the company can structure knowledge clearly before any formal project begins.",
      },
    ],
    cta: {
      title: "Need help applying the material?",
      body:
        "Resources are most valuable when they lead to clearer decisions. If you need help turning guidance into implementation, continue into a consultation or project discussion.",
      primaryHref: "/book-a-consultation/",
      primaryLabel: "Book a consultation",
      secondaryHref: "/contact/",
      secondaryLabel: "Contact LKProfessionals",
    },
  },
  contact: {
    overview: [
      "This route should make it easier for visitors to choose the right contact path.",
      "Its job is to reduce misrouted enquiries and set expectations about what happens after someone reaches out.",
    ],
    highlights: [
      {
        title: "What visitors need here",
        items: [
          "Clarity on the purpose of this contact route.",
          "Confidence that the right team will handle the enquiry.",
          "A quick sense of what information is useful to provide.",
        ],
      },
    ],
    sections: [
      {
        title: "Why route-specific contact pages help",
        body:
          "Specialised contact pages make the enquiry experience cleaner for both the visitor and the team receiving the message. They help separate general enquiries from sales, support or more structured project discussions.",
      },
      {
        title: "What should happen after submission",
        body:
          "The page should set practical expectations about response flow, ownership and what kind of follow-up is likely next.",
      },
    ],
    cta: {
      title: "Need a more structured project path?",
      body:
        "If the request is already moving toward delivery, a quote or consultation path is usually more efficient than a broad contact form.",
      primaryHref: "/get-a-quote/",
      primaryLabel: "Request a quote",
      secondaryHref: "/book-a-consultation/",
      secondaryLabel: "Book a consultation",
    },
  },
  "client-portal": {
    overview: [
      "These portal pages are functional placeholders for authenticated client workflows.",
      "They should explain the purpose of the area without overpromising access to unauthenticated visitors.",
    ],
    highlights: [
      {
        title: "What these pages should make clear",
        items: [
          "Which client activity belongs in this area.",
          "Whether access requires login or onboarding.",
          "How the portal supports ongoing delivery and communication.",
        ],
      },
    ],
    sections: [
      {
        title: "Portal expectations",
        body:
          "Client portal routes should focus on access clarity, workflow purpose and support expectations. Public visitors do not need feature-heavy marketing here; they need a simple understanding of what the portal is for.",
      },
      {
        title: "Operational role",
        body:
          "A portal is typically useful once a working relationship is active. These pages should therefore act as orientation points rather than broad acquisition content.",
      },
    ],
    cta: {
      title: "Need access or project support?",
      body:
        "If you are an existing client and need help with access or project coordination, use the relevant support or contact route.",
      primaryHref: "/contact/support/",
      primaryLabel: "Contact support",
      secondaryHref: "/contact/",
      secondaryLabel: "General contact",
    },
  },
  legal: {
    overview: [
      "These pages organise policy and legal-reference information for the public website.",
      "They should be clear, restrained and easy to navigate rather than sales-oriented.",
    ],
    highlights: [
      {
        title: "What legal pages should prioritise",
        items: [
          "Clear scope of the policy or term.",
          "Straightforward language about what is covered.",
          "Easy navigation to related legal references.",
        ],
      },
    ],
    sections: [
      {
        title: "Why this page matters",
        body:
          "Legal pages help define expectations around privacy, use of the website and commercial terms. Even when simplified, they should make the subject area understandable and easy to locate.",
      },
      {
        title: "How visitors use these routes",
        body:
          "People usually arrive on legal pages with a narrow question. The page should therefore orient them quickly and point them toward the specific policy or term they need.",
      },
    ],
    cta: {
      title: "Need clarification?",
      body:
        "If a policy, term or process is unclear in relation to an active project or enquiry, use a direct contact route for clarification.",
      primaryHref: "/contact/",
      primaryLabel: "Contact LKProfessionals",
      secondaryHref: "/legal/",
      secondaryLabel: "View legal index",
    },
  },
  fallback: {
    overview: [
      "This page fills a content gap while staying aligned to the surrounding section of the website.",
      "Its purpose is to give visitors enough route-specific context to continue exploring confidently.",
    ],
    highlights: [
      {
        title: "What this page should do",
        items: [
          "Explain why this route exists.",
          "Connect the route to related content or services.",
          "Provide a sensible next step instead of a dead end.",
        ],
      },
    ],
    sections: [
      {
        title: "Context",
        body:
          "Not every route needs a long page, but every public route should still tell the visitor what it is about, where it fits and what to do next.",
      },
      {
        title: "Next step",
        body:
          "The page should always route visitors toward a more specific service, proof point, resource or contact path depending on their intent.",
      },
    ],
    cta: {
      title: "Continue exploring",
      body:
        "Use the surrounding navigation and related links to move from this overview into the more detailed parts of the site.",
      primaryHref: "/services/",
      primaryLabel: "Explore services",
      secondaryHref: "/contact/",
      secondaryLabel: "Contact LKProfessionals",
    },
  },
};

function toSentenceCase(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function humanizeSlug(slug: string): string {
  return slug
    .split("-")
    .map((part) => {
      if (part === "ai" || part === "api" || part === "hrm" || part === "crm" || part === "erp" || part === "seo" || part === "ssl" || part === "vps" || part === "kpi" || part === "ios") {
        return part.toUpperCase();
      }

      return toSentenceCase(part);
    })
    .join(" ");
}

function getRootSection(path: string): string {
  return path.split("/")[0] ?? "";
}

function getSlug(path: string): string {
  const parts = path.split("/");
  return parts[parts.length - 1] ?? path;
}

function getParentLabel(page: SitePage): string {
  if (!page.parentPath) {
    return page.eyebrow;
  }

  const family = serviceFamilyByHref.get(page.parentPath);

  if (family) {
    return family.title;
  }

  const parentGroup = headerNavigation.find(
    (entry) => entry.href.replace(/^\//, "") === page.parentPath,
  );

  if (parentGroup) {
    return parentGroup.label;
  }

  return humanizeSlug(getSlug(page.parentPath));
}

function getSiblingLabels(page: SitePage): string[] {
  const root = getRootSection(page.path);

  if (page.parentPath?.startsWith("services/")) {
    const family = serviceFamilyByHref.get(page.parentPath);
    return family?.focus ?? [];
  }

  if (root === "about") {
    return aboutNavigation.map((entry) => entry.label);
  }

  if (root === "insights") {
    return insightNavigation.map((entry) => entry.label);
  }

  if (page.path.startsWith("case-studies")) {
    return caseStudiesNavigation.map((entry) => entry.label);
  }

  if (page.path.startsWith("industries")) {
    return industryNavigation.map((entry) => entry.label);
  }

  return page.childPaths.map((path) => humanizeSlug(getSlug(path)));
}

function getServiceContent(page: SitePage): FoundationPageContent | null {
  const slug = getSlug(page.path);
  const family = page.parentPath
    ? serviceFamilyByHref.get(page.parentPath)
    : serviceFamilyByHref.get(page.path);

  if (!family) {
    return null;
  }

  const group = serviceGroupByName.get(family.group);
  const theme = servicePageThemes[slug];

  if (theme) {
    return {
      title: `${page.title} Services`,
      description: `${page.title} services from LKProfessionals for businesses that need ${theme.outcomes[0].replace(/\.$/, "").toLowerCase()}.`,
      lead: `${page.title} should be described as a practical business service with clear operational value, realistic scope and a direct connection to how the wider ${family.title.toLowerCase()} service line works.`,
      contextLabel: family.group,
      overview: [
        family.description,
        group
          ? `${family.title} belongs to the ${group.name.toLowerCase()} group: ${group.description}`
          : `This route sits within the ${family.title.toLowerCase()} service family.`,
      ],
      highlights: [
        {
          title: "Typical outcomes",
          items: theme.outcomes,
        },
        {
          title: "Typical delivery scope",
          items: theme.deliverables,
        },
      ],
      sections: [
        {
          title: `How LKProfessionals should position ${page.title}`,
          body: `This page should explain ${page.title.toLowerCase()} in business terms first. The visitor should understand the workflow, commercial goal or operational burden the service addresses before reading about tools or features.`,
        },
        {
          title: "Where this fits in a broader engagement",
          body: `Most ${page.title.toLowerCase()} work is not isolated. It usually connects to adjacent concerns such as planning, content, integration, maintenance or internal process design. The page should make that relationship explicit so the service feels credible rather than narrow.`,
        },
        {
          title: "Delivery approach",
          body: theme.process.join(" "),
        },
      ],
      cta: {
        title: `Discuss ${page.title.toLowerCase()} requirements`,
        body: `If your business is evaluating ${page.title.toLowerCase()}, the next step should be a scoped conversation around requirements, constraints, dependencies and delivery priorities.`,
        primaryHref: "/get-a-quote/",
        primaryLabel: "Request a quote",
        secondaryHref: family.href,
        secondaryLabel: `Explore ${family.title}`,
      },
    };
  }

  return {
    title: family.title,
    description: family.description,
    lead: `${family.title} should be presented as a connected service family rather than a loose list of offerings. This page exists to explain the shared business logic, implementation standards and decision criteria that apply across the service line.`,
    contextLabel: family.group,
    overview: [
      family.description,
      `Core focus areas: ${family.focus.join(", ")}.`,
    ],
    highlights: [
      {
        title: `${family.title} focus`,
        items: family.focus,
      },
      {
        title: "Service principles",
        items: servicePrinciples.slice(0, 3).map(
          (principle) => `${principle.title}: ${principle.description}`,
        ),
      },
    ],
    sections: [
      {
        title: "What this service family covers",
        body: `The ${family.title.toLowerCase()} section should help visitors understand the types of problems LKProfessionals addresses in this area, the delivery boundaries involved, and the difference between this service family and adjacent ones.`,
      },
      {
        title: "How to evaluate fit",
        body: `A strong category page should help a visitor decide whether they need a focused service, a broader engagement or a staged rollout. It should reduce confusion before someone moves into a specific sub-service or project conversation.`,
      },
      {
        title: "How LKProfessionals should work here",
        body: group
          ? group.description
          : "The delivery model should stay practical, modular and tied to measurable business outcomes.",
      },
    ],
    cta: {
      title: `Need a ${family.title.toLowerCase()} partner?`,
      body: "Use this section to move into a more specific sub-service or start a direct scoping conversation with the team.",
      primaryHref: "/get-a-quote/",
      primaryLabel: "Start a project discussion",
      secondaryHref: "/contact/",
      secondaryLabel: "Contact LKProfessionals",
    },
  };
}

function getSectionContent(page: SitePage): FoundationPageContent {
  const root = getRootSection(page.path);
  const theme =
    sectionThemes[root] ??
    sectionThemes[page.path] ??
    sectionThemes.fallback;
  const parentLabel = getParentLabel(page);
  const siblingLabels = getSiblingLabels(page).slice(0, 6);
  const childLabels = page.childPaths
    .map((path) => humanizeSlug(getSlug(path)))
    .slice(0, 6);
  const related =
    childLabels.length > 0
      ? childLabels
      : siblingLabels.length > 0
        ? siblingLabels
        : [parentLabel];

  const title =
    page.title === parentLabel
      ? page.title
      : `${page.title} | ${parentLabel}`;

  return {
    title,
    description: `${page.title} information within the LKProfessionals ${parentLabel.toLowerCase()} section.`,
    lead: `${theme.overview[0]} For this route specifically, the page should explain what "${page.title}" means inside the wider ${parentLabel} section and help the visitor take the next sensible step.`,
    contextLabel: root ? humanizeSlug(root) : page.eyebrow,
    overview: [
      ...theme.overview,
      `Related routes in this area include ${related.join(", ")}.`,
    ],
    highlights: [
      ...theme.highlights,
      {
        title: "Related focus areas",
        items: related,
      },
    ],
    sections: [
      {
        title: `How ${page.title} fits here`,
        body: `This route belongs to the ${parentLabel} area of the website. The content should therefore connect the page to surrounding navigation, related questions and the reason a visitor would choose this specific path instead of a broader section page.`,
      },
      ...theme.sections,
    ],
    cta: theme.cta,
  };
}

export function getFoundationPageContent(
  page: SitePage,
): FoundationPageContent {
  if (page.path.startsWith("services/")) {
    return getServiceContent(page) ?? getSectionContent(page);
  }

  return getSectionContent(page);
}
