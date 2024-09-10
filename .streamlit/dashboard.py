import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

# Initialize connection
@st.cache_resource(hash_funcs={psycopg2.extensions.connection: id})
def init_connection():
    try:
        # Pass PostgreSQL credentials directly to psycopg2.connect
        return psycopg2.connect(
            dbname="telecom",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
    except Exception as e:
        st.error(f"Error connecting to PostgreSQL database: {e}")
        return None  # Return None if connection fails

conn = init_connection()

# Perform query
@st.cache_data(ttl=600)
def run_query(query):
    if conn is None:
        st.error("Failed to establish database connection.")
        return None  # Return None if connection is not established
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None

# Sidebar headers
st.sidebar.title('Analysis Sections')
analysis_sections = ['User Overview Analysis', 'User Engagement Analysis', 'User Experience Analysis', 'User Satisfaction Analysis']
selected_section = st.sidebar.selectbox("Select Analysis Section:", analysis_sections)

# User Overview Analysis
if selected_section == 'User Overview Analysis':
    st.header("User Overview Analysis")

    # Top handsets
    query_top_handsets = "SELECT \"Handset Type\", COUNT(*) AS \"Count\" FROM xdr_data GROUP BY \"Handset Type\" ORDER BY \"Count\" DESC LIMIT 10"
    top_handsets = run_query(query_top_handsets)

    if top_handsets is not None:
        top_handsets_df = pd.DataFrame(top_handsets, columns=['Handset Type', 'Count'])
        st.subheader("Top Handsets")
        st.bar_chart(top_handsets_df, x='Handset Type', y='Count')
    else:
        st.error("Failed to fetch top handsets data.")

    # Top handsets by manufacturers
    query_top_manufacturers = "SELECT \"Handset Manufacturer\", COUNT(*) AS \"Count\" FROM xdr_data GROUP BY \"Handset Manufacturer\" ORDER BY \"Count\" DESC LIMIT 10"
    top_manufacturers = run_query(query_top_manufacturers)

    if top_manufacturers is not None:
        top_manufacturers_df = pd.DataFrame(top_manufacturers, columns=['Handset Manufacturer', 'Count'])
        st.subheader("Top Handsets by Manufacturers")
        st.bar_chart(top_manufacturers_df, x='Handset Manufacturer', y='Count')
    else:
        st.error("Failed to fetch top handset manufacturers data.")

    # Users with the top number of sessions
    query_top_sessions = "SELECT \"MSISDN/Number\", COUNT(*) AS \"Session Count\" FROM xdr_data GROUP BY \"MSISDN/Number\" ORDER BY \"Session Count\" DESC LIMIT 10"
    top_sessions = run_query(query_top_sessions)

    if top_sessions is not None:
        top_sessions_df = pd.DataFrame(top_sessions, columns=['MSISDN/Number', 'Session Count'])
        st.subheader("Users with the Top Number of Sessions")
        st.table(top_sessions_df)
    else:
        st.error("Failed to fetch top sessions data.")

    # Top total duration of sessions
    query_top_duration = "SELECT \"MSISDN/Number\", SUM(\"Dur. (ms)\") AS \"Total Duration\" FROM xdr_data GROUP BY \"MSISDN/Number\" ORDER BY \"Total Duration\" DESC LIMIT 10"
    top_duration = run_query(query_top_duration)

    if top_duration is not None:
        top_duration_df = pd.DataFrame(top_duration, columns=['MSISDN/Number', 'Total Duration'])
        st.subheader("Users with the Top Total Duration of Sessions")
        st.table(top_duration_df)
    else:
        st.error("Failed to fetch top duration data.")

    # Top average duration of sessions
    query_top_avg_duration = "SELECT \"MSISDN/Number\", AVG(\"Dur. (ms)\") AS \"Average Duration\" FROM xdr_data GROUP BY \"MSISDN/Number\" ORDER BY \"Average Duration\" DESC LIMIT 10"
    top_avg_duration = run_query(query_top_avg_duration)

    if top_avg_duration is not None:
        top_avg_duration_df = pd.DataFrame(top_avg_duration, columns=['MSISDN/Number', 'Average Duration'])
        st.subheader("Users with the Top Average Duration of Sessions")
        st.table(top_avg_duration_df)
    else:
        st.error("Failed to fetch top average duration data.")

    # Users with the top total data used
    query_top_data = "SELECT \"MSISDN/Number\", SUM(\"Total DL (Bytes)\") + SUM(\"Total UL (Bytes)\") AS \"Total Data Used\" FROM xdr_data GROUP BY \"MSISDN/Number\" ORDER BY \"Total Data Used\" DESC LIMIT 10"
    top_data = run_query(query_top_data)

    if top_data is not None:
        top_data_df = pd.DataFrame(top_data, columns=['MSISDN/Number','Total Data Used'])
        st.subheader("Users with the Top Total Data Used")
        st.table(top_data_df)
    else:
        st.error("Failed to fetch top data usage data.")

# User Engagement Analysis
elif selected_section == 'User Engagement Analysis':
    st.header("User Engagement Analysis")

    engagement_metrics = ['Number of Sessions', 'Total Duration', 'Total Data Volume']
    selected_engagement_metric = st.selectbox("Select an engagement metric:", engagement_metrics)

    if selected_engagement_metric == 'Number of Sessions':
        query_engagement = "SELECT \"MSISDN/Number\", COUNT(*) AS \"Session Count\" FROM xdr_data GROUP BY \"MSISDN/Number\" ORDER BY \"Session Count\" DESC LIMIT 10"
    elif selected_engagement_metric == 'Total Duration':
        query_engagement = "SELECT \"MSISDN/Number\", SUM(\"Dur. (ms)\") AS \"Total Duration\" FROM xdr_data GROUP BY \"MSISDN/Number\" ORDER BY \"Total Duration\" DESC LIMIT 10"
    elif selected_engagement_metric == 'Total Data Volume':
        query_engagement = "SELECT \"MSISDN/Number\", SUM(\"Total DL (Bytes)\") + SUM(\"Total UL (Bytes)\") AS \"Total Data Volume\" FROM xdr_data GROUP BY \"MSISDN/Number\" ORDER BY \"Total Data Volume\" DESC LIMIT 10"
    else:
        st.error("Invalid engagement metric selected.")

    engagement_data = run_query(query_engagement)

    if engagement_data is not None:
        engagement_df = pd.DataFrame(engagement_data, columns=['MSISDN/Number', selected_engagement_metric])
        st.subheader(f"Top 10 Users by {selected_engagement_metric}")
        st.table(engagement_df)
    else:
        st.error("Failed to fetch engagement data.")

# User Experience Analysis
elif selected_section == 'User Experience Analysis':
    st.header("User Experience Analysis")

    experience_metrics = ['Avg RTT DL', 'Avg RTT UL', 'Avg Bearer TP DL', 'Avg Bearer TP UL']
    selected_experience_metric = st.selectbox("Select an experience metric:", experience_metrics)

    if selected_experience_metric == 'Avg RTT DL':
        query_experience = "SELECT \"MSISDN/Number\", \"Avg RTT DL (ms)\" AS \"Average RTT DL\" FROM xdr_data ORDER BY \"Average RTT DL\" DESC LIMIT 10"
    elif selected_experience_metric == 'Avg RTT UL':
        query_experience = "SELECT \"MSISDN/Number\", \"Avg RTT UL (ms)\" AS \"Average RTT UL\" FROM xdr_data ORDER BY \"Average RTT UL\" DESC LIMIT 10"
    elif selected_experience_metric == 'Avg Bearer TP DL':
        query_experience = "SELECT \"MSISDN/Number\", \"Avg Bearer TP DL (kbps)\" AS \"Average Bearer TP DL\" FROM xdr_data ORDER BY \"Average Bearer TP DL\" DESC LIMIT 10"
    elif selected_experience_metric == 'Avg Bearer TP UL':
        query_experience = "SELECT \"MSISDN/Number\", \"Avg Bearer TP UL (kbps)\" AS \"Average Bearer TP UL\" FROM xdr_data ORDER BY \"Average Bearer TP UL\" DESC LIMIT 10"
    else:
        st.error("Invalid experience metric selected.")

    experience_data = run_query(query_experience)

    if experience_data is not None:
        experience_df = pd.DataFrame(experience_data, columns=['MSISDN/Number', selected_experience_metric])
        st.subheader(f"Top 10 Users by {selected_experience_metric}")
        st.table(experience_df)
    else:
        st.error("Failed to fetch experience data.")

# User Satisfaction Analysis
elif selected_section == 'User Satisfaction Analysis':
    st.header("User Satisfaction Analysis")

    satisfaction_metrics = ['Engagement Score', 'Experience Score']
    selected_satisfaction_metric = st.selectbox("Select a satisfaction metric:", satisfaction_metrics)

    if selected_satisfaction_metric == 'Engagement Score':
        query_satisfaction = "SELECT \"MSISDN/Number\", COUNT(*) AS \"Engagement Score\" FROM xdr_data GROUP BY \"MSISDN/Number\" ORDER BY \"Engagement Score\" DESC LIMIT 10"
    elif selected_satisfaction_metric == 'Experience Score':
        query_satisfaction = "SELECT \"MSISDN/Number\", \"Avg RTT DL (ms)\" + \"Avg RTT UL (ms)\" + \"Avg Bearer TP DL (kbps)\" + \"Avg Bearer TP UL (kbps)\" AS \"Experience Score\" FROM xdr_data ORDER BY \"Experience Score\" DESC LIMIT 10"
    else:
        st.error("Invalid satisfaction metric selected.")

    satisfaction_data = run_query(query_satisfaction)

    if satisfaction_data is not None:
        satisfaction_df = pd.DataFrame(satisfaction_data, columns=['MSISDN/Number', selected_satisfaction_metric])
        st.subheader(f"Top 10 Users by {selected_satisfaction_metric}")
        st.table(satisfaction_df)
    else:
        st.error("Failed to fetch satisfaction data.")