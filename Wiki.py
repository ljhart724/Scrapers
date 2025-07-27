import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

# Set up User-Agent
ua = UserAgent()
headers = {'User-Agent': ua.random}

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', class_='wikitable')

# Prepare CSV writing
with open('WSVampWiki.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Rank', 'Country', 'GDP (US$)', 'Year'])

    rank = 1
    for row in table.find_all('tr')[1:]:  # Skip header
        cols = row.find_all('td')
        if len(cols) >= 3:
            country = cols[0].text.strip()
            gdp = cols[1].text.strip()
            year = cols[2].text.strip()

            if country.lower() == 'world':  # Skip world total
                continue

            writer.writerow([rank, country, gdp, year])
            rank += 1
