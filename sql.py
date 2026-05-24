"""# **SQL connection Table Creation**"""

pip install mysql-connector-python

import mysql.connector

conn = mysql.connector.connect(
    host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user = "3fXqCw6nxxduoS8.root",
    password = "u2dctQHUVuOXcZhS",
    port = 4000
)

cma = conn.cursor()

cma.execute("DROP DATABASE IF EXISTS Cross_Market_Analysis")
conn.commit()

cma.execute("CREATE DATABASE Cross_Market_Analysis")
conn.commit()

cma.execute("show databases")
cma.fetchall()

cma.execute("use Cross_Market_Analysis")

# creating tables for cryptocurrencies

cma.execute("""CREATE TABLE cryptocurrencies
                 (id VARCHAR(50) PRIMARY KEY,
                 symbol VARCHAR(10),
                 name VARCHAR(100),
                 current_price DECIMAL(18, 6),
                 market_cap BIGINT,
                 market_cap_rank INT,
                 total_volume BIGINT,
                 circulating_supply DECIMAL(20, 6),
                 total_supply DECIMAL(20, 6),
                 ath DECIMAL(18, 6),
                 atl DECIMAL(18, 6),
                 date DATE
                 );

                 """)
conn.commit() # apply the changes to the sqlite3

#creating table for Crypto_prices

cma.execute("""CREATE TABLE top_coins
                 (coin_id VARCHAR(50),
                 date DATE,
                 price DECIMAL(18, 6)
                 );

                 """)
conn.commit()

#creating table for Oil_prices

cma.execute("""CREATE TABLE oil_prices
                 (date DATE PRIMARY KEY,
                 price_INR DECIMAL(18, 6)
                 );

                 """)
conn.commit()

#creating table for Stock_prices
cma.execute("""CREATE TABLE stk_prices
                 (date DATE,
                 open DECIMAL(18, 6),
                 high DECIMAL(18, 6),
                 low DECIMAL(18, 6),
                 close DECIMAL(18, 6),
                 volume BIGINT,
                 ticker VARCHAR(20)
                 );

                 """)
conn.commit()

cma.execute("show tables")
cma.fetchall()

"""# **Pushing data frames in to SQL and create sql engine**"""

pip install pandas sqlalchemy mysql-connector-python

from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://3fXqCw6nxxduoS8.root:u2dctQHUVuOXcZhS@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/Cross_Market_Analysis")

crypto_df.to_sql ("cryptocurrencies", con = engine, if_exists = "replace", index = False) # push crypto_df to sqlite

top_coins_df.to_sql ("top_coins", con = engine, if_exists = "replace", index = False)

oil_df.to_sql ("oil_prices", con = engine, if_exists = "replace", index = False)

stks_df.to_sql ("stks_prices", con = engine, if_exists = "replace", index = False)

"""# **Querries where mentioned in project file**

### **Cryptocurrencies**
"""

# show/read cryptocurrencies table
df = pd.read_sql("SELECT * FROM  cryptocurrencies;", engine)
df

# 1. Find the top 5 cryptocurrencies by market cap.
top_cryp = pd.read_sql (
    """SELECT coin_name, MAX(market_cap) AS market_cap FROM cryptocurrencies WHERE market_cap IS NOT NULL GROUP BY coin_name ORDER BY market_cap DESC LIMIT 5;""", engine)

top_cryp

# 2. List all coins where circulating supply exceeds 90% of total supply.

cir_sup = pd.read_sql (
    """SELECT * FROM cryptocurrencies WHERE total_supply IS NOT NULL AND total_supply > 0 AND circulating_supply >= 0.9 * total_supply AND circulating_supply IS NOT NULL;""", engine)

cir_sup

# 3. Get coins that are within 10% of their all-time-high (ATH).

ath = pd.read_sql(""" SELECT * FROM cryptocurrencies WHERE current_price >= 0.9 * ath
AND current_price IS NOT NULL ORDER BY current_price DESC;
""", engine)

ath

# 4. Find the average market cap rank of coins with volume above $1B.

df = pd.read_sql ("SELECT AVG(market_cap_rank) FROM cryptocurrencies WHERE total_volume > 1000000000 AND total_volume IS NOT NULL;", engine)

df

# 5. Get the most recently updated coin.

df = pd.read_sql ("SELECT * FROM cryptocurrencies ORDER BY last_updated DESC LIMIT 1;", engine)

df

"""### **Crypto_Prices (Daily Prices of Top Coins)**"""

df = pd.read_sql("SELECT * FROM  top_coins;", engine)
df

# 1. Find the highest daily price of Bitcoin in the last 365 days.

df = pd.read_sql(
    """SELECT coin_id, MAX(price) AS highest_daily_price FROM top_coins WHERE coin_id = 'bitcoin' AND DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 365 DAY);""", engine
)

df

# 2. Calculate the average daily price of Ethereum in the past 1 year.

df = pd.read_sql ("SELECT coin_id, AVG(price) as Avg_price FROM top_coins WHERE coin_id = 'ethereum' AND DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 365 DAY);", engine)

df

# 3. Show the daily price trend of Bitcoin in January 2025. (or change the month and year according you your data)

df = pd.read_sql(
    """SELECT coin_id, price AS daily_price, date FROM top_coins WHERE coin_id = 'bitcoin' AND Date BETWEEN '2025-01-01' AND '2026-02-28' ORDER BY Date;""", engine)

df

# 4. Find the coin with the highest average price over 1 year.

df = pd.read_sql (
    """SELECT coin_id, AVG(price) AS avg_price FROM top_coins WHERE DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 365 DAY)
    GROUP BY coin_id ORDER BY avg_price DESC LIMIT 1;""",
    engine)

df

# 5. Get the % change in Bitcoin’s price between Feb 2025 and Feb 2026.

df = pd.read_sql(
    """ SELECT
        (
            (MAX(CASE WHEN DATE(date) BETWEEN '2026-02-01' AND '2026-02-28' THEN price END)
                -
                MAX(CASE WHEN DATE(date) BETWEEN '2025-02-01' AND '2025-02-28' THEN price END)
            )
            /
            MAX(CASE WHEN DATE(date) BETWEEN '2025-02-01' AND '2025-02-28' THEN price END)
        ) * 100 AS percentage_change
    FROM top_coins WHERE coin_id = 'bitcoin';""",
    engine
)

df

"""### **Oil_Price**"""

df = pd.read_sql ("SELECT * FROM  oil_prices;", engine)
df

# 1. Find the highest oil price in the last 5 years.

df = pd.read_sql(""" SELECT MAX(price) AS highest_price FROM oil_prices WHERE date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR);
""", engine)

df

# 2. Get the average oil price per year.

df = pd.read_sql("""SELECT YEAR(date) AS year, AVG(price) AS avg_price
FROM oil_prices GROUP BY YEAR(date) ORDER BY YEAR(date);""", engine)

df

# 3. Show oil prices during COVID crash (March–April 2020).

df = pd.read_sql("""SELECT date, price FROM oil_prices WHERE date BETWEEN '2020-03-01' AND '2020-04-30' ORDER BY date;
""", engine)

df

# 4. Find the lowest price of oil in the last 10 years.

df = pd.read_sql("""SELECT date, price FROM oil_prices
WHERE price = (SELECT MIN(price) FROM oil_prices WHERE date >= DATE_SUB(CURDATE(), INTERVAL 10 YEAR));
""", engine)

df

# 5. Calculate the volatility of oil prices (max-min difference per year).

df = pd.read_sql("""SELECT YEAR(date) AS year, MAX(price) AS highest_price, MIN(price) AS lowest_price, MAX(price) - MIN(price) AS volatility
FROM oil_prices GROUP BY YEAR(date) ORDER BY YEAR(date);
""", engine)

df

"""### **Stock_Prices**"""

df = pd.read_sql("SELECT * FROM stks_prices;", engine)
df

# 1. Get all stock prices for a given ticker

df = pd.read_sql(""" SELECT * FROM stks_prices WHERE Ticker IN ('^IXIC', '^NSEI', '^GSPC')
AND Open IS NOT NULL AND High IS NOT NULL
AND Low IS NOT NULL AND Close IS NOT NULL
AND Volume IS NOT NULL ORDER BY Date;
""", engine)

df

# 2. Find the highest closing price for NASDAQ (^IXIC)

df = pd.read_sql ("SELECT MAX(close) AS highest_closing_price FROM stks_prices WHERE ticker = '^IXIC';", engine)

df

# 3. List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)

df = pd.read_sql ("""SELECT date, high - low AS price_difference FROM stks_prices
WHERE ticker = '^GSPC' ORDER BY price_difference DESC LIMIT 5
;""", engine)

df

# 4. Get monthly average closing price for each ticker

df = pd.read_sql("""
SELECT Ticker,
       DATE_FORMAT(Date, '%Y-%m') AS month,
       AVG(Close) AS avg_closing_price
FROM stks_prices
WHERE Close IS NOT NULL AND Date IS NOT NULL
GROUP BY Ticker, month ORDER BY Ticker, month;
""", engine)

df

"""### **Joint Querries**"""

# 1. Compare Bitcoin vs Oil average price in 2025.

df = pd.read_sql("""
SELECT
    DATE(c.date) AS date,
    c.price AS btc_close,
    o.price AS oil_close
FROM top_coins c
LEFT JOIN oil_prices o
    ON DATE(c.date) = DATE(o.date)
WHERE c.coin_id = 'bitcoin'
AND c.price IS NOT NULL
AND o.price IS NOT NULL
ORDER BY date;
""", engine)

df

# 2. Check if Bitcoin moves with S&P 500 (correlation idea).

df = pd.read_sql("""
SELECT
    DATE(t.date) AS date,
    t.price AS btc_close,
    s.Close AS stks_close
FROM top_coins t
LEFT JOIN stks_prices s
    ON DATE(t.date) = DATE(s.Date)
   AND s.Ticker = '^GSPC'
WHERE t.coin_id = 'bitcoin'
AND t.price IS NOT NULL
AND s.Close IS NOT NULL
ORDER BY date;
""", engine)

df

# 3. Compare Ethereum and NASDAQ daily prices for 2025.

df = pd.read_sql("""
SELECT
    DATE(t.date) AS date,
    t.price AS eth_close,
    s.Close AS nasdaq_close
FROM top_coins t
JOIN stks_prices s
    ON DATE(t.date) = DATE(s.Date)
WHERE t.coin_id = 'ethereum'
AND s.Ticker = '^IXIC'
AND YEAR(t.date) = 2025
AND t.price IS NOT NULL
AND s.Close IS NOT NULL
ORDER BY date;
""", engine)


df

# 4. Find days when oil price spiked and compare with Bitcoin price change.

df = pd.read_sql ("""SELECT date(o.Date) AS date,
    o.Price AS oil_price,
    t.price AS btc_price
FROM oil_prices o
JOIN top_coins t
    ON date(o.Date) = date(t.Date)
WHERE t.coin_id = 'bitcoin'
AND t.price IS NOT NULL
AND o.price IS NOT NULL
ORDER BY date;
""", engine)

df

# 5. Compare top 3 coins daily price trend vs Nifty (^NSEI).

df = pd.read_sql ("""
SELECT
    date(c.Date) AS date,
    c.coin_id AS coins,
    c.price AS coin_prices,
    s.Close AS nifty_close
FROM top_coins c
JOIN stks_prices s
    ON date(c.Date) = date(s.Date)
WHERE c.coin_id IN ('bitcoin', 'ethereum', 'binancecoin')
  AND s.Ticker = '^NSEI'
  AND c.price IS NOT NULL
  AND s.Close IS NOT NULL
ORDER BY date;
""", engine)

df

# 6. Compare stock prices (^GSPC) with crude oil prices on the same dates


df = pd.read_sql("""
SELECT
    date(s.Date) AS date,
    s.Close AS nifty_close,
    o.Price AS oil_price
FROM stks_prices s
JOIN oil_prices o
    ON date(s.Date) = date(o.Date)
WHERE s.Ticker = '^GSPC'
AND s.Close IS NOT NULL
AND o.Price IS NOT NULL
ORDER BY date;
""", engine)

df

# 7. Correlate Bitcoin closing price with crude oil closing price (same date)

df = pd.read_sql("""
SELECT
    date(t.Date) AS date,
    t.price AS btc_price,
    o.Price AS oil_price
FROM top_coins t
JOIN oil_prices o
    ON date(t.Date) = date(o.Date)
WHERE t.coin_id = 'bitcoin'
AND t.price IS NOT NULL
AND o.Price IS NOT NULL
ORDER BY date;
""", engine)

df

# 8. Compare NASDAQ (^IXIC) with Ethereum price trends

df = pd.read_sql("""
SELECT
    date(t.Date) AS date,
    t.price AS eth_price,
    s.Close AS ixic_close
FROM top_coins t
JOIN stks_prices s
    ON date(t.Date) = date(s.Date)
WHERE t.coin_id = 'ethereum'
  AND s.Ticker = '^IXIC'
  AND t.price IS NOT NULL
  AND s.Close IS NOT NULL
ORDER BY date;
""", engine)

df

# 9. Join top 3 crypto coins with stock indices for 2025
df = pd.read_sql("""
SELECT
    DATE(c.Date) AS date,
    c.coin_id AS crypto_coin,
    c.price AS crypto_price,
    s.Ticker AS stock_index,
    s.Close AS stock_close
FROM top_coins c
JOIN stks_prices s
    ON DATE(c.Date) = DATE(s.Date)
WHERE c.coin_id IN ('bitcoin', 'ethereum', 'binancecoin')
AND s.Ticker IN ('^GSPC', '^IXIC', '^NSEI')
AND YEAR(c.Date) = 2025
AND c.price IS NOT NULL
AND s.Close IS NOT NULL
ORDER BY date, crypto_coin;
""", engine)

df

# 10. Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison

df = pd.read_sql("""
SELECT
    date(t.Date) AS date,
    t.price AS btc_price,
    s.Close AS stk_close,
    o.Price AS oil_price
FROM top_coins t
JOIN stks_prices s
    ON date(t.Date) = date(s.Date)
JOIN oil_prices o
    ON date(t.Date) = date(o.Date)
WHERE t.coin_id = 'bitcoin'
  AND s.Ticker = '^GSPC'
  AND t.price IS NOT NULL
  AND s.Close IS NOT NULL
  AND o.Price IS NOT NULL
ORDER BY date;
""", engine)

df
