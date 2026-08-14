from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.database import driver
from app.queries import (
    get_jobs_by_skill,
    get_jobs_by_skill_and_location,
    get_skill_company_connections,
    get_related_skills,
    get_skill_to_company_graph,
    get_job_details,
    get_job_graph,
)
from app.queries import search_jobs


app = FastAPI(
    title="SkillGraph API",
    description="Graph-powered job and technology relationship explorer",
    version="1.0.0",
)


# Allow the Next.js frontend to communicate with the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://skillgraph-frontend-mu.vercel.app",
        "https://skillgraph-frontend-b0sm436rj-ruchitha5.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "SkillGraph API is running",
        "status": "ok",
    }


@app.get("/health")
def health():
    try:
        driver.verify_connectivity()

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "unavailable",
            },
        )


@app.get("/api/jobs")
def jobs_by_skill(
    skill: str = Query(..., min_length=1),
):
    try:
        return {
            "skill": skill,
            "jobs": get_jobs_by_skill(skill),
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to query jobs from the database",
        )


@app.get("/api/jobs/location")
def jobs_by_skill_and_location(
    skill: str = Query(..., min_length=1),
    city: str = Query(..., min_length=1),
):
    try:
        return {
            "skill": skill,
            "city": city,
            "jobs": get_jobs_by_skill_and_location(
                skill,
                city,
            ),
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to query jobs from the database",
        )


@app.get("/api/skills/{skill_name}/companies")
def skill_companies(skill_name: str):
    try:
        return {
            "skill": skill_name,
            "connections": get_skill_company_connections(
                skill_name
            ),
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to query graph relationships",
        )


@app.get("/api/skills/{skill_name}/related")
def related_skills(skill_name: str):
    try:
        return {
            "skill": skill_name,
            "related_skills": get_related_skills(
                skill_name
            ),
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to query related skills",
        )


@app.get("/api/graph/{skill_name}")
def skill_graph(skill_name: str):
    try:
        return get_skill_to_company_graph(
            skill_name
        )

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to build graph",
        )

@app.get("/api/jobs/search")
def search_jobs_endpoint(
    skill: Optional[str] = Query(default=None),
    city: Optional[str] = Query(default=None),
    industry: Optional[str] = Query(default=None),
    technology: Optional[str] = Query(default=None),
):
    return search_jobs(
        skill_name=skill,
        city=city,
        industry=industry,
        technology=technology,
    )

@app.get("/api/jobs/{job_id}/graph")
def job_graph(job_id: str):
    result = get_job_graph(job_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return result

@app.get("/api/jobs/{job_id}")
def job_details(job_id: str):
    result = get_job_details(job_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return result


@app.on_event("shutdown")
def shutdown():
    driver.close()