"use client";

import { useState } from "react";
import { searchJobs, getJobDetails, getJobGraph, SkillGraph, Job, JobDetails } from "@/lib/api";
import GraphExplorer from "./GraphExplorer";

export default function JobSearch() {
  const [skill, setSkill] = useState("");
  const [city, setCity] = useState("");
  const [industry, setIndustry] = useState("");
  const [technology, setTechnology] = useState("");

  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedJob, setSelectedJob] =
    useState<JobDetails | null>(null);

  const [detailsLoading, setDetailsLoading] =
    useState(false);

  const [detailsError, setDetailsError] =
    useState("");

  const [jobGraph, setJobGraph] =
  useState<SkillGraph | null>(null);

  const [graphLoading, setGraphLoading] =
    useState(false);

  const [graphError, setGraphError] =
    useState("");

  async function handleSearch() {
    setLoading(true);
    setError("");

    try {
      const results = await searchJobs({
        skill: skill.trim() || undefined,
        city: city.trim() || undefined,
        industry: industry.trim() || undefined,
        technology: technology.trim() || undefined,
      });

      setJobs(results);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to search jobs"
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleJobClick(jobId: string) {
    setDetailsLoading(true);
    setDetailsError("");

    try {
      const details = await getJobDetails(jobId);
      setSelectedJob(details);
    } catch (err) {
      setDetailsError(
        err instanceof Error
          ? err.message
          : "Failed to load job details"
      );
    } finally {
      setDetailsLoading(false);
    }
  }

  async function handleExploreGraph(jobId: string) {
    setGraphLoading(true);
    setGraphError("");

    try {
      const graph = await getJobGraph(jobId);
      setJobGraph(graph);
    } catch (err) {
      setGraphError(
        err instanceof Error
          ? err.message
          : "Failed to load job graph"
      );
    } finally {
      setGraphLoading(false);
    }
  }

  function handleClear() {
    setSkill("");
    setCity("");
    setIndustry("");
    setTechnology("");
    setJobs([]);
    setError("");
  }

  return (
    <section className="w-full">
      <div className="rounded-xl border border-slate-800 bg-slate-950 p-6">
        <h2 className="text-xl font-semibold text-white">
          Job Search
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Search jobs using graph-based filters.
        </p>

        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <input
            value={skill}
            onChange={(e) => setSkill(e.target.value)}
            placeholder="Skill e.g. Java"
            className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none"
          />

          <input
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="City e.g. Hyderabad"
            className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none"
          />

          <input
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
            placeholder="Industry e.g. FinTech"
            className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none"
          />

          <input
            value={technology}
            onChange={(e) => setTechnology(e.target.value)}
            placeholder="Technology e.g. Spring Boot"
            className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none"
          />
        </div>

        <div className="mt-5 flex gap-3">
          <button
            onClick={handleSearch}
            disabled={loading}
            className="rounded-lg bg-blue-600 px-5 py-3 font-medium text-white disabled:opacity-50"
          >
            {loading ? "Searching..." : "Search Jobs"}
          </button>

          <button
            onClick={handleClear}
            className="rounded-lg border border-slate-700 px-5 py-3 font-medium text-slate-300"
          >
            Clear
          </button>
        </div>

        {error && (
          <p className="mt-4 text-sm text-red-400">
            {error}
          </p>
        )}
      </div>

      <div className="mt-6">
        {jobs.length > 0 && (
          <p className="mb-4 text-sm text-slate-400">
            {jobs.length} job{jobs.length !== 1 ? "s" : ""} found
          </p>
        )}

        <div className="grid gap-4 md:grid-cols-2">
          {jobs.map((job) => (
            <article
              key={job.job_id}
              onClick={() => handleJobClick(job.job_id)}
              className="cursor-pointer rounded-xl border border-slate-800 bg-slate-950 p-5 transition hover:border-blue-500"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="text-lg font-semibold text-white">
                    {job.job_title}
                  </h3>

                  <p className="mt-1 text-slate-400">
                    {job.company}
                  </p>
                </div>

                <span className="rounded-full bg-blue-500/10 px-3 py-1 text-xs text-blue-400">
                  {job.job_id}
                </span>
              </div>

              <div className="mt-4 flex flex-wrap gap-2 text-sm">
                {job.city && (
                  <span className="rounded-md bg-slate-800 px-3 py-1 text-slate-300">
                    📍 {job.city}
                  </span>
                )}

                {job.industry && (
                  <span className="rounded-md bg-slate-800 px-3 py-1 text-slate-300">
                    {job.industry}
                  </span>
                )}
              </div>
            </article>
          ))}
        </div>

        {!loading && jobs.length === 0 && (
          <div className="rounded-xl border border-dashed border-slate-800 p-10 text-center">
            <p className="text-slate-400">
              Enter filters and search for jobs.
            </p>
          </div>
        )}
      </div>
      {detailsLoading && (
        <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-6">
          <p className="text-slate-400">
            Loading job details...
          </p>
        </div>
      )}

      {detailsError && (
        <div className="mt-6 rounded-xl border border-red-900 bg-red-950/30 p-6">
          <p className="text-red-400">
            {detailsError}
          </p>
        </div>
      )}

      {selectedJob && !detailsLoading && (
        <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold text-white">
                {selectedJob.job_title}
              </h2>

              <p className="mt-1 text-slate-400">
                {selectedJob.company}
              </p>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() =>
                  handleExploreGraph(selectedJob.job_id)
                }
                disabled={graphLoading}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
              >
                {graphLoading ? "Loading Graph..." : "Explore Graph"}
              </button>

              <button
                onClick={() => {
                  setSelectedJob(null);
                  setJobGraph(null);
                  setGraphError("");
                }}
                className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300"
              >
                Close
              </button>
            </div>
          </div>

          <div className="mt-5 grid gap-4 sm:grid-cols-3">
            <div className="rounded-lg bg-slate-900 p-4">
              <p className="text-xs text-slate-500">
                Location
              </p>

              <p className="mt-1 text-white">
                {selectedJob.city || "N/A"}
              </p>
            </div>

            <div className="rounded-lg bg-slate-900 p-4">
              <p className="text-xs text-slate-500">
                Industry
              </p>

              <p className="mt-1 text-white">
                {selectedJob.industry || "N/A"}
              </p>
            </div>

            <div className="rounded-lg bg-slate-900 p-4">
              <p className="text-xs text-slate-500">
                Job ID
              </p>

              <p className="mt-1 text-white">
                {selectedJob.job_id}
              </p>
            </div>
          </div>

          <div className="mt-6">
            <h3 className="font-semibold text-white">
              Required Skills
            </h3>

            <div className="mt-3 flex flex-wrap gap-2">
              {selectedJob.skills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-full bg-blue-500/10 px-3 py-1 text-sm text-blue-400"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="mt-6">
            <h3 className="font-semibold text-white">
              Technologies
            </h3>

            <div className="mt-3 flex flex-wrap gap-2">
              {selectedJob.technologies.map(
                (technology) => (
                  <span
                    key={technology}
                    className="rounded-full bg-emerald-500/10 px-3 py-1 text-sm text-emerald-400"
                  >
                    {technology}
                  </span>
                )
              )}
            </div>
          </div>
        </div>
      )}
      {graphError && (
      <div className="mt-6 rounded-xl border border-red-900 bg-red-950/30 p-6">
        <p className="text-red-400">
          {graphError}
        </p>
      </div>
    )}

    {jobGraph && !graphLoading && (
      <div className="mt-6">
        <div className="mb-3">
          <h2 className="text-xl font-semibold text-white">
            Job Relationship Graph
          </h2>

          <p className="mt-1 text-sm text-slate-400">
            Explore how this job connects to skills,
            technologies, company, location, and industry.
          </p>
        </div>

        <GraphExplorer graph={jobGraph} />
      </div>
    )}
    </section>
  ); 
}