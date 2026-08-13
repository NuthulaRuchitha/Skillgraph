from app.database import driver, verify_connection


try:
    verify_connection()
    print("SUCCESS: Connected to CognoDB")

finally:
    driver.close()