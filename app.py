import streamlit as st
from datetime import datetime
import pandas as pd
import mysql.connector
import plotly.express as px

# connecting with sql
mydb = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="3fXqCw6nxxduoS8.root",
    password="u2dctQHUVuOXcZhS",
    database="Cross_Market_Analysis"
)

# load data
@st.cache_data # data stored in cache to avoid reloading on every interaction, improving performance
def load_data():
  crypto = pd.read_sql("SELECT * FROM cryptocurrencies;", mydb)
  top_coins = pd.read_sql("SELECT * FROM top_coins;", mydb)
  oil = pd.read_sql("SELECT * FROM oil_prices;", mydb)
  stks = pd.read_sql("SELECT * FROM stks_prices;", mydb)
  return crypto, top_coins, oil, stks

crypto, top_coins, oil, stks = load_data()

top_coins.columns = top_coins.columns.str.strip().str.lower() # Clean column names for easier access
oil.columns = oil.columns.str.strip().str.lower()
stks.columns = stks.columns.str.strip().str.lower()

st.set_page_config(
    page_title="Cross Market Analysis",
    layout="wide"
) # Set wide layout for better visualization

st.title("📊💹 Cross Market Analysis Dashboard") 

st.sidebar.title("Navigation")
pages = {"Market Overview", "SQL Query Runner", "Charts & Trends"} # Define available pages in the sidebar
selection = st.sidebar.selectbox("Go to", list(pages))
    
if selection == "SQL Query Runner":
    st.subheader("🧠 SQL Query Runner")

    from utils.quries import queries # Import predefined SQL queries from a separate module

    category = st.selectbox("Select Category", list(queries.keys())) # Allow user to select a category of queries from the sidebar
    query_name = st.selectbox("Select Query", list(queries[category].keys())) 

    if st.button("Run Query"): # Execute the selected query when the button is clicked
        sql = queries[category][query_name]
        df = pd.read_sql(sql, mydb)
        st.dataframe(df)

elif selection == "Charts & Trends":
    st.subheader("📈 Charts & Trends")
    st.write("Explore price trends and correlations across markets.")

    from utils.charts import make_price_chart # Import the function to create price charts from a separate module

    # Ensure columns are clean once
    top_coins.columns = top_coins.columns.str.strip().str.lower()

    coins = top_coins["coin_id"].unique() # Get unique coin IDs for the dropdown selection
    selected_coin = st.selectbox("Select Coin", coins) # Dropdown to select a coin for charting

    selected_coin_df = top_coins[top_coins["coin_id"] == selected_coin]

    fig = make_price_chart(selected_coin_df, selected_coin)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.subheader("📊 Market Overview")
    start_date = st.date_input("Start Date", datetime(2025, 1, 1)) # Set default start date to Jan 1, 2025
    end_date = st.date_input("End Date", datetime(2026, 1, 1)) # Set default end date to Jan 1, 2026

    start_dt = pd.to_datetime(start_date) # Convert date to datetime
    end_dt = pd.to_datetime(end_date)
    top_coins["date"] = pd.to_datetime(top_coins["date"]) # Ensure date column is in datetime format for filtering
    oil["date"] = pd.to_datetime(oil["date"])
    stks["date"] = pd.to_datetime(stks["date"])
     
    btc_df = top_coins[
                (top_coins["coin_id"] == "bitcoin") &
                (top_coins["date"].between(start_dt, end_dt))
            ] # Filter data based on selected date range

    oil_filtered = oil[oil["date"].between(start_dt, end_dt)]

    nifty = stks[(stks["ticker"] == "^NSEI") & (stks["date"].between(start_dt, end_dt))]
    sp500 = stks[(stks["ticker"] == "^GSPC") & (stks["date"].between(start_dt, end_dt))]

    col1, col2, col3, col4 = st.columns(4) # Create 4 columns for metrics in streamlit
    col1.metric("Bitcoin Avg Price", round(btc_df["price"].mean(), 2))
    col2.metric("Oil Avg Price", round(oil_filtered["price"].mean(), 2))
    col3.metric("NIFTY Avg Close", round(nifty["close"].mean(), 2))
    col4.metric("S&P 500 Avg close", round(sp500["close"].mean(), 2))

    snapshot = (
    btc_df.merge(oil_filtered, on="date", how="inner", suffixes=("_btc", "_oil"))
    .merge(nifty[["date", "close"]], on="date", how="inner")
    .rename(columns={"close": "close_nifty"})
    .merge(sp500[["date", "close"]], on="date", how="inner")
    .rename(columns={"close": "close_sp500"})
    ) # Create a daily snapshot by merging the filtered dataframes on date and renaming columns for clarity

    st.subheader("📅 Daily Market Snapshot") 
    cols = [col for col in ["date","price_btc","price_oil","close_nifty","close_sp500"] if col in snapshot.columns] 
    # Ensure only existing columns are selected for display
    st.dataframe(snapshot[cols])
