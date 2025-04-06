import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from datetime import datetime as dt
import plotly.graph_objects as go
import joblib

# Génération des données
def load_data():
    df = pd.read_csv("exchange_rate_gpb_sek.csv")
    df["Timestamp"] = pd.to_datetime(df['Timestamp'])
    return df

# Calcul des métriques
def daily_report():
    df = load_data()
    if df.empty:
        return "Pas encore de données", {}

    open_price = df.iloc[0]["Exchange Rate"]
    close_price = df.iloc[-1]["Exchange Rate"]
    max_price = df["Exchange Rate"].max()
    min_price = df["Exchange Rate"].min()
    volatility = df["Exchange Rate"].std()

    evolution = ((close_price - open_price) / open_price) * 100

    report = {
        "Ouverture": open_price,
        "Clôture": close_price,
        "Évolution (%)": round(evolution, 2),
        "Max": max_price,
        "Min": min_price,
        "Volatilité": round(volatility, 4)
    }

    return report

# Initialisation Dash
app = dash.Dash(__name__)

# Layout avec thème sombre et design moderne
app.layout = html.Div(style={
    'background': 'linear-gradient(to right, #2D3748, #4A5568)', 'color': '#F1F5F9', 'padding': '30px', 'fontFamily': 'Arial, sans-serif'
}, children=[

    html.H1("Taux de Change GBP -> SEK", style={
        'textAlign': 'center', 'fontSize': '48px', 'marginBottom': '40px', 'color': '#FF6347', 'fontWeight': 'bold'
    }),

    html.Div([
        html.Label("Sélectionnez la plage de dates:", style={
            'fontSize': '18px', 'color': '#D1E8E2', 'fontWeight': 'bold', 'marginBottom': '10px'
        }),
        dcc.DatePickerRange(
            id="date-picker-range",
            start_date="2025-01-01",
            end_date="2025-04-06",
            display_format="YYYY-MM-DD",
            style={'padding': '10px', 'borderRadius': '10px', 'backgroundColor': '#2D3748', 'color': '#F1F5F9'}
        ),
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    html.Div(id="latest-rate", style={
        'textAlign': 'center', 'fontSize': '60px', 'color': '#FF6347', 'fontWeight': 'bold', 'marginBottom': '30px',
        'backgroundColor': '#2D3748', 'padding': '20px', 'borderRadius': '15px', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.2)'
    }),

    html.Div([
        dcc.Graph(id="rate-graph", style={'height': '500px', 'borderRadius': '15px', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.2)'})
    ], style={'backgroundColor': '#2D3748', 'borderRadius': '15px', 'padding': '20px', 'marginBottom': '40px'}),

    html.Div([

        # Rapport journalier
        html.Div(id="daily-report", style={
            'width': '48%', 'display': 'inline-block', 'backgroundColor': '#2D3748', 'borderRadius': '15px', 'padding': '20px',
            'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.2)', 'color': '#F1F5F9'
        }),

        # Prévision ARIMA
        html.Div([
            html.H3("Prévisions ARIMA", style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Label("Nombre de jours à prévoir :", style={'fontWeight': 'bold'}),
            dcc.Slider(
                id='forecast-slider',
                min=1,
                max=10,
                step=1,
                value=3,
                marks={i: str(i) for i in range(1, 11)},
                tooltip={"placement": "bottom"}
            ),
            dcc.Graph(id='forecast-graph', style={'marginTop': '20px'})
        ], id="empty-space", style={
            'width': '48%', 'display': 'inline-block', 'backgroundColor': '#2D3748', 'borderRadius': '15px', 'padding': '20px',
            'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.2)', 'color': '#F1F5F9'
        }),

    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '40px'}),

    dcc.Interval(id="interval-component", interval=5*60*1000, n_intervals=0)
])

# Callback principal
@app.callback(
    [Output("latest-rate", "children"),
     Output("rate-graph", "figure"),
     Output("daily-report", "children")],
    [Input("interval-component", "n_intervals"),
     Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date")]
)
def update_dashboard(n, start_date, end_date):
    df = load_data()
    if df.empty:
        return "Pas encore de données", {"data": [], "layout": {}}, "Rapport non disponible"

    df_filtered = df[(df["Timestamp"] >= start_date) & (df["Timestamp"] <= end_date)]

    latest_rate = df_filtered.iloc[-1]["Exchange Rate"]
    report = daily_report()

    evolution = report.get("Évolution (%)", 0)
    latest_rate_text = f"Taux actuel : {latest_rate} SEK | Évolution : {evolution}%"

    report_html = html.Div([
        html.H3("Rapport Journalier", style={'textAlign': 'center', 'marginBottom': '15px'}),
        html.Ul([
            html.Li(f"{key} : {value}", style={'marginBottom': '5px', 'fontSize': '16px'})
            for key, value in report.items()
        ])
    ])

    figure_main = {
        "data": [go.Scatter(
            x=df_filtered["Timestamp"],
            y=df_filtered["Exchange Rate"],
            mode="lines",
            name="Taux de change",
            line={"color": "#FF6347", "width": 3}
        )],
        "layout": {
            "title": "Évolution du taux de change GBP -> SEK",
            "xaxis": {"title": "Temps"},
            "yaxis": {"title": "Taux de change"},
            "plot_bgcolor": "#2D3748",
            "paper_bgcolor": "#2D3748",
            "font": {"color": "#F1F5F9"}
        }
    }

    return latest_rate_text, figure_main, report_html

# Callback pour prévision ARIMA
@app.callback(
    Output("forecast-graph", "figure"),
    [Input("forecast-slider", "value")]
)
def update_forecast_graph(forecast_days):
    df = load_data()
    df = df.set_index("Timestamp")

    model_fit = joblib.load("arima_gbp_sek_model.pkl")
    forecast = model_fit.forecast(steps=forecast_days)

    last_date = df.index[-1]
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=forecast_days)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index[-20:], y=df["Exchange Rate"].iloc[-20:],
        mode='lines+markers', name="Historique", line=dict(color='orange')
    ))

    fig.add_trace(go.Scatter(
        x=future_dates, y=forecast,
        mode='lines+markers', name="Prévision", line=dict(color='cyan', dash='dash')
    ))

    fig.update_layout(
        title="Prévision du taux de change (ARIMA)",
        xaxis_title="Date",
        yaxis_title="Taux de change",
        plot_bgcolor="#2D3748",
        paper_bgcolor="#2D3748",
        font=dict(color="#F1F5F9")
    )

    return fig

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050)

