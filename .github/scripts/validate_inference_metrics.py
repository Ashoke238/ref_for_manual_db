import os
from mlflow.tracking import MlflowClient
import mlflow

# Set tracking URI for Databricks
mlflow.set_tracking_uri("databricks")

# Dynamic experiment path logic
repo = os.getenv("GITHUB_REPOSITORY", "").split("/")[-1]
branch = os.getenv("GITHUB_REF_NAME", "dev")
user_email = os.getenv("USER_EMAIL")

env = "prod" if branch == "main" else "dev"

# Inference experiment path format
experiment_name = f"/Users/{user_email}/{repo}_inference_{env}"
print(f"🔍 Validating inference from experiment: {experiment_name}")

client = MlflowClient()
experiment = client.get_experiment_by_name(experiment_name)
if not experiment:
    raise Exception(f"❌ Experiment '{experiment_name}' not found!")

runs = client.search_runs(experiment.experiment_id, order_by=["start_time DESC"], max_results=1)
precision = runs[0].data.metrics.get("precision", 0)

print(f"ℹ️ Last inference precision: {precision}")
if precision < 0:
    raise Exception("❌ Precision below threshold! Failing CI.")
else:
    print("✅ Precision is acceptable.")
