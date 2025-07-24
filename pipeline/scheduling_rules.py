def apply_scheduling_rules(df):
    def assign_priority(prob):
        if prob > 0.85:
            return "Urgent"
        elif prob > 0.7:
            return "Medium"
        else:
            return "Low"

    df["Priority"] = df["Failure_Prob"].apply(assign_priority)
    return df