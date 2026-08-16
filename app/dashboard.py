import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Market Dashboard", layout="wide")
st.title("Job Market Dynamics Dashboard")
st.caption("Note: dataset covers Feb 7 - Mar 24, 2024 (~6 weeks). Panels show weekly trends; "
           "designed to be re-run as new monthly data is added.")

@st.cache_data
def load_data():
    df = pd.read_csv('../data/cleaned_jobs.csv')
    df['published_date'] = pd.to_datetime(df['published_date'])
    df['week'] = df['published_date'].dt.isocalendar().week
    df = df[df['week'].between(7, 12)]  # keep only the real data window
    return df

df = load_data()

# --- Panel 1: Posting volume over time ---
st.subheader("1. Posting Volume Over Time")
weekly_volume = df.groupby('week').size().reset_index(name='postings')
fig1 = px.line(weekly_volume, x='week', y='postings', markers=True,
               title='Total Job Postings Per Week')
st.plotly_chart(fig1, use_container_width=True)

# --- Panel 2: Hourly vs Fixed-price mix ---
st.subheader("2. Hourly vs Fixed-Price Mix Over Time")
mix = df.groupby(['week', 'is_hourly']).size().reset_index(name='count')
mix['type'] = mix['is_hourly'].map({True: 'Hourly', False: 'Fixed-price'})
fig2 = px.bar(mix, x='week', y='count', color='type', barmode='group',
              title='Hourly vs Fixed-Price Postings by Week')
st.plotly_chart(fig2, use_container_width=True)

# --- Panel 3: Average hourly rate trend ---
st.subheader("3. Average Hourly Rate Trend")
hourly_only = df[df['is_hourly'] == True].dropna(subset=['avg_hourly_rate'])
rate_trend = hourly_only.groupby('week')['avg_hourly_rate'].mean().reset_index()
fig3 = px.line(rate_trend, x='week', y='avg_hourly_rate', markers=True,
               title='Average (Mean) Hourly Rate by Week')
st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.caption("To refresh with new monthly data: replace cleaned_jobs.csv and re-run this dashboard.")