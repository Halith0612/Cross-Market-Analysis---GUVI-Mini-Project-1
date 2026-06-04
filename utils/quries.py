queries = {
    "Cryptocurrencies" : {"Find the top 5 cryptocurrencies by market cap":"""SELECT coin_name, MAX(market_cap) AS market_cap 
                            FROM cryptocurrencies WHERE market_cap IS NOT NULL GROUP BY coin_name ORDER BY market_cap DESC LIMIT 5;""",

                        "List all coins where circulating supply exceeds 90pct of total supply":"""SELECT * FROM cryptocurrencies 
                            WHERE total_supply IS NOT NULL AND total_supply > 0 AND circulating_supply >= 0.9 * total_supply 
                            AND circulating_supply IS NOT NULL;""",

                        "Get coins that are within 10pct of their all-time-high (ATH)": """ SELECT coin_id, current_price FROM cryptocurrencies 
                            WHERE current_price >= 0.9 * ath AND current_price IS NOT NULL ORDER BY current_price DESC;""",

                        "Find the average market cap rank of coins with volume above $1B" : """SELECT coin_name, AVG(market_cap_rank) FROM cryptocurrencies 
                            WHERE total_volume > 1000000000 AND total_volume IS NOT NULL GROUP BY coin_name;""",

                        "Get the most recently updated coin": """SELECT * FROM cryptocurrencies ORDER BY last_updated DESC LIMIT 1;"""},

    "Top Coins": {"Find the highest daily price of Bitcoin in the last 365 days" : """SELECT coin_id, MAX(price) AS highest_daily_price 
                    FROM top_coins WHERE coin_id = 'bitcoin' AND DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 365 DAY);""",

                "Calculate the average daily price of Ethereum in the past 1 year" : """SELECT coin_id, AVG(price) as Avg_price 
                    FROM top_coins WHERE coin_id = 'ethereum' AND DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 365 DAY);""",

                "Show the daily price trend of Bitcoin in January 2025. (or change the month and year according you your data)" : 
                    """SELECT coin_id, price AS daily_price, date 
                    FROM top_coins WHERE coin_id = 'bitcoin' AND Date BETWEEN '2025-01-01' AND '2026-02-28' ORDER BY Date;""",

                "Find the coin with the highest average price over 1 year" : """SELECT coin_id, AVG(price) AS avg_price FROM top_coins 
                    WHERE DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 365 DAY) GROUP BY coin_id ORDER BY avg_price DESC LIMIT 1;""",

                "Get the pct change in Bitcoin price between Jun 2025 and Jun 2026" : """SELECT coin_id,
                (
                    (MAX(CASE WHEN DATE(date) BETWEEN '2026-06-01' AND '2026-06-30' THEN price END) 
                    - 
                    MAX(CASE WHEN DATE(date) BETWEEN '2025-06-01' AND '2025-06-30' THEN price END)) 
                    / 
                    MAX(CASE WHEN DATE(date) BETWEEN '2025-06-01' AND '2025-06-30' THEN price END)
                ) * 100 AS percentage_change 
                FROM top_coins WHERE coin_id = 'bitcoin';"""},

    "Oil Prices": {"Find the highest oil price in the last 5 years" : """ SELECT MAX(price) AS highest_price FROM oil_prices 
                    WHERE date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR);""",

                "Get the average oil price per year" : """SELECT YEAR(date) AS year, AVG(price) AS avg_price FROM oil_prices GROUP BY YEAR(date) 
                    ORDER BY YEAR(date);""",

                "Show oil prices during COVID crash (March_April 2020)" : """SELECT date, price FROM oil_prices 
                    WHERE date BETWEEN '2020-03-01' AND '2020-04-30' ORDER BY date;""",

                "Find the lowest price of oil in the last 10 years" : """SELECT date, price FROM oil_prices 
                    WHERE price = (SELECT MIN(price) FROM oil_prices WHERE date >= DATE_SUB(CURDATE(), INTERVAL 10 YEAR));""",

                "Calculate the volatility of oil prices (max-min difference per year)" : """SELECT YEAR(date) AS year, MAX(price) AS highest_price, 
                    MIN(price) AS lowest_price, MAX(price) - MIN(price) AS volatility FROM oil_prices GROUP BY YEAR(date) ORDER BY YEAR(date);"""},

    "Stock Prices": {"Get all stock prices for a given ticker" : """ SELECT * FROM stks_prices WHERE Ticker IN ('^IXIC', '^NSEI', '^GSPC')
                        AND Open IS NOT NULL AND High IS NOT NULL AND Low IS NOT NULL AND Close IS NOT NULL AND Volume IS NOT NULL 
                        ORDER BY Date;""",
                        
                    "Find the highest closing price for NASDAQ (^IXIC)" : """SELECT Ticker, MAX(close) AS highest_closing_price 
                        FROM stks_prices WHERE ticker = '^IXIC';""",

                    "List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)": """SELECT Ticker, date, high - low AS price_difference 
                        FROM stks_prices WHERE ticker = '^GSPC' ORDER BY price_difference DESC LIMIT 5;""",

                    "Get monthly average closing price for each ticker" : """ SELECT Ticker, DATE_FORMAT(Date, '%Y-%m') AS month, 
                        AVG(Close) AS avg_closing_price FROM stks_prices WHERE Close IS NOT NULL AND Date IS NOT NULL 
                        GROUP BY Ticker, month ORDER BY Ticker, month;""",
                    
                    "Get average trading volume of NSEI in 2024" : """SELECT Ticker, AVG(Volume) AS avg_trading_volume FROM stks_prices
                    WHERE Ticker = '^NSEI' AND YEAR(Date) = 2024 GROUP BY Ticker;"""},

    "Joint Querries": {"Compare Bitcoin vs Oil average price in 2025" : """ SELECT DATE(c.date) AS date, c.price AS btc_close, o.price AS oil_close
                        FROM top_coins c LEFT JOIN oil_prices o ON DATE(c.date) = DATE(o.date) WHERE c.coin_id = 'bitcoin'
                        AND c.price IS NOT NULL AND o.price IS NOT NULL ORDER BY date;""",

                    "Check if Bitcoin moves with S&P 500 (correlation idea)" :"""SELECT DATE(t.date) AS date, t.price AS btc_close, s.Close AS stks_close
                        FROM top_coins t LEFT JOIN stks_prices s ON DATE(t.date) = DATE(s.Date) AND s.Ticker = '^GSPC'
                        WHERE t.coin_id = 'bitcoin' AND t.price IS NOT NULL AND s.Close IS NOT NULL ORDER BY date;""",

                    "Compare Ethereum and NASDAQ daily prices for 2025":"""SELECT DATE(t.date) AS date, t.price AS eth_close,
                        s.Close AS nasdaq_close FROM top_coins t JOIN stks_prices s ON DATE(t.date) = DATE(s.Date)
                        WHERE t.coin_id = 'ethereum' AND s.Ticker = '^IXIC' AND YEAR(t.date) = 2025 AND t.price IS NOT NULL
                        AND s.Close IS NOT NULL ORDER BY date;""", 

                    "Find days when oil price spiked and compare with Bitcoin price change" : """SELECT date(o.Date) AS date, o.Price AS oil_price,
                        t.price AS btc_price FROM oil_prices o JOIN top_coins t ON date(o.Date) = date(t.Date)
                        WHERE t.coin_id = 'bitcoin' AND t.price IS NOT NULL AND o.price IS NOT NULL ORDER BY date;""", 

                    "Compare top 3 coins daily price trend vs Nifty (^NSEI)" : """ SELECT date(c.Date) AS date, c.coin_id AS coins, c.price AS coin_prices,
                        s.Close AS nifty_close FROM top_coins c JOIN stks_prices s ON date(c.Date) = date(s.Date)
                        WHERE c.coin_id IN ('bitcoin', 'ethereum', 'binancecoin') AND s.Ticker = '^NSEI' AND c.price IS NOT NULL AND s.Close IS NOT NULL
                        ORDER BY date;""", 

                    "Compare stock prices (^GSPC) with crude oil prices on the same dates" : """SELECT
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
                        """, 

                    "Correlate Bitcoin closing price with crude oil closing price (same date)" : """SELECT
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
                        """,

                    "Compare NASDAQ (^IXIC) with Ethereum price trends" : """SELECT
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
                        """,

                    "Join top 3 crypto coins with stock indices for 2025" : """
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
                        """,

                    "Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison" : """SELECT
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
                        AND s.Close IS NOT NULL AND o.Price IS NOT NULL ORDER BY date;"""}
}