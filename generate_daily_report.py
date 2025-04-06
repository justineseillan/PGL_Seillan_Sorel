import pandas as pd
from datetime import datetime as dt

df = pd.read_csv("/home/ec2-user/PGL_Seillan_Sorel/exchange_rate_gbp_sek.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
today = dt.now().date()
df_today = df[df["Timestamp"].dt.date == today]

if df_today.empty:
    exit()

open_price = df_today.iloc[0]["Exchange Rate"]
close_price = df_today.iloc[-1]["Exchange Rate"]
max_price = df_today["Exchange Rate"].max()
min_price = df_today["Exchange Rate"].min()
volatility = df_today["Exchange Rate"].std()
evolution = ((close_price - open_price) / open_price) * 100

with open("/home/ec2-user/PGL_Seillan_Sorel/rapport_quotidien.txt", "w") as f:
    f.write(f"Rapport du {today}\n")
    f.write(f"Ouverture: {open_price}\n")
    f.write(f"Clôture: {close_price}\n")
    f.write(f"Évolution: {round(evolution, 2)}%\n")
    f.write(f"Max: {max_price}\n")
    f.write(f"Min: {min_price}\n")
    f.write(f"Volatilité: {round(volatility, 4)}\n")
