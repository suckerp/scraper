import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)

driver.get("http://www.footcharts.co.uk/index.cfm?task=basics_cards")

url = "http://www.footcharts.co.uk/index.cfm?task=basics_cards"
heads = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
response = requests.get(url, headers=heads)
html_icerigi = response.text
soup = BeautifulSoup(html_icerigi, "html.parser")
print(soup)


clubs = soup.find_all("table",{"class":"table table-condensed sortable"})
club_list = []
for club in clubs:
    club_list.append({"Futbolcu" : club.text.strip()})

print(club_list)