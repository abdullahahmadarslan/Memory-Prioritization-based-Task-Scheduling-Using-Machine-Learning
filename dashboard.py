# Real-Time PMPD Scheduler Dashboard

import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Title
st.title("🖥 Real-Time PMPD Scheduler Dashboard")

# Refresh every 10 seconds automatically
st_autorefresh(interval=10 * 1000, limit=None, key="refresh")

# Read PM status CSV file
try:
    df = pd.read_csv("pm_status.csv", on_bad_lines='skip')

    # Optional: limit for smoother rendering (show top 50 machines only)
    df = df.drop_duplicates(subset="machine_id", keep="last")
    df_sampled = df.head(50)



    st.subheader("CPU Free Capacity per PM")
    st.bar_chart(df_sampled.set_index("machine_id")["cpu_free"])

    st.subheader("Memory Free Capacity per PM")
    st.bar_chart(df_sampled.set_index("machine_id")["mem_free"])

    # Show full PM resource table
    st.subheader("Current PM Resource Status")
    st.dataframe(df[["machine_id", "cpu_free", "mem_free"]])

except FileNotFoundError:
    st.write("PM Status file not yet generated... waiting for first scheduling run.")
