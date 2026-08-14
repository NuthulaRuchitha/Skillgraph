const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export interface Job {
  job_id: string;
  job_title: string;
  company: string;
  city: string | null;
  industry: string | null;
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

export interface GraphNode {
  id: string;
  label: string;
  name: string;
}

export interface GraphRelationship {
  source: string;
  target: string;
  type: string;
}

export interface SkillGraph {
  nodes: GraphNode[];
  relationships: GraphRelationship[];
}

export async function getSkillGraph(
  skill: string
): Promise<SkillGraph> {
  const response = await fetch(
    `${API_URL}/api/graph/${encodeURIComponent(skill)}`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch graph");
  }

  return response.json();
}


export async function searchJobs(params: {
  skill?: string;
  city?: string;
  industry?: string;
  technology?: string;
}): Promise<Job[]> {
  const searchParams = new URLSearchParams();

  if (params.skill) {
    searchParams.set("skill", params.skill);
  }

  if (params.city) {
    searchParams.set("city", params.city);
  }

  if (params.industry) {
    searchParams.set("industry", params.industry);
  }

  if (params.technology) {
    searchParams.set("technology", params.technology);
  }

  const response = await fetch(
    `${API_URL}/api/jobs/search?${searchParams.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to search jobs");
  }

  return response.json();
}

export interface JobDetails {
  job_id: string;
  job_title: string;
  company: string;
  industry: string | null;
  city: string | null;
  skills: string[];
  technologies: string[];
}

export async function getJobDetails(
  jobId: string
): Promise<JobDetails> {
  const response = await fetch(
    `${API_URL}/api/jobs/${encodeURIComponent(jobId)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch job details");
  }

  return response.json();
}

export async function getJobGraph(
  jobId: string
): Promise<SkillGraph> {
  const response = await fetch(
    `${API_URL}/api/jobs/${encodeURIComponent(jobId)}/graph`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch job graph");
  }

  return response.json();
}