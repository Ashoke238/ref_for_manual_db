import os
from mlflow.tracking import MlflowClient

# Update with your actual experiment path or ID logic
experiment_name = "/Users/your_email/ref_for_manual_db_train_dev"

client = MlflowClient()
experiment = client.get_experiment_by_name(experiment_name)
runs = client.search_runs(experiment.experiment_id, order_by=["start_time DESC"], max_results=1)

accuracy = runs[0].data.metrics.get("accuracy", 0)
print(f"ℹ️ Last run accuracy: {accuracy}")

if accuracy < 0.85:
    raise Exception("❌ Accuracy below threshold! Failing CI.")
else:
    print("✅ Accuracy is acceptable.")
