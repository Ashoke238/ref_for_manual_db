import os
import json
import requests

host = os.environ.get("DATABRICKS_HOST")
token = os.environ.get("DATABRICKS_TOKEN")
job_id = os.environ.get("JOB_ID")
output_file = os.getenv("RUN_ID_FILE", "run_id.txt")  # default fallback

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "job_id": int(job_id)
}

response = requests.post(
    f"{host}/api/2.1/jobs/run-now",
    headers=headers,
    json=payload
)

if response.ok:
    run_id = response.json().get("run_id")
    if run_id:
        print(f"✅ RUN_ID ={run_id}")
        # Save to GitHub Actions env file
        with open(output_file, "w") as f:
            f.write(str(run_id))
    else:
        print("❌ run_id missing in response:", response.json())
        exit(1)
else:
    print("❌ Failed to trigger job:", response.text)
    exit(1)
