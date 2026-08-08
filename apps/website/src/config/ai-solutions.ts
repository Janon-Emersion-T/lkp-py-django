export interface AiSolutionService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface AiPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface AiUseCase {
  number: string;
  title: string;
  description: string;
}

export const aiSolutionServices: AiSolutionService[] = [
  {
    number: "01",
    title: "AI Chatbots",
    href: "/services/ai-solutions/ai-chatbots/",
    description:
      "Conversational interfaces that help customers or internal teams find information, complete defined tasks and receive guided support.",
    capabilities: [
      "Customer support",
      "Knowledge retrieval",
      "Lead qualification",
      "Guided interactions",
    ],
  },
  {
    number: "02",
    title: "AI Automation",
    href: "/services/ai-solutions/ai-automation/",
    description:
      "Use AI where interpretation, classification or generation can reduce repetitive work inside wider business workflows.",
    capabilities: [
      "Document processing",
      "Classification",
      "Content workflows",
      "Decision assistance",
    ],
  },
  {
    number: "03",
    title: "AI Assistants",
    href: "/services/ai-solutions/ai-assistants/",
    description:
      "Task-oriented assistants designed around specific business contexts, information sources and user responsibilities.",
    capabilities: [
      "Internal assistants",
      "Research support",
      "Knowledge access",
      "Task assistance",
    ],
  },
  {
    number: "04",
    title: "AI Integration",
    href: "/services/ai-solutions/ai-integration/",
    description:
      "Introduce AI capabilities into existing websites, software and operational systems rather than rebuilding the entire technology stack.",
    capabilities: [
      "AI APIs",
      "Existing software",
      "Workflow integration",
      "Data connections",
    ],
  },
  {
    number: "05",
    title: "Custom AI Solutions",
    href: "/services/ai-solutions/custom-ai-solutions/",
    description:
      "Design purpose-built AI-enabled applications where off-the-shelf tools do not adequately fit the business problem.",
    capabilities: [
      "Custom workflows",
      "Domain-specific tools",
      "AI-enabled software",
      "Solution prototyping",
    ],
  },
];

export const aiPrinciples: AiPrinciple[] = [
  {
    number: "01",
    title: "Use AI where uncertainty exists",
    description:
      "AI is most useful where the work involves interpretation, language, classification or generation. Clear deterministic rules often belong in normal software.",
  },
  {
    number: "02",
    title: "Keep humans in control of important decisions",
    description:
      "High-impact actions should have appropriate approval, review or escalation rather than relying blindly on model output.",
  },
  {
    number: "03",
    title: "Ground outputs in relevant information",
    description:
      "Useful AI systems need controlled context, suitable data and clear boundaries instead of relying on generic model knowledge alone.",
  },
  {
    number: "04",
    title: "Design for imperfect answers",
    description:
      "AI systems can make mistakes. Workflows should account for uncertainty, validation and fallback behaviour from the beginning.",
  },
];

export const aiUseCases: AiUseCase[] = [
  {
    number: "01",
    title: "Customer support",
    description:
      "Handle common enquiries, surface relevant information and route complex cases to people.",
  },
  {
    number: "02",
    title: "Knowledge access",
    description:
      "Help teams find answers across internal documents, policies or structured business information.",
  },
  {
    number: "03",
    title: "Document processing",
    description:
      "Extract, classify, summarise or organise information from recurring document workflows.",
  },
  {
    number: "04",
    title: "Sales assistance",
    description:
      "Support lead qualification, response preparation, account research and follow-up workflows.",
  },
  {
    number: "05",
    title: "Content operations",
    description:
      "Assist with structured drafting, transformation and review while keeping human oversight.",
  },
  {
    number: "06",
    title: "Operational assistance",
    description:
      "Support staff with repetitive analysis, information retrieval and routine decision preparation.",
  },
];
