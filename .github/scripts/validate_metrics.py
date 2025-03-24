import os
import mlflow
from mlflow.tracking import MlflowClient

# Set tracking URI for Databricks
mlflow.set_tracking_uri("databricks")

# Get environment variables
repo = os.getenv("GITHUB_REPOSITORY", "").split("/")[-1]
branch = os.getenv("GITHUB_REF_NAME", "dev")
user_email = os.getenv("USER_EMAIL")

# Determine environment
env = "prod" if branch == "main" else "dev"

# Build dynamic experiment name
experiment_name = f"/Users/{user_email}/{repo}_train_{env}"
print(f"🔍 Checking experiment: {experiment_name}")

# Query MLflow
client = MlflowClient()
experiment = client.get_experiment_by_name(experiment_name)
if not experiment:
    raise Exception(f"❌ Experiment '{experiment_name}' not found!")

runs = client.search_runs(experiment.experiment_id, order_by=["start_time DESC"], max_results=1)
accuracy = runs[0].data.metrics.get("accuracy", 0)
print(f"ℹ️ Last run accuracy: {accuracy}")

if accuracy <= 0:
    raise Exception("❌ Accuracy below threshold! Failing CI.")
else:
    print("✅ Accuracy is acceptable.")
