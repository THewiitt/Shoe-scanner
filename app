import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Shoe Scalp Dashboard", layout="wide")
st.title("👟 Live Shoe Scalp Opportunities")

# Function to pull data from your scanner's database
def get_data():
    conn = sqlite3.connect('shoe_listings.db')
    # Fetch the 10 most recent "deals" found by your worker.py
    df = pd.read_sql_query("SELECT * FROM listings ORDER BY timestamp DESC LIMIT 10", conn)
    conn.close()
    return df

# Create a 'Refresh' button
if st.button('Check for New Deals'):
    data = get_data()
    if not data.empty:
        for index, row in data.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                col1.subheader(row['title'])
                col1.write(f"Price: **£{row['price']}**")
                col2.link_button("View on Site", row['link'])
                st.divider()
    else:
        st.write("No deals found yet. Keep the scanner running!")
