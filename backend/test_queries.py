from app.queries import (
    get_jobs_by_skill,
    get_jobs_by_skill_and_location,
    get_skill_company_connections,
    get_related_skills,
    get_skill_to_company_graph,
)
from app.database import driver


def main():
    print("\n=== Jobs requiring Java ===")
    print(get_jobs_by_skill("Java"))

    print("\n=== Java jobs in Hyderabad ===")
    print(get_jobs_by_skill_and_location("Java", "Hyderabad"))

    print("\n=== Java → Job → Company → Industry ===")
    print(get_skill_company_connections("Java"))

    print("\n=== Skills related to Java ===")
    print(get_related_skills("Java"))

    print("\n=== Java graph ===")
    print(get_skill_to_company_graph("Java"))

    driver.close()


if __name__ == "__main__":
    main()