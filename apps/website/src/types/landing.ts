export interface NavigationItem {
  label: string;
  href: string;
}

export interface ServiceSummary {
  number: string;
  title: string;
  description: string;
  href: string;
  capabilities: string[];
}

export interface ProcessStep {
  number: string;
  title: string;
  description: string;
}

export interface ProofPoint {
  value: string;
  label: string;
  note: string;
}
