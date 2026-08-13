from app.database import driver


def get_jobs_by_skill(skill_name: str):
    query = """
    MATCH (s:Skill {name: $skill_name})
          <-[:REQUIRES_SKILL]-(j:Job)
          -[:POSTED_BY]->(c:Company)
    RETURN
        j.id AS job_id,
        j.title AS job_title,
        c.name AS company
    ORDER BY j.title
    """

    with driver.session() as session:
        result = session.run(
            query,
            skill_name=skill_name,
        )

        return [record.data() for record in result]


def get_jobs_by_skill_and_location(
    skill_name: str,
    city: str,
):
    query = """
    MATCH (s:Skill {name: $skill_name})
          <-[:REQUIRES_SKILL]-(j:Job)
          -[:LOCATED_IN]->(l:Location)
    WHERE l.city = $city
    RETURN
        j.id AS job_id,
        j.title AS job_title,
        l.city AS city
    ORDER BY j.title
    """

    with driver.session() as session:
        result = session.run(
            query,
            skill_name=skill_name,
            city=city,
        )

        return [record.data() for record in result]


def get_skill_company_connections(skill_name: str):
    query = """
    MATCH (s:Skill {name: $skill_name})
          <-[:REQUIRES_SKILL]-(j:Job)
          -[:POSTED_BY]->(c:Company)
          -[:OPERATES_IN]->(i:Industry)
    RETURN DISTINCT
        s.name AS skill,
        j.title AS job,
        c.name AS company,
        i.name AS industry
    ORDER BY company, job
    """

    with driver.session() as session:
        result = session.run(
            query,
            skill_name=skill_name,
        )

        return [record.data() for record in result]


def get_related_skills(skill_name: str):
    query = """
    MATCH (s:Skill {name: $skill_name})
          -[:RELATED_TO]->(related:Skill)
    RETURN
        related.name AS skill,
        related.category AS category
    ORDER BY related.name
    """

    with driver.session() as session:
        result = session.run(
            query,
            skill_name=skill_name,
        )

        return [record.data() for record in result]


def get_skill_to_company_graph(skill_name: str):
    query = """
    MATCH path =
        (s:Skill {name: $skill_name})
        <-[:REQUIRES_SKILL]-(j:Job)
        -[:POSTED_BY]->(c:Company)

    RETURN
        [node IN nodes(path) |
            {
                id: elementId(node),
                label: labels(node)[0],
                name: coalesce(node.name, node.title)
            }
        ] AS nodes,

        [relationship IN relationships(path) |
            {
                type: type(relationship)
            }
        ] AS relationships
    """

    with driver.session() as session:
        result = session.run(
            query,
            skill_name=skill_name,
        )

        nodes = {}
        relationships = []

        for record in result:
            for node in record["nodes"]:
                nodes[node["id"]] = node

            for relationship in record["relationships"]:
                relationships.append(relationship)

        return {
            "nodes": list(nodes.values()),
            "relationships": relationships,
        }