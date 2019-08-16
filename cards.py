import os

try: 
    from selenium import webdriver
except ImportError:
    print('Versuche Selenium zu installieren')
    os.system('python -m pip install selenium') 

try: 
    import numpy as np
except ImportError:
    print('Versuche Selenium zu installieren')
    os.system('python -m pip install numpy') 

options = webdriver.ChromeOptions()
options.add_argument('headless')


urls = [
    "https://en.24score.com/football/england/premier_league/2019-2020/regular_season/cards/",
    "https://en.24score.com/football/germany/1_bundesliga/2019-2020/regular_season/cards/",
    "https://en.24score.com/football/spain/primera_division/2019-2020/regular_season/cards/",
    "https://en.24score.com/football/italy/serie_a/2019-2020/regular_season/cards/", 
    "https://en.24score.com/football/france/ligue_1/2019-2020/1st_round/cards/"
]

counter = 1

for url in urls:

    browser = webdriver.Chrome('chromedriver', options=options)
    browser.get(url)

    ou = browser.find_element_by_class_name("moreless").text
    ou_lines = ou.splitlines()
    ou_lines = [l.replace(" ", "") for l in ou_lines]

    check = False

    if ou_lines[2] == '6.5': result = browser.find_element_by_class_name('total6').text
    elif ou_lines[2] == '5.5': result = browser.find_element_by_class_name('total5').text
    elif ou_lines[2] == '4.5': result = browser.find_element_by_class_name('total4').text
    elif ou_lines[2] == '3.5': result = browser.find_element_by_class_name('total3').text
    elif ou_lines[2] == '2.5': result = browser.find_element_by_class_name('total2').text
    if result == "": 
        result = browser.find_element_by_class_name('totals_ou').text
        check = True

    result = "\n".join(result.split("\n")[1:])
    
    lines = result.splitlines()
    if check == False: lines = lines[:-1]

    lines = [l.replace("  ", "Team ") for l in lines]
    lines = [l.replace("Avg (match)", "Avg_(match)") for l in lines]
    lines = [l.replace("O %", "O_%") for l in lines]
    lines = [l.replace("U %", "U_%") for l in lines]
    lines = [l.replace("C Palace", "Crystal_Palace") for l in lines]
    lines = [l.replace("Man Utd", "Man_Utd") for l in lines]
    lines = [l.replace("Man City", "Man_City") for l in lines]
    lines = [l.replace("West Ham", "West_Ham") for l in lines]
    lines = [l.replace("Sheffield United", "Sheffield_United") for l in lines]
    lines = [l.replace("Aston Villa", "Aston_Villa") for l in lines]
    lines = [l.replace("Fortuna Dusseldorf", "Fortuna_Düsseldorf") for l in lines]
    lines = [l.replace("Union Berlin", "Union_Berlin") for l in lines]
    lines = [l.replace("Bayern Munich", "Bayern_München") for l in lines]
    lines = [l.replace("Werder Bremen", "Werder_Bremen") for l in lines]
    lines = [l.replace("Eintracht Frankfurt", "Eintracht_Frankfurt") for l in lines]
    lines = [l.replace("Real Sociedad", "Real_Sociedad") for l in lines]
    lines = [l.replace("Celta Vigo", "Celta_Vigo") for l in lines]
    lines = [l.replace("Atletico Madrid", "Atletico_Madrid") for l in lines]
    lines = [l.replace("At. Bilbao", "At._Bilbao") for l in lines]
    lines = [l.replace("FC Sevilla", "FC_Sevilla") for l in lines]
    lines = [l.replace("Real Madrid", "Real_Madrid") for l in lines]
    lines = [l.replace("SC Amiens", "SC_Amiens") for l in lines]
    lines = [l.replace("Ol. Lyon", "Ol._Lyon") for l in lines]
    lines = [l.replace("St. Etienne", "St._Etienne") for l in lines]
    lines = [l.replace(".5", ",5") for l in lines]
    lines = [l.replace(" ", ";") for l in lines]
    lines = [l.replace("_", " ") for l in lines]

    browser.quit

    np.savetxt('league' + str(counter) +  '.csv', lines, delimiter=';', fmt='%s', newline='\n')

    print('League done')

    counter = counter + 1

browser.quit
print('All DONE!!!') 




""" 
#Premier League
url = "https://en.24score.com/football/england/premier_league/2019-2020/regular_season/cards/"

browser.get(url)

ou = browser.find_element_by_class_name("moreless").text
ou_lines = ou.splitlines()
ou_lines = [l.replace(" ", "") for l in ou_lines]

if ou_lines[2] == '6.5': result = browser.find_element_by_class_name('total6').text
if ou_lines[2] == '5.5': result = browser.find_element_by_class_name('total5').text
if ou_lines[2] == '4.5': result = browser.find_element_by_class_name('total4').text
if ou_lines[2] == '3.5': result = browser.find_element_by_class_name('total3').text
if ou_lines[2] == '2.5': result = browser.find_element_by_class_name('total2').text


result = "\n".join(result.split("\n")[1:])
result = "\n".join(result.split("\n")[:21])
lines = result.splitlines()

lines = [l.replace("  ", "Team ") for l in lines]
lines = [l.replace("Avg (match)", "Avg_(match)") for l in lines]
lines = [l.replace("O %", "O_%") for l in lines]
lines = [l.replace("U %", "U_%") for l in lines]
lines = [l.replace("C Palace", "Crystal_Palace") for l in lines]
lines = [l.replace("Man Utd", "Man_Utd") for l in lines]
lines = [l.replace("Man City", "Man_City") for l in lines]
lines = [l.replace("West Ham", "West_Ham") for l in lines]
lines = [l.replace("Sheffield United", "Sheffield_United") for l in lines]
lines = [l.replace("Aston Villa", "Aston_Villa") for l in lines]
lines = [l.replace(" ", ";") for l in lines]
lines = [l.replace("_", " ") for l in lines]

np.savetxt('england.csv', lines, delimiter=';', fmt='%s', newline='\n')

print('Premier League done')


#Bundesliga
browser.quit
browser = webdriver.Chrome('chromedriver', options=options)
browser.get("https://en.24score.com/football/germany/1_bundesliga/2019-2020/regular_season/cards/")

ou = browser.find_element_by_class_name("moreless").text
ou_lines = ou.splitlines()
ou_lines = [l.replace(" ", "") for l in ou_lines]

if ou_lines[2] == '6.5': result = browser.find_element_by_class_name('total6').text
if ou_lines[2] == '5.5': result = browser.find_element_by_class_name('total5').text
if ou_lines[2] == '4.5': result = browser.find_element_by_class_name('total4').text
if ou_lines[2] == '3.5': result = browser.find_element_by_class_name('total3').text
if ou_lines[2] == '2.5': result = browser.find_element_by_class_name('total2').text

result = "\n".join(result.split("\n")[1:])
lines = result.splitlines()

lines = [l.replace("  ", "Team ") for l in lines]
lines = [l.replace("Avg (match)", "Avg_(match)") for l in lines]
lines = [l.replace("O %", "O_%") for l in lines]
lines = [l.replace("U %", "U_%") for l in lines]
lines = [l.replace("Fortuna Dusseldorf", "Fortuna_Düsseldorf") for l in lines]
lines = [l.replace("Union Berlin", "Union_Berlin") for l in lines]
lines = [l.replace("Bayern Munich", "Bayern_München") for l in lines]
lines = [l.replace("Werder Bremen", "Werder_Bremen") for l in lines]
lines = [l.replace("Eintracht Frankfurt", "Eintracht_Frankfurt") for l in lines]
lines = [l.replace(" ", ";") for l in lines]
lines = [l.replace("_", " ") for l in lines]

np.savetxt('deutschland.csv', lines, delimiter=';', fmt='%s', newline='\n')

print('Deutschland done')


#Serie A
browser.quit
browser = webdriver.Chrome('chromedriver', options=options)
browser.get("https://en.24score.com/football/italy/serie_a/2019-2020/regular_season/cards/")

ou = browser.find_element_by_class_name("moreless").text
ou_lines = ou.splitlines()
ou_lines = [l.replace(" ", "") for l in ou_lines]

if ou_lines[2] == '6.5': result = browser.find_element_by_class_name('total6').text
if ou_lines[2] == '5.5': result = browser.find_element_by_class_name('total5').text
if ou_lines[2] == '4.5': result = browser.find_element_by_class_name('total4').text
if ou_lines[2] == '3.5': result = browser.find_element_by_class_name('total3').text
if ou_lines[2] == '2.5': result = browser.find_element_by_class_name('total2').text
if result == "": result = browser.find_element_by_class_name('totals_ou').text


result = "\n".join(result.split("\n")[1:])
lines = result.splitlines()


lines = [l.replace("  ", "Team ") for l in lines]
lines = [l.replace("Avg (match)", "Avg_(match)") for l in lines]
lines = [l.replace("O %", "O_%") for l in lines]
lines = [l.replace("U %", "U_%") for l in lines]
lines = [l.replace(" ", ";") for l in lines]

np.savetxt('italien.csv', lines, delimiter=';', fmt='%s', newline='\n')

print('Serie A done')


#La Liga
browser.quit
browser = webdriver.Chrome('chromedriver', options=options)
browser.get("https://en.24score.com/football/spain/primera_division/2019-2020/regular_season/cards/")

ou = browser.find_element_by_class_name("moreless").text
ou_lines = ou.splitlines()
ou_lines = [l.replace(" ", "") for l in ou_lines]

if ou_lines[2] == '6.5': result = browser.find_element_by_class_name('total6').text
if ou_lines[2] == '5.5': result = browser.find_element_by_class_name('total5').text
if ou_lines[2] == '4.5': result = browser.find_element_by_class_name('total4').text
if ou_lines[2] == '3.5': result = browser.find_element_by_class_name('total3').text
if ou_lines[2] == '2.5': result = browser.find_element_by_class_name('total2').text

result = "\n".join(result.split("\n")[1:])
lines = result.splitlines()

lines = [l.replace("  ", "Team ") for l in lines]
lines = [l.replace("Avg (match)", "Avg_(match)") for l in lines]
lines = [l.replace("O %", "O_%") for l in lines]
lines = [l.replace("U %", "U_%") for l in lines]
lines = [l.replace("Real Sociedad", "Real_Sociedad") for l in lines]
lines = [l.replace("Celta Vigo", "Celta_Vigo") for l in lines]
lines = [l.replace("Atletico Madrid", "Atletico_Madrid") for l in lines]
lines = [l.replace("At. Bilbao", "At._Bilbao") for l in lines]
lines = [l.replace("FC Sevilla", "FC_Sevilla") for l in lines]
lines = [l.replace("Real Madrid", "Real_Madrid") for l in lines]
lines = [l.replace(" ", ";") for l in lines]
lines = [l.replace("_", " ") for l in lines]

np.savetxt('spanien.csv', lines, delimiter=';', fmt='%s', newline='\n')

print('La Liga done')

browser.quit

print('All DONE!!!') 

"""