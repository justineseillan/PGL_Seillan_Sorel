#!/bin/bash
# URL de la page
url="https://www.xe.com/currencyconverter/convert/?Amount=1&From=GBP&To=SEK"
# Récupération du HTML
html=$(curl -s "$url")
# Extraction de la valeur du taux de change (nombre avant le <span class="fade)
exchange_rate=$(echo "$html" | grep -oP '<p class="sc-294d8168-1[^>]*>\K[0-9]+\.[0-9]+(?=<span class="fade)')
# Affichage du taux
echo "Exchange rate (GBP to SEK): $exchange_rate"
