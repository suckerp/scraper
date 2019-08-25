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


def idx(a_list, value):
    try:
        return a_list.index(value)
    except ValueError:
        return -1


#Beide Browser werden im Headless Modus gestartet, also ohne sichtbares Fenster

#Chrome
options = webdriver.ChromeOptions()
options.add_argument('headless')

#Firefox
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#cap = DesiredCapabilities().FIREFOX
#cap["marionette"] = True
#options = Options()
#options.add_argument("--headless")

#URL zu den verschiedenen Ligen
urls = [
    "https://en.24score.com/football/england/premier_league/2019-2020/regular_season/fixtures/",
    "https://en.24score.com/football/germany/1_bundesliga/2019-2020/regular_season/fixtures/",
    "https://en.24score.com/football/spain/primera_division/2019-2020/regular_season/fixtures/",
    "https://en.24score.com/football/italy/serie_a/2019-2020/regular_season/fixtures/", 
    "https://en.24score.com/football/france/ligue_1/2019-2020/1st_round/fixtures/"
]

#Dateinamen für die Ausgabe der .csv Dateien
files = [
    "england.csv",
    "deutschland.csv",
    "spanien.csv",
    "italien.csv",
    "frankreich.csv"
]

#Zähler für den richtigen dateinamen
counter = 0

#Durchlaufen des URL Array

#Chrome
browser = webdriver.Chrome('chromedriver', options=options)

#Firefox
#browser = webdriver.Firefox(capabilities=cap, options=options)

#Datei öffnen
browser.get("https://en.24score.com/football/england/premier_league/2019-2020/regular_season/fixtures/")




elems = browser.find_elements_by_xpath("//table/tbody//td[contains(@class, 'h2h')]//a[@href]")

games = len(elems)

matchday = input("Spieltag?")

matches = []

start = games - (int(matchday)*10)
end = games - (int(matchday)*10 - 10)


for i in range (start, end):
    matches.append(elems[i].get_attribute("href"))


cards = [[0 for x in range(0)] for y in range(int(((games / 20) + 1) / 2))]



#browser.get("https://en.24score.com/football/england/premier_league/2019-2020/regular_season/referees/")

#refs = browser.find_element_by_class_name("data-tab").text

#refs = refs.splitlines()


counter = 0


for match in matches:

    browser.get(match)

    cards[counter].append(matchday)

    ou = browser.find_elements_by_class_name("data_h2h_last20")

    ou_lines = ou[1].text.splitlines()

    if idx(ou_lines, "Cards 0.5 1.5 2.5 3.5 4.5 5.5 6.5") < 0:
        ou_lines = ou[2].text.splitlines()


    index = ou_lines.index("Cards 0.5 1.5 2.5 3.5 4.5 5.5 6.5")


    cards[counter].append(ou_lines[0].replace(' OVER', ''))
    cards[counter].append(ou_lines[1].replace('UNDER ', ''))
        
    cards[counter].append('\'' + ou_lines[index - 2] + ' - ' + ou_lines[index - 1])
    cards[counter].append('\'' + ou_lines[index + 3] + ' - ' + ou_lines[index + 4])

    print(cards)
    

    counter+= 1







#Ergebnis wird als csv Datei gespeichert
#Dateiname ist der jeweilige Eintrag aus dem files-Array
#Delimiter ist das Semikolon und Zeilenumbrüche werden mir Enter hinterlegt
#np.savetxt(".\\output\\" + files[counter], lines, delimiter=';', fmt='%s', newline='\n')
np.savetxt(".\\output\\england.csv", cards, delimiter=';', fmt='%s', newline='\n')


browser.quit()

"""
for url in urls:
    #Chrome
    browser = webdriver.Chrome('chromedriver', options=options)

    #Firefox
    #browser = webdriver.Firefox(capabilities=cap, options=options)

    #Datei öffnen
    browser.get(url)

    #Finden des Div mit den O/U Optionen
    ou = browser.find_element_by_class_name("moreless").text
    #jedes Ergebnis wird in ein Arrayfeld geschrieben
    ou_lines = ou.splitlines()
    #Leerzeichen werden entfernt
    ou_lines = [l.replace(" ", "") for l in ou_lines]

    #Variable zur Überprüfung, ob bereits ein Spiel stattgefunden hat
    check = True

    #Überprüfung, welches O/U an der 3. Stelle steht und Auslesen der Tabelle
    if ou_lines[2] == '6.5': result = browser.find_element_by_class_name('total6').text
    elif ou_lines[2] == '5.5': result = browser.find_element_by_class_name('total5').text
    elif ou_lines[2] == '4.5': result = browser.find_element_by_class_name('total4').text
    elif ou_lines[2] == '3.5': result = browser.find_element_by_class_name('total3').text
    elif ou_lines[2] == '2.5': result = browser.find_element_by_class_name('total2').text
    #Falls nichts gefunden wurde, weil es noch kein Spiel gab, dann wird nach einer weitern Möglichkeit gesucht
    if result == "": 
        result = browser.find_element_by_class_name('totals_ou').text
        #Prüfvariable wird auf False gesetzt, es hat noch kein Spiel stattgefunden
        check = False

    
    #1. Zeile wird ausgelassen
    result = "\n".join(result.split("\n")[1:])

    #Zeilenweises aufteilen der Ergebnistabelle
    lines = result.splitlines()

    #Falls es schon ein Spiel gab, dann wird auch die letzte Zeile ausgelassen
    if check == True: lines = lines[:-1]

    #Leerzeichen in den Teamnamen und im Header werden mit Unterstrichen ersetzt
    lines = [l.replace("  ", "O/U_" + ou_lines[2] + " ") for l in lines]
    lines = [l.replace("Avg (match)", "Avg_(match)") for l in lines]
    lines = [l.replace("O %", "O_%") for l in lines]
    lines = [l.replace("U %", "U_%") for l in lines]
    lines = [l.replace("C Palace", "Crystal_Palace") for l in lines]
    lines = [l.replace("Man Utd", "Manchester_United") for l in lines]
    lines = [l.replace("Man City", "Manchester_City") for l in lines]
    lines = [l.replace("West Ham", "West_Ham") for l in lines]
    lines = [l.replace("Sheffield United", "Sheffield_United") for l in lines]
    lines = [l.replace("Aston Villa", "Aston_Villa") for l in lines]
    lines = [l.replace("Cologne", "Köln") for l in lines]
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
    #Kommazahlen werden auf den lokalen Standard (Komma statt Punkt) angepasst
    lines = [l.replace(".5", ",5") for l in lines]
    #Verbleibende Leerzeichen werden mit Semikolons als Delimiter ersetzt
    lines = [l.replace(" ", ";") for l in lines]
    #Unterstriche werden wieder mit Leerzeichen ersetzt
    lines = [l.replace("_", " ") for l in lines]


    #Ergebnis wird als csv Datei gespeichert
    #Dateiname ist der jeweilige Eintrag aus dem files-Array
    #Delimiter ist das Semikolon und Zeilenumbrüche werden mir Enter hinterlegt
    np.savetxt(".\\output\\" + files[counter], lines, delimiter=';', fmt='%s', newline='\n')

    #Ausgabe, dass die Datei geschrieben wurde
    print(files[counter] + ' done')

    #Browser wird geschlossen
    browser.quit()

    #Zähler wird um 1 erhöht, damit beim nächsten Durchlauf wieder der passende Dateiname gewählt wird
    counter = counter + 1
"""


#Ausgabe, dass alles erledigt wurde
print('All DONE!!!')

#Am Ende wird der Browser noch einmal geschlossen
browser.quit()