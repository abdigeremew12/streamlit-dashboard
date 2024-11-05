import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Compliance Risk Dashboard", layout="wide")

def load_data():
    data = pd.read_csv("compliance_risk_data.csv")  # Update CSV file name
    data['DATE'] = pd.to_datetime(data['DATE'])
    return data

df = load_data()

# Select relevant columns for compliance risk metrics
df1 = df[['DATE', 'RISK_SCORE', 'ISSUES_REPORTED', 'RESOLVED_ISSUES', 'PENDING_ISSUES']]

# Calculate row-wise cumulative sum for the selected metrics
df2 = df1.copy()
for column in ['RISK_SCORE', 'ISSUES_REPORTED', 'RESOLVED_ISSUES', 'PENDING_ISSUES']:
    df2[column] = df2[column].cumsum()

def format_with_commas(number):
    return f"{number:,}"

st.title("Compliance Risk Dashboard")

logo_icon = "images/streamlit-mark-color.png"
logo_image = "images/streamlit-logo-primary-colormark-lighttext.png"
st.image(logo_image, width=100)  # Adjusted image display

with st.sidebar:
    st.header("⚙️ Settings")
    start_date = st.date_input("Start date", df['DATE'].min())
    end_date = st.date_input("End date", df['DATE'].max())

    time_frame = st.selectbox(
        "Select time frame",
        ("Daily", "Cumulative"),
    )

# Display key metrics (Total)
st.subheader("Key Metrics")
st.caption("All-Time Statistics")

col = st.columns(4)
with col[0]:
    with st.container(border=True):
        st.metric("Current Risk Score", format_with_commas(df['RISK_SCORE'].iloc[-1]))
        if time_frame == 'Daily':
            df_risk_score = df1[["DATE", "RISK_SCORE"]].set_index(df1.columns[0])
            st.area_chart(df_risk_score, color='#29b5e8', height=150)

        if time_frame == 'Cumulative':
            df_risk_score = df2[["DATE", "RISK_SCORE"]].set_index(df2.columns[0])
            st.area_chart(df_risk_score, color='#29b5e8', height=150)

with col[1]:
    with st.container(border=True):
        st.metric("Total Issues Reported", format_with_commas(df['ISSUES_REPORTED'].sum()))

        if time_frame == 'Daily':
            df_issues_reported = df1[["DATE", "ISSUES_REPORTED"]].set_index(df1.columns[0])
            st.area_chart(df_issues_reported, color='#FF9F36', height=150)

        if time_frame == 'Cumulative':
            df_issues_reported = df2[["DATE", "ISSUES_REPORTED"]].set_index(df2.columns[0])
            st.area_chart(df_issues_reported, color='#FF9F36', height=150)

with col[2]:
    with st.container(border=True):
        st.metric("Total Resolved Issues", format_with_commas(df['RESOLVED_ISSUES'].sum()))

        if time_frame == 'Daily':
            df_resolved_issues = df1[["DATE", "RESOLVED_ISSUES"]].set_index(df1.columns[0])
            st.area_chart(df_resolved_issues, color='#D45B90', height=150)

        if time_frame == 'Cumulative':
            df_resolved_issues = df2[["DATE", "RESOLVED_ISSUES"]].set_index(df2.columns[0])
            st.area_chart(df_resolved_issues, color='#D45B90', height=150)

with col[3]:
    with st.container(border=True):
        st.metric("Total Pending Issues", format_with_commas(df['PENDING_ISSUES'].sum()))

        if time_frame == 'Daily':
            df_pending_issues = df1[["DATE", "PENDING_ISSUES"]].set_index(df1.columns[0])
            st.area_chart(df_pending_issues, color='#7D44CF', height=150)

        if time_frame == 'Cumulative':
            df_pending_issues = df2[["DATE", "PENDING_ISSUES"]].set_index(df2.columns[0])
            st.area_chart(df_pending_issues, color='#7D44CF', height=150)

# Display key metrics (Selected Duration)
st.caption("Selected Duration")

if time_frame == 'Daily':
    mask = (df1['DATE'].dt.date >= start_date) & (df1['DATE'].dt.date <= end_date)
    filtered_df = df1.loc[mask]
    
if time_frame == 'Cumulative':
    mask = (df2['DATE'].dt.date >= start_date) & (df2['DATE'].dt.date <= end_date)
    filtered_df = df2.loc[mask]

cols = st.columns(4)
with cols[0]:
    with st.container(border=True):
        st.metric("Risk Score", format_with_commas(filtered_df['RISK_SCORE'].sum()))

        df_risk_score_duration = filtered_df[["DATE", "RISK_SCORE"]].set_index(filtered_df.columns[0])
        st.area_chart(df_risk_score_duration, color='#29b5e8', height=150)

with cols[1]:
    with st.container(border=True):
        st.metric("Issues Reported", format_with_commas(filtered_df['ISSUES_REPORTED'].sum()))

        df_issues_duration = filtered_df[["DATE", "ISSUES_REPORTED"]].set_index(filtered_df.columns[0])
        st.area_chart(df_issues_duration, color='#FF9F36', height=150)

with cols[2]:
    with st.container(border=True):
        st.metric("Resolved Issues", format_with_commas(filtered_df['RESOLVED_ISSUES'].sum()))

        df_resolved_duration = filtered_df[["DATE", "RESOLVED_ISSUES"]].set_index(filtered_df.columns[0])
        st.area_chart(df_resolved_duration, color='#D45B90', height=150)

with cols[3]:
    with st.container(border=True):
        st.metric("Pending Issues", format_with_commas(filtered_df['PENDING_ISSUES'].sum()))

        df_pending_duration = filtered_df[["DATE", "PENDING_ISSUES"]].set_index(filtered_df.columns[0])
        st.area_chart(df_pending_duration, color='#7D44CF', height=150)

with st.expander("See DataFrame"):
    st.dataframe(df)

