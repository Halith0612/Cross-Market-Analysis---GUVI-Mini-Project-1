import plotly.express as px

def make_price_chart(selected_coin_df, coin_name):
    fig = px.line(
        selected_coin_df,
        x="date",
        y="price",
        title=f"{coin_name.upper()} Price Trend"
    )
    return fig