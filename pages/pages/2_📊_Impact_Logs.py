import os
import streamlit as st
import snowflake.connector
import pandas as pd

st.markdown('<p class="main-header">📊 Cloud Impact & Telemetry Logs</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Real-time engagement telemetry captured safely through Snowflake data warehouses.</p>', unsafe_allow_html=True)

st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.write("Fetching live audit telemetry records from the `generosity_logs` table...")

try:
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
    df = pd.read_sql("SELECT * FROM generosity_logs ORDER BY timestamp DESC LIMIT 50", conn)
    conn.close()
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No logs recorded yet. Submit a match on the Matchmaker page to populate this table!")
except Exception as e:
    st.warning(f"Could not connect to Snowflake to render the live table in preview: {e}")
    st.info("You can execute this query directly in your Snowflake worksheet:\n`SELECT * FROM generosity_db.public.generosity_logs ORDER BY timestamp DESC;`")

st.markdown('</div>', unsafe_allow_html=True)
