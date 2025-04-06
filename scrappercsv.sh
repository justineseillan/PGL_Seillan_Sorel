#!/bin/bash
# Nom du fichier CSV
output_file="/home/ec2-user/PGL_Seillan_Sorel/exchange_rate_gbp_sek.csv"
<<<<<<< HEAD
# URL de la page
url="https://www.xe.com/currencyconverter/convert/?Amount=1&From=GBP&To=SEK"
# Récupération du HTML
html=$(curl -s "$url")
# Extraction du taux de change
exchange_rate=$(echo "$html" | grep -oP '<p class="sc-294d8168-1[^>]*>\K[0-9]+\.[0-9]+(?=<span class="fade)')
=======

# URL de l'API JSON (floatrates.com)
url="https://www.floatrates.com/daily/gbp.json"

# Récupération du JSON avec curl
json_data=$(curl -s "$url")

# Extraction du taux de change GBP -> SEK avec une regex
exchange_rate=$(echo "$json_data" | grep -oP '(?<="sek":{"code":"SEK","alphaCode":"SEK","numericCode":"752","name":"Swedish Krona","rate":)[0-9]+\.[0-9]+')

>>>>>>> 0c16b07 (Nouveau scrapper avec nouveau site, car l'ancien ne marchait pas comme on voulait)
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
