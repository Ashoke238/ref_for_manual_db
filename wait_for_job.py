import os
import time
import requests

# Required environment variables
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
RUN_ID = os.getenv("RUN_ID")

if not RUN_ID:
    raise ValueError("❌ RUN_ID not found in environment variables.")

print(f"⏳ Waiting for Databricks job run to complete (run_id={RUN_ID})...")

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json"
}

url = f"{DATABRICKS_HOST}/api/2.1/jobs/runs/get?run_id={RUN_ID}"

# Poll every 15 seconds
while True:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    run_data = response.json()

    life_cycle = run_data["state"]["life_cycle_state"]
    result_state = run_data["state"].get("result_state", "N/A")

    print(f"🔄 Status: {life_cycle}, Result: {result_state}")

    if life_cycle in ["TERMINATED", "SKIPPED", "INTERNAL_ERROR"]:
        if result_state == "SUCCESS":
            print("✅ Job completed successfully.")
            break
        else:
            print(f"❌ Job failed with result: {result_state}")
            exit(1)

    time.sleep(15)
