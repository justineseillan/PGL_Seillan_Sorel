#!/bin/bash
# URL to scrape
url="https://www.xe.com/currencyconverter/convert/?Amount=1&From=GBP&To=SEK"
# Fetch the HTML content
html=$(curl -s "$url")
# Extract the exchange rate using grep and regex
exchange_rate=$(echo "$html" | grep -oP '(?<=1 GBP = )[\d,.]+')
# Print the extracted exchange rate
echo "Exchange rate (GBP to SEK): $exchange_rate"
