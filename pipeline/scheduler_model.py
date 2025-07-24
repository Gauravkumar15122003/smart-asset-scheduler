import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def train_model(df):
    df = df.copy()
    le = LabelEncoder()
    df["Asset_ID_Code"] = le.fit_transform(df["Asset_ID"])
    features = ["Asset_ID_Code", "Usage_Hours", "Temperature", "Pressure"]
    X = df[features]
    y = df["Failure"]

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_failures(df, model):
    df = df.copy()
    le = LabelEncoder()
    df["Asset_ID_Code"] = le.fit_transform(df["Asset_ID"])
    features = ["Asset_ID_Code", "Usage_Hours", "Temperature", "Pressure"]
    df["Failure_Prob"] = model.predict_proba(df[features])[:, 1]
    df["Predicted_Failure"] = df["Failure_Prob"] > 0.5
    return df