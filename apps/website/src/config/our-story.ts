export interface StoryMilestone {
  year: string;
  label: string;
  title: string;
  description: string;
}

export interface StoryPrinciple {
  number: string;
  title: string;
  description: string;
}

export const storyMilestones: StoryMilestone[] = [
  {
    year: "2013",
    label: "The beginning",
    title: "LKProfessionals begins its journey.",
    description:
      "The story started with practical technology work and a simple objective: help people and businesses solve real problems using dependable IT solutions.",
  },
  {
    year: "2013–2023",
    label: "Building experience",
    title: "Capability grew through real work.",
    description:
      "Over the following years, the scope expanded across websites, software, digital services, technical support and business technology while experience was built project by project.",
  },
  {
    year: "2024",
    label: "Formal incorporation",
    title: "LKProfessionals became LKProfessionals (Pvt) Ltd.",
    description:
      "Formal incorporation established the next stage of the company: a structured technology business designed to grow beyond individual projects and support longer-term client relationships.",
  },
  {
    year: "Today",
    label: "The next chapter",
    title: "A broader technology company with international ambition.",
    description:
      "From Jaffna, LKProfessionals is building deeper capabilities across engineering, digital growth, automation, infrastructure and technology consulting while serving businesses locally and beyond Sri Lanka.",
  },
];

export const storyPrinciples: StoryPrinciple[] = [
  {
    number: "01",
    title: "Practical beginnings",
    description:
      "The company was built around solving problems rather than chasing technology for its own sake.",
  },
  {
    number: "02",
    title: "Experience earned through delivery",
    description:
      "Capability has developed through years of real projects, changing technologies and client requirements.",
  },
  {
    number: "03",
    title: "Growth with structure",
    description:
      "As the company expands, processes, systems and accountability are being strengthened rather than left informal.",
  },
  {
    number: "04",
    title: "Long-term direction",
    description:
      "The objective is to build a sustainable technology company capable of supporting clients across markets and over time.",
  },
];
