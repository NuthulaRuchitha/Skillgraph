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
    MATCH (s:Skill {name: $skill_name})

    OPTIONAL MATCH (s)<-[:REQUIRES_SKILL]-(j:Job)
    OPTIONAL MATCH (j)-[:POSTED_BY]->(c:Company)
    OPTIONAL MATCH (j)-[:LOCATED_IN]->(l:Location)
    OPTIONAL MATCH (j)-[:USES_TECHNOLOGY]->(t:Technology)
    OPTIONAL MATCH (s)-[:RELATED_TO]->(related:Skill)
    OPTIONAL MATCH (c)-[:OPERATES_IN]->(i:Industry)

    WITH
        collect(DISTINCT s) +
        collect(DISTINCT j) +
        collect(DISTINCT c) +
        collect(DISTINCT l) +
        collect(DISTINCT t) +
        collect(DISTINCT related) +
        collect(DISTINCT i) AS all_nodes,

        collect(DISTINCT
            CASE
                WHEN j IS NOT NULL
                THEN {
                    source: elementId(j),
                    target: elementId(s),
                    type: 'REQUIRES_SKILL'
                }
            END
        ) AS skill_relationships,

        collect(DISTINCT
            CASE
                WHEN j IS NOT NULL AND c IS NOT NULL
                THEN {
                    source: elementId(j),
                    target: elementId(c),
                    type: 'POSTED_BY'
                }
            END
        ) AS company_relationships,

        collect(DISTINCT
            CASE
                WHEN j IS NOT NULL AND l IS NOT NULL
                THEN {
                    source: elementId(j),
                    target: elementId(l),
                    type: 'LOCATED_IN'
                }
            END
        ) AS location_relationships,

        collect(DISTINCT
            CASE
                WHEN j IS NOT NULL AND t IS NOT NULL
                THEN {
                    source: elementId(j),
                    target: elementId(t),
                    type: 'USES_TECHNOLOGY'
                }
            END
        ) AS technology_relationships,

        collect(DISTINCT
            CASE
                WHEN related IS NOT NULL
                THEN {
                    source: elementId(s),
                    target: elementId(related),
                    type: 'RELATED_TO'
                }
            END
        ) AS related_skill_relationships,

        collect(DISTINCT
            CASE
                WHEN c IS NOT NULL AND i IS NOT NULL
                THEN {
                    source: elementId(c),
                    target: elementId(i),
                    type: 'OPERATES_IN'
                }
            END
        ) AS industry_relationships

    RETURN
        [
            node IN all_nodes
            WHERE node IS NOT NULL
            |
            {
                id: elementId(node),
                label: labels(node)[0],
                name: coalesce(
                    node.name,
                    node.title,
                    node.city
                )
            }
        ] AS nodes,

        skill_relationships +
        company_relationships +
        location_relationships +
        technology_relationships +
        related_skill_relationships +
        industry_relationships AS relationship_groups
    """

    with driver.session() as session:
        result = session.run(
            query,
            skill_name=skill_name,
        )

        record = result.single()

        if not record:
            return {
                "nodes": [],
                "relationships": [],
            }

        relationships = [
            relationship
            for relationship in record["relationship_groups"]
            if relationship is not None
        ]

        # Remove duplicate nodes by ID
        unique_nodes = {}

        for node in record["nodes"]:
            unique_nodes[node["id"]] = node

        return {
            "nodes": list(unique_nodes.values()),
            "relationships": relationships,
        }

def search_jobs(
    skill_name: str | None = None,
    city: str | None = None,
    industry: str | None = None,
    technology: str | None = None,
):
    query = """
    MATCH (j:Job)-[:POSTED_BY]->(c:Company)

    OPTIONAL MATCH (j)-[:REQUIRES_SKILL]->(skill:Skill)
    OPTIONAL MATCH (j)-[:LOCATED_IN]->(location:Location)
    OPTIONAL MATCH (c)-[:OPERATES_IN]->(industry_node:Industry)
    OPTIONAL MATCH (j)-[:USES_TECHNOLOGY]->(technology_node:Technology)

    WITH
        j,
        c,
        collect(DISTINCT skill.name) AS skills,
        collect(DISTINCT location.city) AS cities,
        collect(DISTINCT industry_node.name) AS industries,
        collect(DISTINCT technology_node.name) AS technologies

    WHERE
        (
            $skill_name IS NULL
            OR any(x IN skills WHERE toLower(x) = toLower($skill_name))
        )
        AND
        (
            $city IS NULL
            OR any(x IN cities WHERE toLower(x) = toLower($city))
        )
        AND
        (
            $industry IS NULL
            OR any(x IN industries WHERE toLower(x) = toLower($industry))
        )
        AND
        (
            $technology IS NULL
            OR any(x IN technologies WHERE toLower(x) = toLower($technology))
        )

    RETURN
        j.id AS job_id,
        j.title AS job_title,
        c.name AS company,
        CASE
            WHEN size(cities) > 0
            THEN cities[0]
            ELSE NULL
        END AS city,
        CASE
            WHEN size(industries) > 0
            THEN industries[0]
            ELSE NULL
        END AS industry

    ORDER BY j.title
    """
    with driver.session() as session:
        result = session.run(
            query,
            skill_name=skill_name,
            city=city,
            industry=industry,
            technology=technology,
        )

        return [record.data() for record in result]

def get_job_details(job_id: str):
    query = """
    MATCH (j:Job {id: $job_id})
    OPTIONAL MATCH (j)-[:POSTED_BY]->(c:Company)
    OPTIONAL MATCH (j)-[:LOCATED_IN]->(l:Location)
    OPTIONAL MATCH (j)-[:REQUIRES_SKILL]->(s:Skill)
    OPTIONAL MATCH (j)-[:USES_TECHNOLOGY]->(t:Technology)
    OPTIONAL MATCH (c)-[:OPERATES_IN]->(i:Industry)

    RETURN
        j.id AS job_id,
        j.title AS job_title,
        c.name AS company,
        i.name AS industry,
        l.city AS city,
        collect(DISTINCT s.name) AS skills,
        collect(DISTINCT t.name) AS technologies
    """

    with driver.session() as session:
        result = session.run(
            query,
            job_id=job_id,
        )

        record = result.single()

        if not record:
            return None

        return record.data()

def get_job_graph(job_id: str):
    query = """
    MATCH (j:Job {id: $job_id})

    OPTIONAL MATCH (j)-[r]->(n)

    WITH
        j,
        collect(DISTINCT r) AS job_relationships,
        collect(DISTINCT n) AS neighbors

    OPTIONAL MATCH (j)-[:POSTED_BY]->(c:Company)
        -[industry_rel:OPERATES_IN]->(i:Industry)

    WITH
        j,
        neighbors,
        job_relationships,
        collect(DISTINCT i) AS industries,
        collect(DISTINCT industry_rel) AS industry_relationships

    WITH
        [j] + neighbors + industries AS all_nodes,
        job_relationships + industry_relationships AS all_relationships

    UNWIND all_nodes AS node

    WITH
        collect(DISTINCT node) AS nodes,
        all_relationships

    UNWIND all_relationships AS relationship

    WITH
        nodes,
        collect(DISTINCT relationship) AS relationships

    RETURN
        [
            node IN nodes
            WHERE node IS NOT NULL |
            {
                id: elementId(node),
                label: labels(node)[0],
                name: coalesce(node.name, node.title, node.city)
            }
        ] AS nodes,

        [
            relationship IN relationships
            WHERE relationship IS NOT NULL |
            {
                source: elementId(startNode(relationship)),
                target: elementId(endNode(relationship)),
                type: type(relationship)
            }
        ] AS relationships
    """

    with driver.session() as session:
        result = session.run(
            query,
            job_id=job_id,
        )

        record = result.single()

        if not record:
            return None

        raw_nodes = record["nodes"]
        raw_relationships = record["relationships"]

        # --------------------------------------------------
        # Deduplicate nodes by name
        # --------------------------------------------------

        nodes_by_name = {}
        old_id_to_new_id = {}

        # Prefer Technology over Skill when both have
        # the same name, e.g. Spring Boot.
        priority = {
            "Job": 6,
            "Company": 5,
            "Industry": 4,
            "Location": 3,
            "Technology": 2,
            "Skill": 1,
        }

        for node in raw_nodes:
            name = node.get("name")

            if not name:
                continue

            name = name.strip()

            node_id = node["id"]
            label = node["label"]

            if name not in nodes_by_name:
                nodes_by_name[name] = node
                old_id_to_new_id[node_id] = node_id

            else:
                existing = nodes_by_name[name]

                existing_priority = priority.get(
                    existing["label"],
                    0
                )

                current_priority = priority.get(
                    label,
                    0
                )

                if current_priority > existing_priority:
                    old_existing_id = existing["id"]

                    nodes_by_name[name] = node

                    # Both old IDs now point to the new
                    # canonical node.
                    old_id_to_new_id[
                        old_existing_id
                    ] = node_id

                    old_id_to_new_id[node_id] = node_id

                else:
                    old_id_to_new_id[node_id] = existing["id"]

        # --------------------------------------------------
        # Rebuild relationships using deduplicated IDs
        # --------------------------------------------------

        relationships = []
        relationship_set = set()

        for relationship in raw_relationships:
            source = relationship["source"]
            target = relationship["target"]
            relationship_type = relationship["type"]

            source = old_id_to_new_id.get(source)
            target = old_id_to_new_id.get(target)

            if not source or not target:
                continue

            # Don't create self-links after deduplication.
            if source == target:
                continue

            key = (
                source,
                target,
                relationship_type,
            )

            if key in relationship_set:
                continue

            relationship_set.add(key)

            relationships.append(
                {
                    "source": source,
                    "target": target,
                    "type": relationship_type,
                }
            )

        return {
            "nodes": list(nodes_by_name.values()),
            "relationships": relationships,
        }