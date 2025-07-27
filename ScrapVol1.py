#Scrape: Book Title, Price, Availability. Challenge: Scrape Multiple Pages(pagination)

import requests
from bs4 import BeautifulSoup
import csv
import fake_useragent as ua

ua = ua.UserAgent()
headers = {'User-Agent': ua.random}

page = 1

prices = []
bAvailability = []
BTitles = []

try:
    for page in range(1,51):
        Books2Scrape = requests.get(f"http://books.toscrape.com/catalogue/page-{page}.html", headers=headers)
        Books2Scrape.raise_for_status()
        BookScrape = BeautifulSoup(Books2Scrape.text, "html.parser")


        price = BookScrape.find_all("p", class_="price_color")
        for p in price:
            prices.append(p.text)

        links = BookScrape.find_all("a") #links/titles
        BTitles.extend([a['title'] for a in BookScrape.find_all('a') if 'title' in a.attrs])

        AAble = BookScrape.find_all("p", class_="instock availability")
        for a in AAble:
            bAvailability.append(a.text.strip())
except requests.exceptions.RequestException as e:
    print(f"Request failed on page {page}: {e}")

with open('VBScrape.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Availability"])
    for i in range(len(prices)):
        writer.writerow([BTitles[i], prices[i], bAvailability[i]])

print(len(prices), len(BTitles), len(bAvailability))
print(prices)
print(BTitles)
print(bAvailability)
