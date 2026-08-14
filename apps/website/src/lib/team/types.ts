export interface PublicTeamService {
  service_title: string;
  is_public: boolean;
}

export interface PublicTeamMember {
  id: string;
  display_name: string;
  job_title: string;
  professional_title: string;
  profile_image_url: string;
  short_bio: string;
  country: string;

  linkedin_url: string;
  github_url: string;
  portfolio_url: string;
  website_url: string;

  is_leadership: boolean;
  is_featured: boolean;

  services: PublicTeamService[];
}

export interface PublicTeam {
  id: string;
  name: string;
  slug: string;
  team_type: string;
  description: string;

  members: PublicTeamMember[];
}
