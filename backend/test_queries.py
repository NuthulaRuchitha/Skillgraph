from app.database import driver
from app.queries import (
    get_jobs_by_skill,
    get_jobs_by_skill_and_location,
    get_skill_company_connections,
    get_related_skills,
    get_skill_to_company_graph,
    search_jobs,
    get_job_details,
)


def print_section(title: str):
    print(f"\n=== {title} ===")


def main():
    print_section("Database Connection")

    driver.verify_connectivity()
    print("SUCCESS: Connected to CognoDB")

    print_section("Jobs requiring Java")
    print(get_jobs_by_skill("Java"))

    print_section("Java jobs in Hyderabad")
    print(
        get_jobs_by_skill_and_location(
            "Java",
            "Hyderabad",
        )
    )

    print_section("Java → Job → Company → Industry")
    print(
        get_skill_company_connections("Java")
    )

    print_section("Skills related to Java")
    print(get_related_skills("Java"))

    print_section("Java graph")
    graph = get_skill_to_company_graph("Java")

    print(
        f"Nodes: {len(graph['nodes'])}"
    )
    print(
        f"Relationships: {len(graph['relationships'])}"
    )

    print_section("All relationship types")

    with driver.session() as session:
        result = session.run(
            """
            MATCH ()-[r]->()
            RETURN DISTINCT type(r) AS relationship
            ORDER BY relationship
            """
        )

        for record in result:
            print(record["relationship"])

    print_section("Node labels")

    with driver.session() as session:
        result = session.run(
            """
            MATCH (n)
            RETURN DISTINCT labels(n) AS labels
            ORDER BY labels(n)
            """
        )

        for record in result:
            print(record["labels"])

    print_section("Search: Java + Hyderabad")
    print(
        search_jobs(
            skill_name="Java",
            city="Hyderabad",
        )
    )

    print_section("Search: Java + FinTech")
    print(
        search_jobs(
            skill_name="Java",
            industry="FinTech",
        )
    )

    print_section("Search: Java + Spring Boot")
    print(
        search_jobs(
            skill_name="Java",
            technology="Spring Boot",
        )
    )

    print_section("Job Details: j1")
    print(get_job_details("j1"))

    print("\nAll tests completed successfully.")


if __name__ == "__main__":
    try:
        main()
    finally:
        driver.close()