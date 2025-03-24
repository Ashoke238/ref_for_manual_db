import os
import time
import requests

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

# Load run ID from file
with open("run_id.txt", "r") as f:
    run_id = f.read().strip()

print(f"⏳ Waiting for Databricks job run to complete (run_id={run_id})...")

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json"
}

url = f"{DATABRICKS_HOST}/api/2.1/jobs/runs/get?run_id={run_id}"

# Poll every 15 seconds
while True:
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    run_data = resp.json()

    life_cycle = run_data["state"]["life_cycle_state"]
    result_state = run_data["state"].get("result_state", "N/A")
    print(f"🔄 Current status: {life_cycle}, Result: {result_state}")

    if life_cycle in ["TERMINATED", "SKIPPED", "INTERNAL_ERROR"]:
        if result_state == "SUCCESS":
            print("✅ Job completed successfully.")
            break
        else:
            print(f"❌ Job failed with result: {result_state}")
            exit(1)

    time.sleep(15)
