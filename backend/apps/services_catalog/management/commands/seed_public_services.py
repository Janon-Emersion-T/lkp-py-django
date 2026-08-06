from __future__ import annotations

from copy import deepcopy
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.services_catalog.models import (
    Service,
    ServiceFaq,
    ServiceFeature,
    ServiceProcessStep,
    ServiceSeo,
    ServiceStatus,
    ServiceTechnology,
)


SERVICE_DEFINITIONS: tuple[dict[str, Any], ...] = (
    {
        "title": "Web Development",
        "slug": "web-development",
        "short_description": (
            "Fast, maintainable business websites and web platforms "
            "designed around search visibility, conversion and "
            "long-term ownership."
        ),
        "hero_title": (
            "Websites built to support the business—not merely "
            "represent it."
        ),
        "hero_description": (
            "LKProfessionals plans, designs and develops "
            "high-performance websites that communicate clearly, "
            "rank responsibly and convert the right visitors into "
            "enquiries."
        ),
        "description": {
            "overview": (
                "A professional website should make the business "
                "easier to understand, easier to trust and easier "
                "to contact."
            ),
            "outcomes": [
                "Clearer positioning and service communication",
                "Improved search and technical performance",
                "More qualified enquiries",
                "A maintainable platform owned by the business",
            ],
        },
        "icon": "browser",
        "sort_order": 10,
        "is_featured": True,
        "cta_title": "Planning a new website?",
        "cta_text": (
            "Tell us what the website must achieve and we will "
            "recommend a practical route forward."
        ),
        "cta_label": "Discuss your website",
        "cta_url": "/request-quote",
        "features": [
            {
                "title": "Discovery and information architecture",
                "description": (
                    "A clear structure based on users, services, "
                    "search intent and commercial priorities."
                ),
                "icon": "structure",
            },
            {
                "title": "Responsive interface design",
                "description": (
                    "Purposeful layouts for desktop, tablet and "
                    "mobile without template-driven visual noise."
                ),
                "icon": "layout",
            },
            {
                "title": "Performance-led development",
                "description": (
                    "Lean implementation, accessible markup and "
                    "technical decisions made for real-world use."
                ),
                "icon": "performance",
            },
            {
                "title": "Conversion foundations",
                "description": (
                    "Clear calls to action, enquiry paths and "
                    "measurement-ready interaction design."
                ),
                "icon": "conversion",
            },
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Understand",
                "description": (
                    "Clarify the business, audience, current "
                    "problems and desired commercial outcome."
                ),
            },
            {
                "step_number": 2,
                "title": "Structure",
                "description": (
                    "Define pages, journeys, content priorities "
                    "and the technical approach."
                ),
            },
            {
                "step_number": 3,
                "title": "Design and build",
                "description": (
                    "Develop the interface and implementation "
                    "through visible review milestones."
                ),
            },
            {
                "step_number": 4,
                "title": "Launch and improve",
                "description": (
                    "Validate quality, deploy responsibly and "
                    "strengthen performance after launch."
                ),
            },
        ],
        "technologies": [
            {
                "name": "Astro",
                "description": (
                    "Content-focused websites with excellent "
                    "performance and maintainable composition."
                ),
            },
            {
                "name": "React",
                "description": (
                    "Interactive product and application "
                    "experiences where richer client behaviour "
                    "is justified."
                ),
            },
            {
                "name": "Laravel",
                "description": (
                    "Reliable business platforms and content-led "
                    "applications with mature conventions."
                ),
            },
            {
                "name": "Django",
                "description": (
                    "Structured, secure systems requiring strong "
                    "administrative and data capabilities."
                ),
            },
        ],
        "faqs": [
            {
                "question": "How long does a business website take?",
                "answer": (
                    "A focused business website commonly takes "
                    "three to six weeks. The final timeline depends "
                    "on scope, content readiness, integrations and "
                    "review speed."
                ),
            },
            {
                "question": (
                    "Will the website be search-engine friendly?"
                ),
                "answer": (
                    "Yes. Semantic structure, crawlability, "
                    "metadata, performance and structured data are "
                    "treated as implementation requirements."
                ),
            },
            {
                "question": (
                    "Can you redesign an existing website?"
                ),
                "answer": (
                    "Yes. We can retain useful content and brand "
                    "equity while improving structure, design, "
                    "technology and conversion paths."
                ),
            },
        ],
        "seo": {
            "meta_title": (
                "Web Development Company | LKProfessionals"
            ),
            "meta_description": (
                "Professional web development for businesses that "
                "need fast, maintainable and search-ready websites "
                "built around measurable outcomes."
            ),
        },
    },
    {
        "title": "Custom Software Development",
        "slug": "custom-software-development",
        "short_description": (
            "Purpose-built software for businesses that have "
            "outgrown spreadsheets, disconnected tools and manual "
            "operational processes."
        ),
        "hero_title": (
            "Software shaped around the way your business "
            "actually works."
        ),
        "hero_description": (
            "We design and build operational systems that connect "
            "people, information and workflows without forcing the "
            "business into an unsuitable off-the-shelf product."
        ),
        "description": {
            "overview": (
                "Custom software is valuable when it removes "
                "repeated friction, improves visibility and creates "
                "dependable operational control."
            ),
            "outcomes": [
                "Less duplicate data entry",
                "Clearer operational accountability",
                "Faster access to reliable information",
                "A system that can evolve with the company",
            ],
        },
        "icon": "code",
        "sort_order": 20,
        "is_featured": True,
        "cta_title": "Have an operational bottleneck?",
        "cta_text": (
            "Walk us through the process. We will help define "
            "whether custom software is commercially sensible."
        ),
        "cta_label": "Discuss the requirement",
        "cta_url": "/request-quote",
        "features": [
            {
                "title": "Business process analysis",
                "description": (
                    "We map the current process before proposing "
                    "screens, features or technology."
                ),
                "icon": "workflow",
            },
            {
                "title": "Role-based operational systems",
                "description": (
                    "Interfaces and permissions aligned with the "
                    "responsibilities of each user group."
                ),
                "icon": "roles",
            },
            {
                "title": "Reporting and visibility",
                "description": (
                    "Operational dashboards and reports built from "
                    "authoritative business data."
                ),
                "icon": "reporting",
            },
            {
                "title": "Integration and automation",
                "description": (
                    "Connections between systems where they remove "
                    "genuine manual effort."
                ),
                "icon": "integration",
            },
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Process discovery",
                "description": (
                    "Document users, decisions, data, exceptions "
                    "and operational risks."
                ),
            },
            {
                "step_number": 2,
                "title": "Solution definition",
                "description": (
                    "Agree scope, architecture, milestones and "
                    "acceptance criteria."
                ),
            },
            {
                "step_number": 3,
                "title": "Incremental delivery",
                "description": (
                    "Build the system in reviewable modules rather "
                    "than a single opaque release."
                ),
            },
            {
                "step_number": 4,
                "title": "Operational adoption",
                "description": (
                    "Deploy, train, monitor and refine using real "
                    "working feedback."
                ),
            },
        ],
        "technologies": [
            {
                "name": "Django",
                "description": "Structured enterprise applications.",
            },
            {
                "name": "Laravel",
                "description": "Mature business web systems.",
            },
            {
                "name": "React",
                "description": "Responsive operational interfaces.",
            },
            {
                "name": "PostgreSQL",
                "description": "Reliable transactional data.",
            },
        ],
        "faqs": [
            {
                "question": "When is custom software justified?",
                "answer": (
                    "It is justified when repeated operational "
                    "friction, data fragmentation or process risk "
                    "costs more than a well-scoped system."
                ),
            },
            {
                "question": (
                    "Can the system be delivered in phases?"
                ),
                "answer": (
                    "Yes. Phased delivery is normally preferable "
                    "because it reduces risk and produces earlier "
                    "operational value."
                ),
            },
            {
                "question": "Will we own the system?",
                "answer": (
                    "Commercial ownership and access arrangements "
                    "are agreed clearly before development begins."
                ),
            },
        ],
        "seo": {
            "meta_title": (
                "Custom Software Development | LKProfessionals"
            ),
            "meta_description": (
                "Custom business software, ERP, CRM and operational "
                "platforms designed around your real processes and "
                "long-term requirements."
            ),
        },
    },
    {
        "title": "E-commerce Development",
        "slug": "ecommerce-development",
        "short_description": (
            "Commercial e-commerce platforms designed for clear "
            "product discovery, dependable operations and "
            "sustainable online growth."
        ),
        "hero_title": (
            "E-commerce that works beyond the checkout page."
        ),
        "hero_description": (
            "We build online stores around the complete commercial "
            "operation: catalogue, customer journey, fulfilment, "
            "payments, reporting and ongoing optimisation."
        ),
        "description": {
            "overview": (
                "A credible online store must balance customer "
                "experience with reliable catalogue and order "
                "operations."
            ),
            "outcomes": [
                "Clearer product discovery",
                "Reduced checkout friction",
                "Reliable order workflows",
                "Better commercial measurement",
            ],
        },
        "icon": "cart",
        "sort_order": 30,
        "is_featured": True,
        "cta_title": "Ready to improve online sales?",
        "cta_text": (
            "Share your product model, current platform and growth "
            "priorities with our team."
        ),
        "cta_label": "Discuss e-commerce",
        "cta_url": "/request-quote",
        "features": [
            {
                "title": "Catalogue architecture",
                "description": (
                    "Products, categories, attributes and filters "
                    "structured for users and search engines."
                ),
                "icon": "catalogue",
            },
            {
                "title": "Checkout and payments",
                "description": (
                    "Practical purchasing journeys with suitable "
                    "payment and fulfilment integrations."
                ),
                "icon": "payment",
            },
            {
                "title": "Operational administration",
                "description": (
                    "Order, customer, inventory and promotional "
                    "tools designed for day-to-day management."
                ),
                "icon": "operations",
            },
            {
                "title": "Growth measurement",
                "description": (
                    "Analytics and conversion tracking prepared for "
                    "informed optimisation."
                ),
                "icon": "analytics",
            },
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Commercial discovery",
                "description": (
                    "Understand products, customers, fulfilment and "
                    "operating constraints."
                ),
            },
            {
                "step_number": 2,
                "title": "Platform planning",
                "description": (
                    "Define catalogue structure, integrations and "
                    "purchase journeys."
                ),
            },
            {
                "step_number": 3,
                "title": "Build and migration",
                "description": (
                    "Implement the store and migrate approved "
                    "product and customer data where required."
                ),
            },
            {
                "step_number": 4,
                "title": "Launch optimisation",
                "description": (
                    "Validate transactions, monitor behaviour and "
                    "improve commercial performance."
                ),
            },
        ],
        "technologies": [
            {
                "name": "WooCommerce",
                "description": "Flexible content-led commerce.",
            },
            {
                "name": "Shopify",
                "description": "Managed commerce operations.",
            },
            {
                "name": "Laravel",
                "description": "Custom commerce workflows.",
            },
            {
                "name": "Stripe",
                "description": "Secure online payment integration.",
            },
        ],
        "faqs": [
            {
                "question": (
                    "Which e-commerce platform should we use?"
                ),
                "answer": (
                    "The answer depends on catalogue complexity, "
                    "operational needs, integrations, budget and "
                    "the level of custom control required."
                ),
            },
            {
                "question": (
                    "Can you migrate an existing online store?"
                ),
                "answer": (
                    "Yes. Migration scope can include products, "
                    "customers, orders, redirects and search "
                    "continuity."
                ),
            },
            {
                "question": (
                    "Do you support payment integrations?"
                ),
                "answer": (
                    "Yes. Suitable providers are selected based on "
                    "market, currency, compliance and business "
                    "requirements."
                ),
            },
        ],
        "seo": {
            "meta_title": (
                "E-commerce Development | LKProfessionals"
            ),
            "meta_description": (
                "E-commerce websites and online stores built for "
                "clear product discovery, reliable order operations "
                "and measurable digital growth."
            ),
        },
    },
    {
        "title": "Search Engine Optimisation",
        "slug": "search-engine-optimisation",
        "short_description": (
            "Sustainable SEO programmes built around technical "
            "quality, commercially useful content and the search "
            "behaviour of real customers."
        ),
        "hero_title": (
            "Search visibility built on useful work—not shortcuts."
        ),
        "hero_description": (
            "LKProfessionals improves technical foundations, page "
            "quality and content coverage so businesses can earn "
            "relevant visibility over time."
        ),
        "description": {
            "overview": (
                "SEO is an operating discipline combining technical "
                "quality, useful content and credible market signals."
            ),
            "outcomes": [
                "Improved crawlability and indexation",
                "Stronger coverage of commercial search intent",
                "Better local and service visibility",
                "Clearer measurement of organic performance",
            ],
        },
        "icon": "search",
        "sort_order": 40,
        "is_featured": True,
        "cta_title": "Need stronger organic visibility?",
        "cta_text": (
            "We can review the technical, content and commercial "
            "gaps holding the website back."
        ),
        "cta_label": "Request an SEO review",
        "cta_url": "/request-quote",
        "features": [
            {
                "title": "Technical SEO",
                "description": (
                    "Indexation, rendering, structure, internal "
                    "linking and performance fundamentals."
                ),
                "icon": "technical",
            },
            {
                "title": "Search-led content planning",
                "description": (
                    "Pages and topics selected by commercial "
                    "relevance rather than publishing volume."
                ),
                "icon": "content",
            },
            {
                "title": "On-page optimisation",
                "description": (
                    "Clearer titles, headings, copy, entities and "
                    "structured data."
                ),
                "icon": "page",
            },
            {
                "title": "Reporting and prioritisation",
                "description": (
                    "Transparent progress reporting with the next "
                    "most valuable actions identified."
                ),
                "icon": "report",
            },
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Audit",
                "description": (
                    "Identify technical, content and authority "
                    "constraints."
                ),
            },
            {
                "step_number": 2,
                "title": "Prioritise",
                "description": (
                    "Rank work by commercial impact and practical "
                    "effort."
                ),
            },
            {
                "step_number": 3,
                "title": "Implement",
                "description": (
                    "Resolve technical issues and strengthen key "
                    "pages and content."
                ),
            },
            {
                "step_number": 4,
                "title": "Measure",
                "description": (
                    "Track visibility, qualified traffic and "
                    "commercial outcomes."
                ),
            },
        ],
        "technologies": [
            {
                "name": "Google Search Console",
                "description": "Search performance.",
            },
            {
                "name": "Google Analytics",
                "description": "Behaviour and conversion.",
            },
            {
                "name": "Schema.org",
                "description": "Structured meaning.",
            },
            {
                "name": "Astro",
                "description": "Performance-focused publishing.",
            },
        ],
        "faqs": [
            {
                "question": "How long does SEO take?",
                "answer": (
                    "Meaningful progress normally requires several "
                    "months. Timing depends on competition, site "
                    "condition, content and historical authority."
                ),
            },
            {
                "question": "Do you guarantee first position?",
                "answer": (
                    "No responsible provider can guarantee a "
                    "specific organic position. We guarantee a clear "
                    "process and accountable implementation."
                ),
            },
            {
                "question": (
                    "Can SEO support international markets?"
                ),
                "answer": (
                    "Yes. Market structure, language, localisation "
                    "and regional search intent must be planned "
                    "carefully."
                ),
            },
        ],
        "seo": {
            "meta_title": "SEO Services | LKProfessionals",
            "meta_description": (
                "Technical SEO, content strategy and search "
                "optimisation focused on relevant visibility, "
                "qualified traffic and sustainable growth."
            ),
        },
    },
    {
        "title": "Local SEO",
        "slug": "local-seo",
        "short_description": (
            "Local search programmes for businesses that need to "
            "be found, trusted and contacted in defined service "
            "areas."
        ),
        "hero_title": (
            "Become easier to find where the business actually "
            "operates."
        ),
        "hero_description": (
            "We improve local relevance across the website, Google "
            "Business Profile and supporting business signals."
        ),
        "description": {
            "overview": (
                "Local visibility depends on consistent business "
                "information, locally relevant pages and a credible "
                "customer presence."
            ),
            "outcomes": [
                "Improved local service visibility",
                "Stronger Google Business Profile quality",
                "More consistent business information",
                "Clearer service-area relevance",
            ],
        },
        "icon": "map-pin",
        "sort_order": 50,
        "is_featured": False,
        "cta_title": "Need more local enquiries?",
        "cta_text": (
            "We can assess your website, business profile and local "
            "competitive position."
        ),
        "cta_label": "Discuss local SEO",
        "cta_url": "/request-quote",
        "features": [
            {
                "title": "Google Business Profile",
                "description": (
                    "Categories, services, content and operating "
                    "information managed coherently."
                ),
                "icon": "profile",
            },
            {
                "title": "Local landing pages",
                "description": (
                    "Useful location and service-area pages without "
                    "thin duplication."
                ),
                "icon": "location",
            },
            {
                "title": "Citation consistency",
                "description": (
                    "Business details reviewed across important "
                    "local sources."
                ),
                "icon": "citation",
            },
            {
                "title": "Review strategy",
                "description": (
                    "A practical process for earning and responding "
                    "to authentic customer feedback."
                ),
                "icon": "reviews",
            },
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Assess",
                "description": "Review local search presence.",
            },
            {
                "step_number": 2,
                "title": "Correct",
                "description": "Resolve inconsistent information.",
            },
            {
                "step_number": 3,
                "title": "Strengthen",
                "description": "Improve pages and profile data.",
            },
            {
                "step_number": 4,
                "title": "Maintain",
                "description": "Publish, review and monitor.",
            },
        ],
        "technologies": [
            {
                "name": "Google Business Profile",
                "description": "Local presence.",
            },
            {
                "name": "Google Maps",
                "description": "Geographic visibility.",
            },
            {
                "name": "Schema.org",
                "description": "Local business data.",
            },
            {
                "name": "Search Console",
                "description": "Organic measurement.",
            },
        ],
        "faqs": [
            {
                "question": (
                    "Is local SEO only for physical shops?"
                ),
                "answer": (
                    "No. Service-area businesses can also build "
                    "local relevance when represented accurately."
                ),
            },
            {
                "question": (
                    "Do reviews affect local visibility?"
                ),
                "answer": (
                    "Reviews contribute to trust and can support "
                    "local prominence, but they are only one part "
                    "of the system."
                ),
            },
            {
                "question": (
                    "Should we create a page for every location?"
                ),
                "answer": (
                    "Only when each page provides genuinely useful "
                    "and distinct local information."
                ),
            },
        ],
        "seo": {
            "meta_title": "Local SEO Services | LKProfessionals",
            "meta_description": (
                "Local SEO and Google Business Profile support for "
                "businesses seeking stronger visibility and more "
                "qualified enquiries in service areas."
            ),
        },
    },
    {
        "title": "Website Maintenance",
        "slug": "website-maintenance",
        "short_description": (
            "Ongoing technical maintenance, monitoring and "
            "improvement for organisations that cannot afford to "
            "let their website quietly deteriorate."
        ),
        "hero_title": (
            "Keep the website secure, current and useful."
        ),
        "hero_description": (
            "Structured website maintenance covering updates, "
            "technical monitoring, fixes and continuous improvement."
        ),
        "description": {
            "overview": (
                "Maintenance protects the investment already made "
                "in the website and reduces preventable operational "
                "risk."
            ),
            "outcomes": [
                "Reduced technical risk",
                "Faster issue resolution",
                "Consistent platform updates",
                "Ongoing performance improvement",
            ],
        },
        "icon": "tools",
        "sort_order": 60,
        "is_featured": False,
        "cta_title": "Need dependable website support?",
        "cta_text": (
            "We can review the current platform and propose a "
            "sensible maintenance arrangement."
        ),
        "cta_label": "Discuss maintenance",
        "cta_url": "/request-quote",
        "features": [
            {
                "title": "Platform updates",
                "description": (
                    "Controlled framework, dependency and plugin "
                    "maintenance."
                ),
                "icon": "update",
            },
            {
                "title": "Monitoring",
                "description": (
                    "Availability, errors and technical quality "
                    "reviewed regularly."
                ),
                "icon": "monitor",
            },
            {
                "title": "Content support",
                "description": (
                    "Approved page and content updates delivered "
                    "without unnecessary delay."
                ),
                "icon": "content",
            },
            {
                "title": "Improvement backlog",
                "description": (
                    "Small enhancements prioritised according to "
                    "business value."
                ),
                "icon": "backlog",
            },
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Review",
                "description": "Assess platform condition and risk.",
            },
            {
                "step_number": 2,
                "title": "Stabilise",
                "description": "Resolve urgent technical issues.",
            },
            {
                "step_number": 3,
                "title": "Maintain",
                "description": "Apply controlled recurring work.",
            },
            {
                "step_number": 4,
                "title": "Improve",
                "description": "Deliver valuable enhancements.",
            },
        ],
        "technologies": [
            {
                "name": "Uptime monitoring",
                "description": "Availability awareness.",
            },
            {
                "name": "Git",
                "description": "Controlled source changes.",
            },
            {
                "name": "Automated backups",
                "description": "Recovery readiness.",
            },
            {
                "name": "Security updates",
                "description": "Risk reduction.",
            },
        ],
        "faqs": [
            {
                "question": (
                    "What does website maintenance include?"
                ),
                "answer": (
                    "The exact scope is agreed, but commonly "
                    "includes updates, monitoring, fixes, backups "
                    "and minor improvements."
                ),
            },
            {
                "question": (
                    "Can you maintain a website you did not build?"
                ),
                "answer": (
                    "Usually yes, after a technical review confirms "
                    "the platform is supportable."
                ),
            },
            {
                "question": "Is hosting included?",
                "answer": (
                    "Hosting can be included or managed separately "
                    "depending on the arrangement."
                ),
            },
        ],
        "seo": {
            "meta_title": (
                "Website Maintenance Services | LKProfessionals"
            ),
            "meta_description": (
                "Professional website maintenance, monitoring, "
                "updates and technical support for dependable "
                "long-term website operation."
            ),
        },
    },
    {
        "title": "Google Ads Management",
        "slug": "google-ads-management",
        "short_description": (
            "Search advertising managed around qualified "
            "commercial intent, responsible measurement and "
            "controlled spending."
        ),
        "hero_title": (
            "Paid search managed for enquiries—not vanity traffic."
        ),
        "hero_description": (
            "We structure Google Ads campaigns around the services, "
            "locations and search terms most likely to produce "
            "commercially useful action."
        ),
        "description": {
            "overview": (
                "Google Ads works best when campaign structure, "
                "landing pages and conversion measurement are "
                "treated as one system."
            ),
            "outcomes": [
                "More relevant search traffic",
                "Reduced wasted spend",
                "Clearer conversion measurement",
                "Better landing-page alignment",
            ],
        },
        "icon": "ads",
        "sort_order": 70,
        "is_featured": False,
        "cta_title": "Need accountable paid search?",
        "cta_text": (
            "Share the market, services and current campaign "
            "performance with us."
        ),
        "cta_label": "Discuss Google Ads",
        "cta_url": "/request-quote",
        "features": [
            {
                "title": "Campaign structure",
                "description": (
                    "Services, locations and intent separated for "
                    "control and relevance."
                ),
                "icon": "campaign",
            },
            {
                "title": "Keyword governance",
                "description": (
                    "Search terms, negatives and match types managed "
                    "actively."
                ),
                "icon": "keywords",
            },
            {
                "title": "Conversion tracking",
                "description": (
                    "Meaningful actions measured rather than clicks "
                    "reported in isolation."
                ),
                "icon": "tracking",
            },
            {
                "title": "Landing-page alignment",
                "description": (
                    "Ad promise, page content and CTA connected "
                    "coherently."
                ),
                "icon": "landing",
            },
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Define",
                "description": "Agree objectives and conversions.",
            },
            {
                "step_number": 2,
                "title": "Structure",
                "description": "Build campaigns and targeting.",
            },
            {
                "step_number": 3,
                "title": "Launch",
                "description": "Deploy with controlled budgets.",
            },
            {
                "step_number": 4,
                "title": "Optimise",
                "description": (
                    "Improve using search and lead data."
                ),
            },
        ],
        "technologies": [
            {
                "name": "Google Ads",
                "description": "Paid search delivery.",
            },
            {
                "name": "Google Tag Manager",
                "description": "Tracking governance.",
            },
            {
                "name": "Google Analytics",
                "description": "Behaviour measurement.",
            },
            {
                "name": "Looker Studio",
                "description": "Reporting visibility.",
            },
        ],
        "faqs": [
            {
                "question": "What budget should we start with?",
                "answer": (
                    "The right budget depends on market demand, cost "
                    "per click, service value and the volume required "
                    "for useful learning."
                ),
            },
            {
                "question": "Do you guarantee leads?",
                "answer": (
                    "No campaign can responsibly guarantee a fixed "
                    "lead volume. We focus on relevance, control and "
                    "transparent optimisation."
                ),
            },
            {
                "question": (
                    "Do we retain ownership of the account?"
                ),
                "answer": (
                    "Yes. The advertising account should remain "
                    "under the client's ownership."
                ),
            },
        ],
        "seo": {
            "meta_title": (
                "Google Ads Management | LKProfessionals"
            ),
            "meta_description": (
                "Google Ads campaign management focused on "
                "qualified search intent, controlled spending and "
                "measurable enquiries."
            ),
        },
    },
    {
        "title": "IT Consulting",
        "slug": "it-consulting",
        "short_description": (
            "Practical technology advice for organisations making "
            "important platform, infrastructure or digital "
            "investment decisions."
        ),
        "hero_title": (
            "Independent technical thinking before expensive "
            "decisions are made."
        ),
        "hero_description": (
            "LKProfessionals helps businesses define requirements, "
            "assess options and reduce technical risk before "
            "committing to a platform or project."
        ),
        "description": {
            "overview": (
                "Good technical advice connects operational reality, "
                "commercial priorities and long-term ownership."
            ),
            "outcomes": [
                "Clearer requirements",
                "Reduced procurement risk",
                "More defensible platform decisions",
                "A practical implementation roadmap",
            ],
        },
        "icon": "consulting",
        "sort_order": 80,
        "is_featured": True,
        "cta_title": "Facing a technology decision?",
        "cta_text": (
            "We can provide a structured assessment before you "
            "commit budget or operational dependency."
        ),
        "cta_label": "Discuss the decision",
        "cta_url": "/contact",
        "features": [
            {
                "title": "Requirements definition",
                "description": (
                    "Translate business needs into testable technical "
                    "and operational requirements."
                ),
                "icon": "requirements",
            },
            {
                "title": "Platform assessment",
                "description": (
                    "Compare viable options against cost, control, "
                    "risk and future needs."
                ),
                "icon": "assessment",
            },
            {
                "title": "Architecture review",
                "description": (
                    "Review systems, integrations, data and "
                    "operational dependencies."
                ),
                "icon": "architecture",
            },
            {
                "title": "Delivery planning",
                "description": (
                    "Define milestones, responsibilities and "
                    "acceptance criteria."
                ),
                "icon": "planning",
            },
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Clarify",
                "description": (
                    "Define the decision and constraints."
                ),
            },
            {
                "step_number": 2,
                "title": "Investigate",
                "description": (
                    "Gather operational evidence."
                ),
            },
            {
                "step_number": 3,
                "title": "Evaluate",
                "description": "Compare practical options.",
            },
            {
                "step_number": 4,
                "title": "Recommend",
                "description": (
                    "Present a defensible route forward."
                ),
            },
        ],
        "technologies": [
            {
                "name": "Architecture review",
                "description": "System-level analysis.",
            },
            {
                "name": "Process mapping",
                "description": "Operational clarity.",
            },
            {
                "name": "Risk assessment",
                "description": "Decision governance.",
            },
            {
                "name": "Delivery roadmap",
                "description": "Implementation planning.",
            },
        ],
        "faqs": [
            {
                "question": (
                    "Can you review another supplier's proposal?"
                ),
                "answer": (
                    "Yes. We can assess scope, architecture, "
                    "assumptions, ownership and delivery risk."
                ),
            },
            {
                "question": (
                    "Do you provide consultation without "
                    "development?"
                ),
                "answer": (
                    "Yes. Advisory work can be completely independent "
                    "of implementation."
                ),
            },
            {
                "question": (
                    "Can you help define an ERP or CRM project?"
                ),
                "answer": (
                    "Yes. Requirements definition before supplier "
                    "selection can substantially reduce project risk."
                ),
            },
        ],
        "seo": {
            "meta_title": "IT Consulting Services | LKProfessionals",
            "meta_description": (
                "Independent IT consulting, platform assessment, "
                "requirements definition and technical planning for "
                "important business technology decisions."
            ),
        },
    },
)


class Command(BaseCommand):
    help = (
        "Seed the initial published LKProfessionals public "
        "service catalogue."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        published_at = timezone.now()

        for raw_definition in SERVICE_DEFINITIONS:
            definition = deepcopy(raw_definition)

            features = definition.pop("features")
            process_steps = definition.pop("process_steps")
            technologies = definition.pop("technologies")
            faqs = definition.pop("faqs")
            seo = definition.pop("seo")

            service, created = Service.objects.update_or_create(
                slug=definition["slug"],
                defaults={
                    **definition,
                    "status": ServiceStatus.PUBLISHED,
                    "published_at": published_at,
                    "scheduled_for": None,
                    "is_active": True,
                },
            )

            service.features.all().delete()
            service.process_steps.all().delete()
            service.technologies.all().delete()
            service.faqs.all().delete()

            ServiceFeature.objects.bulk_create(
                [
                    ServiceFeature(
                        service=service,
                        title=item["title"],
                        description=item["description"],
                        icon=item["icon"],
                        sort_order=index,
                    )
                    for index, item in enumerate(
                        features,
                        start=1,
                    )
                ]
            )

            ServiceProcessStep.objects.bulk_create(
                [
                    ServiceProcessStep(
                        service=service,
                        title=item["title"],
                        description=item["description"],
                        step_number=item["step_number"],
                        sort_order=index,
                    )
                    for index, item in enumerate(
                        process_steps,
                        start=1,
                    )
                ]
            )

            ServiceTechnology.objects.bulk_create(
                [
                    ServiceTechnology(
                        service=service,
                        name=item["name"],
                        description=item["description"],
                        sort_order=index,
                    )
                    for index, item in enumerate(
                        technologies,
                        start=1,
                    )
                ]
            )

            ServiceFaq.objects.bulk_create(
                [
                    ServiceFaq(
                        service=service,
                        question=item["question"],
                        answer=item["answer"],
                        sort_order=index,
                    )
                    for index, item in enumerate(
                        faqs,
                        start=1,
                    )
                ]
            )

            canonical_url = (
                "https://lkprofessionals.com/"
                f"services/{service.slug}"
            )

            structured_data = {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": service.title,
                "url": canonical_url,
                "provider": {
                    "@type": "Organization",
                    "name": "LKProfessionals",
                    "url": "https://lkprofessionals.com",
                },
            }

            ServiceSeo.objects.update_or_create(
                service=service,
                defaults={
                    **seo,
                    "canonical_url": canonical_url,
                    "robots_index": True,
                    "robots_follow": True,
                    "open_graph_title": seo["meta_title"],
                    "open_graph_description": (
                        seo["meta_description"]
                    ),
                    "open_graph_image_id": None,
                    "twitter_title": seo["meta_title"],
                    "twitter_description": (
                        seo["meta_description"]
                    ),
                    "structured_data": structured_data,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Public service catalogue seeded: "
                f"{created_count} created, "
                f"{updated_count} updated."
            )
        )
