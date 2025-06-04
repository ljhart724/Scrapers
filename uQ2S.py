import requests
from bs4 import BeautifulSoup
import csv
import fake_useragent as ua
from urllib.parse import urljoin

ua = ua.UserAgent()
headers = {'User-Agent': ua.random}

page = 1

quotes = []
author = []
tags = []
birthdays = []
birthplaces = []
author_urls = []

author_info = {}  # Store author -> URL
author_details = {}  # Store author -> {birthday, birthplace}

for page in range(1, 11):
    QS = requests.get(f"http://quotes.toscrape.com/page/{page}/", headers=headers)
    Q2S = BeautifulSoup(QS.text, "html.parser")

    squotes = Q2S.find_all("span", class_="text")
    for s in squotes:
        quotes.append(s.text)

    anames = Q2S.find_all("small", class_="author")
    for a in anames:
        author.append(a.text)

    ttags = Q2S.find_all("div", class_="tags")
    for t in ttags:
        tag_list = [tag.text.strip() for tag in t.find_all("a")]
        tags.append(", ".join(tag_list))

    # Capture author URLs with author names from quote blocks
    quote_blocks = Q2S.find_all("div", class_="quote")
    for block in quote_blocks:
        a_name = block.find("small", class_="author").text.strip()
        rel_url = block.find("a", href=True)["href"]
        full_url = urljoin("http://quotes.toscrape.com", rel_url)
        if a_name not in author_info:
            author_info[a_name] = full_url

# Now fetch birthdays and birthplaces once per author
for a_name, url in author_info.items():
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    bday = soup.find("span", class_="author-born-date").text.strip()
    bplace = soup.find("span", class_="author-born-location").text.strip()
    author_details[a_name] = {"birthday": bday, "birthplace": bplace}

# Fill in aligned birthdays and birthplaces
for a in author:
    bday = author_details[a]["birthday"]
    bplace = author_details[a]["birthplace"]
    birthdays.append(bday)
    birthplaces.append(bplace)

with open("uQ2S.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Qoutes", "Author", "Tags", "Birthdays", "Birthplaces"])
    for i in range(len(quotes)):
        writer.writerow([quotes[i], author[i], tags[i], birthdays[i], birthplaces[i]])