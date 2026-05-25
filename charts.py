import plotly.express as px

def make_price_chart(selected_coin_df, coins):
    fig = px.line(
        selected_coin_df,
        x="date",
        y="price",
        title=f"{coins.upper()} Price Trend"
    )
    return fig
