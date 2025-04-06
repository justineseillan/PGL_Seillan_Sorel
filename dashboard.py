import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import os
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def load_data():
    df = pd.read_csv("exchange_rate_gbp_sek.csv")
    return df

# Calculer les stats du jour
def daily_report():
    df = load_data()
    if df.empty:
        return "Pas encore de données", {}

    # Filtrer uniquement les données du jour
    today = dt.now().date()
    df_today = df[df["Timestamp"].dt.date == today]

    if df_today.empty:
        return "Aucune donnée pour aujourd'hui", {}

    # Calcul des métriques
    open_price = df_today.iloc[0]["Exchange Rate"]
    close_price = df_today.iloc[-1]["Exchange Rate"]
    max_price = df_today["Exchange Rate"].max()
    min_price = df_today["Exchange Rate"].min()
    volatility = df_today["Exchange Rate"].std()  # Écart-type

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

app.layout = html.Div([
    html.H1("Taux de Change GBP -> SEK"),

    # Dernier taux de change
    html.Div(id="latest-rate"),

    # Graphique historique
    dcc.Graph(id="rate-graph"),

    # Rapport quotidien
    html.H2("Rapport quotidien"),
    html.Div(id="daily-report"),

    # Mise à jour toutes les 5 minutes
    dcc.Interval(id="interval-component", interval=5*60*1000, n_intervals=0)
])

@app.callback(
    [Output("latest-rate", "children"),
     Output("rate-graph", "figure"),
     Output("daily-report", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n):
    df = load_data()
    if df.empty:
        return "Pas encore de données", {"data": [], "layout": {}}, "Rapport non disponible"

    latest_rate = df.iloc[-1]["Exchange Rate"]
    report = daily_report()

    # Graphique
    figure = {
        "data": [{
            "x": df["Timestamp"],
            "y": df["Exchange Rate"],
            "type": "line",
            "name": "Taux de change"
        }],
        "layout": {
            "title": "Évolution du taux de change GBP -> SEK",
            "xaxis": {"title": "Temps"},
            "yaxis": {"title": "Taux de change"},
        }
    }

    # Format du rapport
    report_html = html.Ul([html.Li(f"{key}: {value}") for key, value in report.items()])

    return f"Taux de change actuel : {latest_rate} SEK", figure, report_html

if __name__ == "__main__":
    app.run(debug=True)
