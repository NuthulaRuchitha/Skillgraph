"use client";

import { useState } from "react";
import {
  Search,
  BriefcaseBusiness,
  Building2,
  ArrowRight,
  Network,
  Sparkles,
} from "lucide-react";

import {
  getJobsBySkill,
  getRelatedSkills,
  getSkillCompanies,
  type Job,
  type RelatedSkill,
  type CompanyConnection,
} from "@/lib/api";


const popularSkills = [
  "Java",
  "Python",
  "React",
  "SQL",
];


export default function Home() {
  const [skill, setSkill] = useState("Java");
  const [searchedSkill, setSearchedSkill] = useState("Java");

  const [jobs, setJobs] = useState<Job[]>([]);
  const [relatedSkills, setRelatedSkills] = useState<RelatedSkill[]>([]);
  const [companies, setCompanies] = useState<CompanyConnection[]>([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  async function exploreSkill(selectedSkill = skill) {
    if (!selectedSkill.trim()) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const [
        jobsResult,
        relatedResult,
        companiesResult,
      ] = await Promise.all([
        getJobsBySkill(selectedSkill),
        getRelatedSkills(selectedSkill),
        getSkillCompanies(selectedSkill),
      ]);

      setJobs(jobsResult);
      setRelatedSkills(relatedResult);
      setCompanies(companiesResult);
      setSearchedSkill(selectedSkill);
    } catch {
      setError(
        "Unable to connect to SkillGraph. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="min-h-screen bg-slate-950 text-white">

      {/* Header */}

      <header className="border-b border-white/10">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600">
              <Network size={22} />
            </div>

            <div>
              <h1 className="text-lg font-semibold">
                SkillGraph
              </h1>

              <p className="text-xs text-slate-400">
                Job & technology relationship explorer
              </p>
            </div>

          </div>

          <div className="hidden items-center gap-6 text-sm text-slate-400 md:flex">
            <span>Explore</span>
            <span>How it works</span>
          </div>

        </div>
      </header>


      {/* Hero */}

      <section className="mx-auto max-w-7xl px-6 pb-16 pt-20">

        <div className="max-w-3xl">

          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-sm text-blue-300">
            <Sparkles size={15} />
            Powered by graph relationships
          </div>

          <h2 className="text-4xl font-bold tracking-tight md:text-6xl">
            Discover where your
            <span className="text-blue-400"> skills </span>
            can take you.
          </h2>

          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-400">
            Explore connections between skills, jobs, companies,
            technologies and industries using a graph-powered
            job discovery experience.
          </p>


          {/* Search */}

          <div className="mt-10 flex max-w-2xl flex-col gap-3 sm:flex-row">

            <div className="relative flex-1">

              <Search
                size={20}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
              />

              <input
                value={skill}
                onChange={(event) =>
                  setSkill(event.target.value)
                }
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    exploreSkill();
                  }
                }}
                placeholder="Search a skill..."
                className="w-full rounded-xl border border-white/10 bg-white/5 py-4 pl-12 pr-4 outline-none transition focus:border-blue-500"
              />

            </div>

            <button
              onClick={() => exploreSkill()}
              disabled={loading}
              className="rounded-xl bg-blue-600 px-7 py-4 font-medium transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Exploring..." : "Explore"}
            </button>

          </div>


          {/* Popular skills */}

          <div className="mt-5 flex flex-wrap gap-2">

            <span className="mr-1 py-2 text-sm text-slate-500">
              Popular:
            </span>

            {popularSkills.map((item) => (
              <button
                key={item}
                onClick={() => {
                  setSkill(item);
                  exploreSkill(item);
                }}
                className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-sm text-slate-300 transition hover:border-blue-500/50 hover:text-blue-300"
              >
                {item}
              </button>
            ))}

          </div>

        </div>

      </section>


      {/* Results */}

      <section className="mx-auto max-w-7xl px-6 pb-20">

        {error && (
          <div className="mb-8 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-red-300">
            {error}
          </div>
        )}


        <div className="mb-8">

          <p className="text-sm text-slate-500">
            Exploring
          </p>

          <h3 className="mt-1 text-3xl font-semibold">
            {searchedSkill}
          </h3>

        </div>


        <div className="grid gap-6 lg:grid-cols-3">

          {/* Jobs */}

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">

            <div className="mb-6 flex items-center gap-3">

              <div className="rounded-lg bg-blue-500/10 p-2 text-blue-400">
                <BriefcaseBusiness size={20} />
              </div>

              <div>
                <h4 className="font-semibold">
                  Matching jobs
                </h4>

                <p className="text-sm text-slate-500">
                  Jobs requiring this skill
                </p>
              </div>

            </div>


            <div className="space-y-3">

              {jobs.length === 0 && !loading && (
                <p className="text-sm text-slate-500">
                  Search for a skill to discover jobs.
                </p>
              )}

              {jobs.map((job) => (
                <div
                  key={job.job_id}
                  className="rounded-xl border border-white/5 bg-white/[0.03] p-4"
                >

                  <p className="font-medium">
                    {job.job_title}
                  </p>

                  <p className="mt-1 text-sm text-slate-400">
                    {job.company}
                  </p>

                </div>
              ))}

            </div>

          </div>


          {/* Related skills */}

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">

            <div className="mb-6">

              <h4 className="font-semibold">
                Related skills
              </h4>

              <p className="mt-1 text-sm text-slate-500">
                Skills connected in the graph
              </p>

            </div>


            <div className="flex flex-wrap gap-2">

              {relatedSkills.length === 0 && !loading && (
                <p className="text-sm text-slate-500">
                  No related skills found.
                </p>
              )}

              {relatedSkills.map((item) => (
                <span
                  key={item.skill}
                  className="rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-2 text-sm text-blue-300"
                >
                  {item.skill}
                </span>
              ))}

            </div>

          </div>


          {/* Companies */}

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">

            <div className="mb-6 flex items-center gap-3">

              <div className="rounded-lg bg-emerald-500/10 p-2 text-emerald-400">
                <Building2 size={20} />
              </div>

              <div>
                <h4 className="font-semibold">
                  Companies
                </h4>

                <p className="text-sm text-slate-500">
                  Connected employers
                </p>
              </div>

            </div>


            <div className="space-y-3">

              {companies.length === 0 && !loading && (
                <p className="text-sm text-slate-500">
                  No companies found.
                </p>
              )}

              {companies.map((item, index) => (
                <div
                  key={`${item.company}-${item.job}-${index}`}
                  className="flex items-center justify-between rounded-xl border border-white/5 bg-white/[0.03] p-4"
                >

                  <div>
                    <p className="font-medium">
                      {item.company}
                    </p>

                    <p className="mt-1 text-sm text-slate-400">
                      {item.industry}
                    </p>
                  </div>

                  <ArrowRight
                    size={16}
                    className="text-slate-600"
                  />

                </div>
              ))}

            </div>

          </div>

        </div>

      </section>

    </main>
  );
}