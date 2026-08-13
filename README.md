# SkillGraph

SkillGraph is a graph-powered job and technology relationship explorer built using **CognoDB**, **FastAPI**, and **Next.js**.

The application models relationships between jobs, skills, technologies, companies, industries, and locations in a graph database and exposes them through a REST API and interactive web interface.

## Features

- Search jobs by:
  - Skill
  - City
  - Industry
  - Technology
- View detailed job information
- Explore relationships between skills, jobs, companies, technologies, locations, and industries
- Interactive graph visualization
- Graph-based relationship queries using Cypher
- CognoDB connectivity and health check
- FastAPI REST endpoints
- Next.js frontend

## Architecture

```text
┌──────────────────────┐
│     Next.js UI       │
│                      │
│  Job Search          │
│  Job Details         │
│  Graph Explorer      │
└──────────┬───────────┘
           │ REST API
           ▼
┌──────────────────────┐
│      FastAPI         │
│                      │
│  Job Search APIs     │
│  Job Details API     │
│  Graph API           │
│  Health Check        │
└──────────┬───────────┘
           │ Cypher
           ▼
┌──────────────────────┐
│       CognoDB        │
│                      │
│ Job                  │
│ Skill                │
│ Technology           │
│ Company              │
│ Industry             │
│ Location             │
└──────────────────────┘
```

## Graph Model

### Node Types

The current graph contains these node labels:

- `Job`
- `Skill`
- `Technology`
- `Company`
- `Industry`
- `Location`

### Relationships

The graph currently uses:

| Relationship | Meaning |
|---|---|
| `REQUIRES_SKILL` | A job requires a skill |
| `USES_TECHNOLOGY` | A job uses a technology |
| `POSTED_BY` | A job is posted by a company |
| `LOCATED_IN` | A job is located in a location |
| `OPERATES_IN` | A company operates in an industry |
| `RELATED_TO` | A skill is related to another skill |

## Example Graph

For the `Java` skill, the graph can connect:

```text
Java
 ├── REQUIRES_SKILL ← Backend Engineer
 │                         ├── POSTED_BY → TechNova
 │                         ├── LOCATED_IN → Hyderabad
 │                         ├── USES_TECHNOLOGY → Spring Boot
 │                         ├── USES_TECHNOLOGY → Docker
 │                         └── USES_TECHNOLOGY → AWS
 │
 ├── REQUIRES_SKILL ← Java Developer
 │                         └── POSTED_BY → InnovaSoft
 │
 ├── REQUIRES_SKILL ← Cloud Backend Engineer
 │                         └── POSTED_BY → PayFlow
 │
 └── REQUIRES_SKILL ← Software Engineer
                           └── POSTED_BY → TechNova
```

## Example Queries

### Jobs requiring Java

```cypher
MATCH (s:Skill {name: "Java"})
      <-[:REQUIRES_SKILL]-(j:Job)
      -[:POSTED_BY]->(c:Company)
RETURN
    j.id AS job_id,
    j.title AS job_title,
    c.name AS company
ORDER BY j.title;
```

Example result:

```text
Backend Engineer       TechNova
Cloud Backend Engineer PayFlow
Java Developer         InnovaSoft
Software Engineer      TechNova
```

### Java jobs in Hyderabad

```cypher
MATCH (s:Skill {name: "Java"})
      <-[:REQUIRES_SKILL]-(j:Job)
      -[:LOCATED_IN]->(l:Location)
WHERE l.city = "Hyderabad"
RETURN
    j.id AS job_id,
    j.title AS job_title,
    l.city AS city
ORDER BY j.title;
```

Example result:

```text
Backend Engineer     Hyderabad
Software Engineer    Hyderabad
```

### Java → Job → Company → Industry

```cypher
MATCH (s:Skill {name: "Java"})
      <-[:REQUIRES_SKILL]-(j:Job)
      -[:POSTED_BY]->(c:Company)
      -[:OPERATES_IN]->(i:Industry)
RETURN DISTINCT
    s.name AS skill,
    j.title AS job,
    c.name AS company,
    i.name AS industry
ORDER BY company, job;
```

## API

Base URL:

```text
http://127.0.0.1:8000
```

### Health Check

```http
GET /health
```

### Jobs by Skill

```http
GET /api/jobs?skill=Java
```

### Jobs by Skill and Location

```http
GET /api/jobs/location?skill=Java&city=Hyderabad
```

### Job Search

Supports multiple optional filters:

```text
skill
city
industry
technology
```

Example:

```http
GET /api/jobs/search?skill=Java&city=Hyderabad
```

### Job Details

```http
GET /api/jobs/{job_id}
```

Example:

```http
GET /api/jobs/j1
```

Example response:

```json
{
  "job_id": "j1",
  "job_title": "Backend Engineer",
  "company": "TechNova",
  "industry": "FinTech",
  "city": "Hyderabad",
  "skills": [
    "Java",
    "SQL",
    "REST APIs",
    "Spring Boot"
  ],
  "technologies": [
    "Spring Boot",
    "Docker",
    "AWS"
  ]
}
```

### Skill Graph

```http
GET /api/graph/{skill_name}
```

Example:

```http
GET /api/graph/Java
```

### Related Skills

```http
GET /api/skills/{skill_name}/related
```

Example:

```http
GET /api/skills/Java/related
```

### Skill → Company Connections

```http
GET /api/skills/{skill_name}/companies
```

Example:

```http
GET /api/skills/Java/companies
```

## Running Locally

### Backend

Navigate to the backend:

```bash
cd backend
```

Create the virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the CognoDB connection using environment variables:

```text
COGNODB_URI=...
COGNODB_USERNAME=...
COGNODB_PASSWORD=...
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start Next.js:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

## Testing

Backend query tests can be run with:

```bash
cd backend
python test_queries.py
```

The current test suite verifies:

- CognoDB connectivity
- Jobs requiring Java
- Java jobs in Hyderabad
- Skill → Job → Company → Industry traversal
- Related skills
- Graph generation
- Relationship types
- Node labels
- Multi-filter job search
- Job details

Current test output confirms:

```text
=== Database Connection ===
SUCCESS: Connected to CognoDB

=== All relationship types ===
LOCATED_IN
OPERATES_IN
POSTED_BY
RELATED_TO
REQUIRES_SKILL
USES_TECHNOLOGY

=== Node labels ===
['Company']
['Industry']
['Job']
['Location']
['Skill']
['Technology']

=== Job Details: j1 ===
{
  'job_id': 'j1',
  'job_title': 'Backend Engineer',
  'company': 'TechNova',
  'industry': 'FinTech',
  'city': 'Hyderabad',
  'skills': [
    'Java',
    'SQL',
    'REST APIs',
    'Spring Boot'
  ],
  'technologies': [
    'Spring Boot',
    'Docker',
    'AWS'
  ]
}

All tests completed successfully.
```

## Tech Stack

### Backend

- Python
- FastAPI
- Neo4j Python Driver
- Cypher
- CognoDB

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- `react-force-graph-2d`

### Database

- CognoDB
- Graph-based data modeling
- Cypher queries

## Project Structure

```text
Skillgraph/
│
├── README.md
├── .gitignore
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── queries.py
│   │
│   ├── test_queries.py
│   └── requirements.txt
│
└── frontend/
    ├── app/
    │   ├── page.tsx
    │   └── ...
    │
    ├── components/
    │   ├── GraphExplorer.tsx
    │   └── JobSearch.tsx
    │
    ├── lib/
    │   └── api.ts
    │
    ├── package.json
    ├── package-lock.json
    └── ...
```

## Why a Graph Database?

Job data naturally contains many-to-many relationships.

A single job can:

- Require multiple skills
- Use multiple technologies
- Be posted by a company
- Be located in a city

A company can:

- Post multiple jobs
- Operate in an industry

A skill can:

- Be required by multiple jobs
- Be related to other skills

This creates a connected structure:

```text
Skill
  ↓
Job
  ↓
Company
  ↓
Industry
```

Graph queries make these relationships explicit and allow multi-hop traversal.

For example:

```text
Java
 ↓
Job
 ↓
Company
 ↓
Industry
```

can be queried directly using Cypher.

This makes the graph useful for relationship-oriented job discovery rather than only simple field-based filtering.

## Current Graph Statistics

The current Java graph exploration returns:

```text
Nodes: 19
Relationships: 27
```

Current node labels:

```text
Company
Industry
Job
Location
Skill
Technology
```

Current relationship types:

```text
LOCATED_IN
OPERATES_IN
POSTED_BY
RELATED_TO
REQUIRES_SKILL
USES_TECHNOLOGY
```

## Design Decisions

### Graph-Based Filtering

The backend uses Cypher queries to perform graph traversal and filtering instead of loading the entire graph into the application.

This keeps relationship logic close to the graph data model.

### Separate Search and Job Details

The search endpoint returns lightweight job information:

```text
job_id
job_title
company
city
industry
```

Detailed information is retrieved separately using:

```text
GET /api/jobs/{job_id}
```

This keeps search responses concise while allowing additional graph traversal when a user selects a job.

### Environment Variable Configuration

Database credentials are loaded through environment variables:

```text
COGNODB_URI
COGNODB_USERNAME
COGNODB_PASSWORD
```

Credentials are not hard-coded into the application.

## Error Handling

The FastAPI backend includes:

- Database health checks
- HTTP 503 responses when the graph database is unavailable
- HTTP 404 responses when a requested job does not exist
- Frontend loading states
- Frontend error states

The health endpoint verifies connectivity to CognoDB:

```http
GET /health
```

## Future Improvements

Potential future improvements include:

- Improved graph layout and visualization
- Pagination for larger job result sets
- More advanced multi-hop search
- Skill-gap analysis
- Job recommendations based on user skills
- Company exploration
- Industry exploration
- More comprehensive automated tests
- Performance benchmarking with larger datasets

## Project Status

The current implementation includes:

- [x] CognoDB connection
- [x] Graph data model
- [x] Cypher graph queries
- [x] Job search API
- [x] Job details API
- [x] Skill relationship API
- [x] Graph API
- [x] FastAPI backend
- [x] Next.js frontend
- [x] Job search interface
- [x] Job details interface
- [x] Interactive graph explorer
- [x] Backend query tests
- [x] Environment variable configuration
- [x] GitHub repository

## Repository

GitHub:

https://github.com/NuthulaRuchitha/Skillgraph