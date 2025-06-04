import requests
from bs4 import BeautifulSoup
import csv
import fake_useragent as ua
from urllib.parse import urljoin

ua = ua.UserAgent()
headers = {'User-Agent': ua.random}

Titles = []
PubDate = []
URL2Article = []

RealPythonWeb = requests.get("https://realpython.com", headers=headers)
RealPython = BeautifulSoup(RealPythonWeb.text, "html.parser")

try:
    ATitles = RealPython.find_all('h2', class_='card-title h4 my-0 py-0')
    for title in ATitles:
        Titles.append(title.text.strip())

    Dates = RealPython.find_all('span', class_='mr-2')
    for date in Dates:
        PubDate.append(date.text.strip())

    TheURL = "https://realpython.com/"
    CardArticles = RealPython.find_all('div', class_='col-12 col-md-6 col-lg-4 mb-5')
    for article in CardArticles:
        relative_url = article.find('a')['href']
        full_link = urljoin(TheURL, relative_url)
        URL2Article.append(full_link)

except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")

with open("ScrapedPythonTuts.csv", "w", newline="",encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Titles", "Date Published", "Link"])
    for i in range(len(URL2Article)):
        writer.writerow([Titles[i], PubDate[i], URL2Article[i]])

print(len(Titles))
print(len(URL2Article))
print(len(PubDate))
print(Titles)
print(URL2Article)
print(PubDate)