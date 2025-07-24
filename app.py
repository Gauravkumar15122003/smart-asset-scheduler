import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Set up Streamlit
st.set_page_config(page_title="Smart Asset Scheduler Dashboard", layout="wide")
st.title("🔧 Smart Asset Scheduler Dashboard")
st.markdown("Get full insights into asset sensor trends, predicted failures, priority risks, and more.")

# ===============================
# Load Data
# ===============================
@st.cache_data
def load_data():
    raw_data = pd.read_csv("synthetic_asset_data.csv")
    prediction_data = pd.read_csv("final_schedule.csv")
    raw_data['Date'] = pd.to_datetime(raw_data['Date'], errors='coerce')
    prediction_data['Date'] = pd.to_datetime(prediction_data['Date'], errors='coerce')
    return raw_data, prediction_data

raw_data, prediction_data = load_data()

# ===============================
# Sidebar filters
# ===============================
st.sidebar.header("🔍 Filter Options")
asset_options = sorted(prediction_data['Asset_ID'].unique())
selected_assets = st.sidebar.multiselect("Select Assets to View", options=asset_options, default=asset_options)

filtered_raw = raw_data[raw_data['Asset_ID'].isin(selected_assets)]
filtered_pred = prediction_data[prediction_data['Asset_ID'].isin(selected_assets)]

# ===============================
# Section 1: Sensor Trends
# ===============================
st.header("📘 Section 1: Asset Sensor Trends")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(filtered_raw, x='Date', y='Usage_Hours', color='Asset_ID', title='Usage Hours Over Time')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(filtered_raw, x='Date', y='Temperature', color='Asset_ID', title='Temperature Over Time')
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.line(filtered_raw, x='Date', y='Pressure', color='Asset_ID', title='Pressure Over Time')
st.plotly_chart(fig3, use_container_width=True)

# ===============================
# Section 2: Failure Analysis
# ===============================
st.header("📙 Section 2: Failure Insights")

failures = filtered_raw[filtered_raw['Failure'] == 1]
failure_count = failures['Asset_ID'].value_counts().reset_index()
failure_count.columns = ['Asset_ID', 'Failure Count']
fig_fail = px.bar(failure_count, x='Asset_ID', y='Failure Count', color='Asset_ID', title="Historical Failures per Asset")
st.plotly_chart(fig_fail, use_container_width=True)

# Failure Heatmap
st.subheader("🔴 Failure Heatmap")
heatmap_data = pd.crosstab(filtered_raw['Date'], filtered_raw['Asset_ID'], values=filtered_raw['Failure'], aggfunc='sum').fillna(0)
st.dataframe(heatmap_data, use_container_width=True)

fig_heat, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(heatmap_data.T, cmap="Reds", linewidths=0.1, linecolor='white', cbar=True, ax=ax)
st.pyplot(fig_heat)

# ===============================
# Section 3: Predictions
# ===============================
st.header("📗 Section 3: Prediction Analysis")

col3, col4 = st.columns(2)

with col3:
    fig_pred = px.histogram(filtered_pred, x='Predicted_Failure', color='Predicted_Failure',
                            title="Predicted Failure Distribution")
    st.plotly_chart(fig_pred, use_container_width=True)

with col4:
    fig_box = px.box(filtered_pred, x='Asset_ID', y='Failure_Prob', color='Asset_ID',
                     title="Predicted Failure Probability")
    st.plotly_chart(fig_box, use_container_width=True)

# Top Explanations
st.subheader("🧠 Top Explanations for Predicted Failures")
top_explanations = filtered_pred['Explanation'].value_counts().head(10).reset_index()
top_explanations.columns = ['Explanation', 'Count']
fig_exp = px.bar(top_explanations, x='Explanation', y='Count', title="Most Common Explanations", color='Count')
st.plotly_chart(fig_exp, use_container_width=True)

# ===============================
# Section 4: Priority View
# ===============================
st.header("🚨 Section 4: Asset Priority & Risk")

priority_data = filtered_pred.groupby('Priority')['Asset_ID'].count().reset_index()
priority_data.columns = ['Priority', 'Count']
fig_priority = px.pie(priority_data, names='Priority', values='Count', title='Assets by Priority Level')
st.plotly_chart(fig_priority, use_container_width=True)

# High Priority List
st.subheader("⚠️ High Risk Asset Schedule")
high_risk = filtered_pred[filtered_pred['Priority'] == 'High'][['Asset_ID', 'Date', 'Failure_Prob', 'Explanation']]
st.dataframe(high_risk.sort_values(by='Failure_Prob', ascending=False), use_container_width=True)

# ===============================
# Section 5: Compare Actual vs Predicted
# ===============================
st.header("📊 Section 5: Real vs Predicted Failure Comparison")

actual_vs_pred = filtered_pred.groupby('Asset_ID')[['Failure', 'Predicted_Failure']].sum().reset_index()
fig_comp = px.bar(actual_vs_pred, x='Asset_ID', y=['Failure', 'Predicted_Failure'],
                  barmode='group', title='Actual vs Predicted Failures')
st.plotly_chart(fig_comp, use_container_width=True)

# ===============================
# Section 6: Correlation Analysis
# ===============================
st.header("🧮 Section 6: Correlation Matrix (Raw Data)")

corr_data = filtered_raw[['Usage_Hours', 'Temperature', 'Pressure', 'Failure']].corr()
fig_corr, ax = plt.subplots()
sns.heatmap(corr_data, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig_corr)

# ===============================
# Section 7: Full Data Tables
# ===============================
st.header("📋 Section 7: Full Data")

with st.expander("📘 Raw Sensor Data"):
    st.dataframe(raw_data, use_container_width=True)

with st.expander("📙 Prediction Output Data"):
    st.dataframe(prediction_data, use_container_width=True)

# ===============================
# Footer
# ===============================
st.markdown("---")
st.caption("Built with ❤️ by Gaurav Kumar | Smart Asset Scheduler Dashboard | Streamlit + Plotly + Seaborn")