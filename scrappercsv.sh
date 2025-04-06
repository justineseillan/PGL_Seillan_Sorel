#!/bin/bash
# Nom du fichier CSV
output_file="/home/ec2-user/PGL_Seillan_Sorel/exchange_rate_gbp_sek.csv"
# URL de la page
url="https://www.xe.com/currencyconverter/convert/?Amount=1&From=GBP&To=SEK"
# Récupération du HTML
html=$(curl -s "$url")
# Extraction du taux de change
exchange_rate=$(echo "$html" | grep -oP '<p class="sc-294d8168-1[^>]*>\K[0-9]+\.[0-9]+(?=<span class="fade)')
# Timestamp actuel (au format ISO 8601)
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
# Vérifie si le fichier existe, sinon ajoute l'en-tête
if [ ! -f "$output_file" ]; then
    echo "Timestamp,Exchange Rate" > "$output_file"
fi
# Ajoute la ligne au CSV
echo "$timestamp,$exchange_rate" >> "$output_file"
# Message de confirmation
echo "Ajouté au CSV : $timestamp, $exchange_rate"
