import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")


if not COGNODB_URI:
    raise RuntimeError("COGNODB_URI is not configured")

if not COGNODB_USERNAME:
    raise RuntimeError("COGNODB_USERNAME is not configured")

if not COGNODB_PASSWORD:
    raise RuntimeError("COGNODB_PASSWORD is not configured")


driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD),
)


def verify_connection():
    driver.verify_connectivity()
    return True