import csv
import os
import statistics
import sys
import time


# Allow the benchmark script to import the backend app package.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

sys.path.insert(0, BACKEND_DIR)


from app.database import driver, verify_connection
from app.queries import (
    get_jobs_by_skill,
    get_jobs_by_skill_and_location,
    get_skill_company_connections,
    get_related_skills,
    search_jobs,
)


WARMUP_ITERATIONS = 5
MEASURED_ITERATIONS = 30


QUERIES = {
    "Q1": {
        "name": "Jobs requiring Java",
        "function": lambda: get_jobs_by_skill("Java"),
    },
    "Q2": {
        "name": "Java jobs in Hyderabad",
        "function": lambda: get_jobs_by_skill_and_location(
            "Java",
            "Hyderabad",
        ),
    },
    "Q3": {
        "name": "Java -> Job -> Company -> Industry",
        "function": lambda: get_skill_company_connections("Java"),
    },
    "Q4": {
        "name": "Skills related to Java",
        "function": lambda: get_related_skills("Java"),
    },
    "Q5": {
        "name": "Java + Spring Boot",
        "function": lambda: search_jobs(
            skill_name="Java",
            technology="Spring Boot",
        ),
    },
}


def measure_query(query_function):
    """
    Execute a query repeatedly and return latency measurements in milliseconds.
    """

    # Warm-up
    for _ in range(WARMUP_ITERATIONS):
        query_function()

    measurements = []

    for _ in range(MEASURED_ITERATIONS):
        start = time.perf_counter()

        query_function()

        end = time.perf_counter()

        latency_ms = (end - start) * 1000
        measurements.append(latency_ms)

    return measurements


def benchmark():
    print("=" * 60)
    print("SkillGraph - CognoDB Benchmark")
    print("=" * 60)

    print("\nChecking database connection...")

    verify_connection()

    print("SUCCESS: Connected to CognoDB")

    print(f"\nWarm-up iterations: {WARMUP_ITERATIONS}")
    print(f"Measured iterations: {MEASURED_ITERATIONS}")

    results = []

    for query_id, query_info in QUERIES.items():
        print(f"\nRunning {query_id}: {query_info['name']}")

        try:
            measurements = measure_query(
                query_info["function"]
            )

            result = {
                "query_id": query_id,
                "query": query_info["name"],
                "iterations": len(measurements),
                "min_ms": min(measurements),
                "max_ms": max(measurements),
                "average_ms": statistics.mean(measurements),
                "median_ms": statistics.median(measurements),
            }

            results.append(result)

            print(
                f"  Average: {result['average_ms']:.3f} ms"
            )
            print(
                f"  Median:  {result['median_ms']:.3f} ms"
            )
            print(
                f"  Min:     {result['min_ms']:.3f} ms"
            )
            print(
                f"  Max:     {result['max_ms']:.3f} ms"
            )

        except Exception as exc:
            print(f"  FAILED: {exc}")

    return results


def save_results(results):
    output_dir = os.path.join(
        PROJECT_ROOT,
        "benchmark",
        "results",
    )

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        "cognodb_results.csv",
    )

    fieldnames = [
        "query_id",
        "query",
        "iterations",
        "min_ms",
        "max_ms",
        "average_ms",
        "median_ms",
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for result in results:
            writer.writerow(
                {
                    **result,
                    "min_ms": f"{result['min_ms']:.3f}",
                    "max_ms": f"{result['max_ms']:.3f}",
                    "average_ms": f"{result['average_ms']:.3f}",
                    "median_ms": f"{result['median_ms']:.3f}",
                }
            )

    print("\nResults saved to:")
    print(output_file)


def main():
    try:
        results = benchmark()

        if not results:
            print("\nNo benchmark results were produced.")
            return

        save_results(results)

        print("\n" + "=" * 60)
        print("Benchmark completed successfully.")
        print("=" * 60)

    finally:
        driver.close()


if __name__ == "__main__":
    main()