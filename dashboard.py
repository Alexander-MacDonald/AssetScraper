import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Load your CSV data
df = pd.read_csv("historical_data/RIVN/RIVN.csv", parse_dates=["Date"])
df.sort_values("Date", inplace=True)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Stock Price Viewer"

# Layout
app.layout = html.Div([
    html.H1("Stock Closing Price", style={"textAlign": "center"}),

    dcc.Graph(id="line-chart"),

    html.Div([
        html.Button("1W", id="1w", n_clicks=0),
        html.Button("1M", id="1m", n_clicks=0),
        html.Button("3M", id="3m", n_clicks=0),
        html.Button("6M", id="6m", n_clicks=0),
        html.Button("YTD", id="ytd", n_clicks=0),
        html.Button("1Y", id="1y", n_clicks=0),
        html.Button("MAX", id="max", n_clicks=0),
    ], style={"textAlign": "center", "marginTop": 20, "marginBottom": 20})
])

# Callback
@app.callback(
    Output("line-chart", "figure"),
    Input("1w", "n_clicks"),
    Input("1m", "n_clicks"),
    Input("3m", "n_clicks"),
    Input("6m", "n_clicks"),
    Input("ytd", "n_clicks"),
    Input("1y", "n_clicks"),
    Input("max", "n_clicks")
)
def update_chart(n1w, n1m, n3m, n6m, nytd, n1y, nmax):
    # Determine which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "max"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    end_date = df["Date"].max()
    if button_id == "1w":
        start_date = end_date - timedelta(weeks=1)
    elif button_id == "1m":
        start_date = end_date - timedelta(days=30)
    elif button_id == "3m":
        start_date = end_date - timedelta(days=90)
    elif button_id == "6m":
        start_date = end_date - timedelta(days=180)
    elif button_id == "ytd":
        start_date = datetime(end_date.year, 1, 1)
    elif button_id == "1y":
        start_date = end_date - timedelta(days=365)
    else:  # max
        start_date = df["Date"].min()

    filtered_df = df[df["Date"] >= start_date]

    fig = px.line(filtered_df, x="Date", y="Close", title="Closing Price Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="Price")

    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)