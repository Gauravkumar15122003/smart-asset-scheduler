def generate_explanation(row):
    if row["Priority"] == "Urgent":
        return f"{row['Asset_ID']} shows high risk of failure based on usage and temp. Immediate maintenance required."
    elif row["Priority"] == "Medium":
        return f"{row['Asset_ID']} is under moderate stress. Maintenance needed soon."
    else:
        return f"{row['Asset_ID']} is operating normally."