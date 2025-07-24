from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import sys
import os

# ✅ Add pipeline folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pipeline"))

# ✅ Import modules from pipeline folder directly (no "pipeline." prefix)
from scheduler_model import train_model, predict_failures
from scheduling_rules import apply_scheduling_rules
from explanation_agent import generate_explanation

# ✅ This is the function that will be called in the DAG
def run_pipeline():
    df = pd.read_csv("/opt/airflow/data/synthetic_asset_data.csv")
    model = train_model(df)
    df_preds = predict_failures(df, model)
    df_sched = apply_scheduling_rules(df_preds)
    df_sched["Explanation"] = df_sched.apply(generate_explanation, axis=1)
    df_sched.to_csv("/opt/airflow/data/final_schedule.csv", index=False)
    print("✅ Smart Scheduler pipeline executed.")

# ✅ DAG Configuration
default_args = {
    'start_date': datetime(2025, 7, 20),
}

with DAG(
    dag_id="asset_scheduler_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    tags=["smart-scheduler"]
) as dag:

    task = PythonOperator(
        task_id="run_smart_scheduler_pipeline",
        python_callable=run_pipeline,
    )