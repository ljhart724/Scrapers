#Title, Price, Location, and Link

import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

ua = UserAgent()
headers = {'User-Agent': ua.random}

Price = []
Title = []
Location = []
Link = []

url = "https://chicago.craigslist.org/search/sss"
response = requests.get(url, headers=headers)
Craig = BeautifulSoup(response.text, 'html.parser')

try:
    Results = Craig.find_all('li', class_='cl-static-search-result')
    for result in Results:
        Title.append(result.find('div', class_='title').text.strip())
        Location.append(result.find('div', class_='location').text.strip())
        Link.append(result.find('a')['href'])
        price_tag = result.find('div', class_='price')  # <-- updated line
        if price_tag:
            Price.append(price_tag.text.strip())
        else:
            Price.append("N/A")

except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")


with open('vCraig.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Price', 'Title', 'Location', 'Link'])
    for i in range(len(Price)):
        writer.writerow([Price[i], Title[i], Location[i], Link[i]])

print(Price)
print(Title)
print(Location)
print(Link)
print(len(Price), len(Title), len(Location), len(Link))