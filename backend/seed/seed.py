from app.database import driver


def create_constraints():
    queries = [
        """
        CREATE CONSTRAINT job_id_unique IF NOT EXISTS
        FOR (j:Job)
        REQUIRE j.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT company_id_unique IF NOT EXISTS
        FOR (c:Company)
        REQUIRE c.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT skill_id_unique IF NOT EXISTS
        FOR (s:Skill)
        REQUIRE s.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT technology_id_unique IF NOT EXISTS
        FOR (t:Technology)
        REQUIRE t.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT location_id_unique IF NOT EXISTS
        FOR (l:Location)
        REQUIRE l.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT industry_id_unique IF NOT EXISTS
        FOR (i:Industry)
        REQUIRE i.id IS UNIQUE
        """,
    ]

    with driver.session() as session:
        for query in queries:
            session.run(query)


def clear_database():
    query = """
    MATCH (n)
    DETACH DELETE n
    """

    with driver.session() as session:
        session.run(query)


def create_data():
    companies = [
        {
            "id": "c1",
            "name": "TechNova",
            "industry": "FinTech",
        },
        {
            "id": "c2",
            "name": "CloudSphere",
            "industry": "Cloud Computing",
        },
        {
            "id": "c3",
            "name": "DataWorks",
            "industry": "Data & Analytics",
        },
        {
            "id": "c4",
            "name": "InnovaSoft",
            "industry": "Software",
        },
        {
            "id": "c5",
            "name": "PayFlow",
            "industry": "FinTech",
        },
    ]

    industries = [
        {"id": "i1", "name": "FinTech"},
        {"id": "i2", "name": "Cloud Computing"},
        {"id": "i3", "name": "Data & Analytics"},
        {"id": "i4", "name": "Software"},
    ]

    locations = [
        {"id": "l1", "city": "Hyderabad", "country": "India"},
        {"id": "l2", "city": "Bangalore", "country": "India"},
        {"id": "l3", "city": "Pune", "country": "India"},
        {"id": "l4", "city": "Chennai", "country": "India"},
        {"id": "l5", "city": "Mumbai", "country": "India"},
    ]

    skills = [
        {"id": "s1", "name": "Java", "category": "Programming"},
        {"id": "s2", "name": "Python", "category": "Programming"},
        {"id": "s3", "name": "JavaScript", "category": "Programming"},
        {"id": "s4", "name": "TypeScript", "category": "Programming"},
        {"id": "s5", "name": "SQL", "category": "Database"},
        {"id": "s6", "name": "REST APIs", "category": "Backend"},
        {"id": "s7", "name": "Spring Boot", "category": "Backend"},
        {"id": "s8", "name": "FastAPI", "category": "Backend"},
        {"id": "s9", "name": "React", "category": "Frontend"},
        {"id": "s10", "name": "Next.js", "category": "Frontend"},
        {"id": "s11", "name": "Containerization", "category": "DevOps"},
        {"id": "s12", "name": "Cloud Computing", "category": "Cloud"},
        {"id": "s13", "name": "Git", "category": "Tools"},
        {"id": "s14", "name": "Redis", "category": "Database"},
        {"id": "s15", "name": "MongoDB", "category": "Database"},
    ]

    technologies = [
        {"id": "t1", "name": "Spring Boot"},
        {"id": "t2", "name": "FastAPI"},
        {"id": "t3", "name": "React"},
        {"id": "t4", "name": "Next.js"},
        {"id": "t5", "name": "Docker"},
        {"id": "t6", "name": "AWS"},
        {"id": "t7", "name": "Redis"},
        {"id": "t8", "name": "PostgreSQL"},
        {"id": "t9", "name": "MongoDB"},
    ]

    jobs = [
        {
            "id": "j1",
            "title": "Backend Engineer",
            "company_id": "c1",
            "location_id": "l1",
            "skills": ["s1", "s5", "s6", "s7"],
            "technologies": ["t1", "t5", "t6"],
        },
        {
            "id": "j2",
            "title": "Full Stack Developer",
            "company_id": "c2",
            "location_id": "l2",
            "skills": ["s3", "s4", "s9", "s10", "s6"],
            "technologies": ["t3", "t4", "t5"],
        },
        {
            "id": "j3",
            "title": "Python Backend Developer",
            "company_id": "c3",
            "location_id": "l3",
            "skills": ["s2", "s5", "s6", "s8"],
            "technologies": ["t2", "t5", "t8"],
        },
        {
            "id": "j4",
            "title": "Java Developer",
            "company_id": "c4",
            "location_id": "l4",
            "skills": ["s1", "s5", "s7", "s13"],
            "technologies": ["t1", "t8"],
        },
        {
            "id": "j5",
            "title": "Cloud Backend Engineer",
            "company_id": "c5",
            "location_id": "l5",
            "skills": ["s1", "s6", "s11", "s12"],
            "technologies": ["t1", "t5", "t6"],
        },
        {
            "id": "j6",
            "title": "Frontend Engineer",
            "company_id": "c2",
            "location_id": "l2",
            "skills": ["s3", "s4", "s9", "s10"],
            "technologies": ["t3", "t4"],
        },
        {
            "id": "j7",
            "title": "Software Engineer",
            "company_id": "c1",
            "location_id": "l1",
            "skills": ["s1", "s5", "s11", "s13"],
            "technologies": ["t1", "t5"],
        },
        {
            "id": "j8",
            "title": "Data Platform Engineer",
            "company_id": "c3",
            "location_id": "l3",
            "skills": ["s2", "s5", "s11", "s12", "s14"],
            "technologies": ["t5", "t6", "t7"],
        },
    ]

    with driver.session() as session:

        session.run(
            """
            UNWIND $industries AS industry
            CREATE (i:Industry {
                id: industry.id,
                name: industry.name
            })
            """,
            industries=industries,
        )

        session.run(
            """
            UNWIND $locations AS location
            CREATE (l:Location {
                id: location.id,
                city: location.city,
                country: location.country
            })
            """,
            locations=locations,
        )

        session.run(
            """
            UNWIND $skills AS skill
            CREATE (s:Skill {
                id: skill.id,
                name: skill.name,
                category: skill.category
            })
            """,
            skills=skills,
        )

        session.run(
            """
            UNWIND $technologies AS technology
            CREATE (t:Technology {
                id: technology.id,
                name: technology.name
            })
            """,
            technologies=technologies,
        )

        session.run(
            """
            UNWIND $companies AS company
            MATCH (i:Industry {name: company.industry})
            CREATE (c:Company {
                id: company.id,
                name: company.name
            })
            CREATE (c)-[:OPERATES_IN]->(i)
            """,
            companies=companies,
        )

        session.run(
            """
            UNWIND $jobs AS job

            MATCH (c:Company {id: job.company_id})
            MATCH (l:Location {id: job.location_id})

            CREATE (j:Job {
                id: job.id,
                title: job.title
            })

            CREATE (j)-[:POSTED_BY]->(c)
            CREATE (j)-[:LOCATED_IN]->(l)
            """,
            jobs=jobs,
        )

        session.run(
            """
            UNWIND $jobs AS job
            MATCH (j:Job {id: job.id})

            UNWIND job.skills AS skill_id
            MATCH (s:Skill {id: skill_id})

            CREATE (j)-[:REQUIRES_SKILL]->(s)
            """,
            jobs=jobs,
        )

        session.run(
            """
            UNWIND $jobs AS job
            MATCH (j:Job {id: job.id})

            UNWIND job.technologies AS technology_id
            MATCH (t:Technology {id: technology_id})

            CREATE (j)-[:USES_TECHNOLOGY]->(t)
            """,
            jobs=jobs,
        )

        session.run(
            """
            MATCH (t:Technology)-[:REQUIRES_SKILL]->(s:Skill)
            RETURN count(t) AS count
            """
        )

        session.run(
            """
            MATCH (t:Technology {name: "Spring Boot"})
            MATCH (s:Skill {name: "Java"})
            CREATE (t)-[:REQUIRES_SKILL]->(s)
            """
        )

        session.run(
            """
            MATCH (t:Technology {name: "FastAPI"})
            MATCH (s:Skill {name: "Python"})
            CREATE (t)-[:REQUIRES_SKILL]->(s)
            """
        )

        session.run(
            """
            MATCH (t:Technology {name: "React"})
            MATCH (s:Skill {name: "JavaScript"})
            CREATE (t)-[:REQUIRES_SKILL]->(s)
            """
        )

        session.run(
            """
            MATCH (t:Technology {name: "Next.js"})
            MATCH (s:Skill {name: "TypeScript"})
            CREATE (t)-[:REQUIRES_SKILL]->(s)
            """
        )

        session.run(
            """
            MATCH (t:Technology {name: "Docker"})
            MATCH (s:Skill {name: "Containerization"})
            CREATE (t)-[:REQUIRES_SKILL]->(s)
            """
        )

        session.run(
            """
            MATCH (t:Technology {name: "AWS"})
            MATCH (s:Skill {name: "Cloud Computing"})
            CREATE (t)-[:REQUIRES_SKILL]->(s)
            """
        )

        session.run(
            """
            MATCH (s1:Skill {name: "Java"})
            MATCH (s2:Skill {name: "Spring Boot"})
            CREATE (s1)-[:RELATED_TO]->(s2)
            """

        )

        session.run(
            """
            MATCH (s1:Skill {name: "Java"})
            MATCH (s2:Skill {name: "SQL"})
            CREATE (s1)-[:RELATED_TO]->(s2)
            """
        )

        session.run(
            """
            MATCH (s1:Skill {name: "Python"})
            MATCH (s2:Skill {name: "FastAPI"})
            CREATE (s1)-[:RELATED_TO]->(s2)
            """
        )

        session.run(
            """
            MATCH (s1:Skill {name: "JavaScript"})
            MATCH (s2:Skill {name: "React"})
            CREATE (s1)-[:RELATED_TO]->(s2)
            """
        )

        session.run(
            """
            MATCH (s1:Skill {name: "TypeScript"})
            MATCH (s2:Skill {name: "Next.js"})
            CREATE (s1)-[:RELATED_TO]->(s2)
            """
        )


def verify_data():
    queries = {
        "nodes": """
            MATCH (n)
            RETURN count(n) AS count
        """,
        "relationships": """
            MATCH ()-[r]->()
            RETURN count(r) AS count
        """,
        "jobs": """
            MATCH (j:Job)
            RETURN count(j) AS count
        """,
        "companies": """
            MATCH (c:Company)
            RETURN count(c) AS count
        """,
        "skills": """
            MATCH (s:Skill)
            RETURN count(s) AS count
        """,
        "technologies": """
            MATCH (t:Technology)
            RETURN count(t) AS count
        """,
    }

    with driver.session() as session:
        print("\nDatabase verification:")

        for name, query in queries.items():
            result = session.run(query)
            record = result.single()
            print(f"{name}: {record['count']}")


def main():
    print("Creating constraints...")
    create_constraints()

    print("Clearing existing data...")
    clear_database()

    print("Creating graph data...")
    create_data()

    verify_data()

    driver.close()

    print("\nSeed completed successfully!")


if __name__ == "__main__":
    main()