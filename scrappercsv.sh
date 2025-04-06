#!/bin/bash
# Nom du fichier CSV
output_file="/home/ec2-user/PGL_Seillan_Sorel/exchange_rate_gbp_sek.csv"

# URL de l'API JSON (floatrates.com)
url="https://www.floatrates.com/daily/gbp.json"

# Récupération du JSON avec curl
json_data=$(curl -s "$url")

# Extraction du taux de change GBP -> SEK avec une regex
exchange_rate=$(echo "$json_data" | grep -oP '(?<="sek":{"code":"SEK","alphaCode":"SEK","numericCode":"752","name":"Swedish Krona","rate":)[0-9]+\.[0-9]+')

# Timestamp actuel (au format ISO 8601)
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# Vérifie si le fichier existe, sinon ajoute l'en-tête
if [ ! -f "$output_file" ]; then
    echo "Timestamp,Exchange Rate" > "$output_file"
fi

# Ajoute la ligne au CSV
echo "$timestamp,$exchange_rate" >> "$output_file"

# Message de confirmation
echo "Ajouté au CSV : $timestamp, $exchange_rate"
