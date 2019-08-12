import requests
import csv
from bs4 import BeautifulSoup

url = "https://www.transfermarkt.de/premier-league/fairnesstabelle/wettbewerb/GB1/plus/?saison_id=2019"
heads = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
response = requests.get(url, headers=heads)
html_icerigi = response.text
soup = BeautifulSoup(html_icerigi, "html.parser")
print(soup)


clubs = soup.find_all("a",{"class":"vereinprofil_tooltip"})
club_list = []
for club in clubs:
    club_list.append({"Futbolcu" : club.text.strip()})

print(club_list)