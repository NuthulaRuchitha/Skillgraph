const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export interface Job {
  job_id: string;
  job_title: string;
  company: string;
}

export interface RelatedSkill {
  skill: string;
  category: string;
}

export interface CompanyConnection {
  skill: string;
  job: string;
  company: string;
  industry: string;
}

export async function getJobsBySkill(
  skill: string
): Promise<Job[]> {
  const response = await fetch(
    `${API_URL}/api/jobs?skill=${encodeURIComponent(skill)}`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch jobs");
  }

  const data = await response.json();

  return data.jobs;
}


export async function getRelatedSkills(
  skill: string
): Promise<RelatedSkill[]> {
  const response = await fetch(
    `${API_URL}/api/skills/${encodeURIComponent(skill)}/related`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch related skills");
  }

  const data = await response.json();

  return data.related_skills;
}


export async function getSkillCompanies(
  skill: string
): Promise<CompanyConnection[]> {
  const response = await fetch(
    `${API_URL}/api/skills/${encodeURIComponent(skill)}/companies`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch company connections");
  }

  const data = await response.json();

  return data.connections;
}