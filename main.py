import pandas as pd
from pipeline.scheduler_model import train_model, predict_failures
from pipeline.scheduling_rules import apply_scheduling_rules
from pipeline.explanation_agent import generate_explanation

df = pd.read_csv("data/synthetic_asset_data.csv")
model = train_model(df)
df_preds = predict_failures(df, model)
df_sched = apply_scheduling_rules(df_preds)
df_sched["Explanation"] = df_sched.apply(generate_explanation, axis=1)
df_sched.to_csv("data/final_schedule.csv", index=False)
print("Final schedule saved to data/final_schedule.csv")