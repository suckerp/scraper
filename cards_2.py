import os

try: 
    from selenium import webdriver
except ImportError:
    print('Versuche Selenium zu installieren')
    os.system('python -m pip install selenium --user') 

try: 
    import numpy as np
except ImportError:
    print('Versuche Selenium zu installieren')
    os.system('python -m pip install numpy --user') 

import math

def idx(a_list, value):
    try:
        return a_list.index(value)
    except ValueError:
        return -1


#Beide Browser werden im Headless Modus gestartet, also ohne sichtbares Fenster

#Chrome
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-logging')

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
    "https://en.24score.com/football/italy/serie_a/2019-2020/regular_season/fixtures/"
]

ref_urls = [
    "https://en.24score.com/football/england/premier_league/2019-2020/regular_season/referees/", 
    "https://en.24score.com/football/germany/1_bundesliga/2019-2020/regular_season/referees/",
    "https://en.24score.com/football/spain/primera_division/2019-2020/regular_season/referees/",
    "https://en.24score.com/football/italy/serie_a/2019-2020/regular_season/referees/"
]


#Dateinamen für die Ausgabe der .csv Dateien
countries = [
    "England",
    "Deutschland",
    "Spanien",
    "Italien"
]

#Zähler für den richtigen dateinamen
ref_counter = 0

#Durchlaufen des URL Array
for idx, url in enumerate(urls):
    #Chrome
    browser = webdriver.Chrome('chromedriver', options=options)

    #Firefox
    #browser = webdriver.Firefox(capabilities=cap, options=options)

    #Refs der jeweiligen Liga auslesen
    browser.get(ref_urls[ref_counter])

    container = browser.find_element_by_class_name("data_0_last5")
    browser.execute_script("arguments[0].style.display = 'block';", container)

    refs = browser.find_element_by_class_name("data_0_last5").text.splitlines()

    #refs = refs

    browser.quit()

    #Auslesen der Liga
    browser = webdriver.Chrome('chromedriver', options=options)

    browser.get(url)

    elems = browser.find_elements_by_xpath("//table/tbody//td[contains(@class, 'h2h')]//a[@href]")

    #Anzahl aller Spiele der Liga auslesen
    games = len(elems)
    matches_day = int((0.5 + math.sqrt(games + 0.5)) / 2)

    #Abfrage des aktuellen Spieltags
    matchday = input("Spieltag " + countries[idx] + "? ")
    #Leeres Array für die Spiele des Spieltags
    matches = []
    #Ausrechnen welche Spiele zum Spieltag gehören
    start = games - (int(matchday) * matches_day)
    end = games - (int(matchday) * matches_day - matches_day)

    #Auslesen der URLs für die ausgerechnete Spiele
    for i in range (int(start), int(end)):
        matches.append(elems[i].get_attribute("href"))

    #2D Array für die Karten wird erstellt
    #Das innere ist leer, das äußere wird durch die Anzahl der Spiele pro Spieltag bestimmt
    #Die berechnet sich aus der Hälfte der Teams
    cards = [[0 for x in range(0)] for y in range(int(((games / matches_day / 2) + 1) / 2))]

    #Zähler für das jeweilige Spiel
    counter = 0
    #Leeres Array für die Refs, die einem Spiel zugewiesen wurden
    refs_match = []
    #Der Index wird auf -1 gesetzt
    index_ref = -1

    #Schleife über alle Spiele des jeweiligen Spieltags einer Liga
    for match in matches:
        #Aufrufen der Seite zum Spiel
        browser.get(match)

        #Zuerst wird die Spieltagnummer eingetragen
        cards[counter].append(matchday)
        #Auslesen der Informationen zum Spiel
        ou = browser.find_elements_by_class_name("data_h2h_last20")

        #Auslesen der Daten
        #Zur Sicherheit wird mit try gearbeitet, falls nichts gefunden wird
        try:
            ref_lines = ou[1].text.splitlines()
        except:
            continue
        
        #Prüfen, ob bereits ein Ref zugewiesen wurde
        try:
            index_ref = ref_lines.index("Referee Played Yellow cards Red cards")
            #Falls ja, dann wird aus dem nächsten Element der Liste die Karten-Info ausgelesen
            ou_lines = ou[2].text.splitlines()
            #ou_number = ou_lines.
            index_cards = [ou_lines.index(i) for i in ou_lines if 'Cards' in i]
        except:
            #Falls nein, dann wird nur die Karten Info ausgelesen
            ou_lines = ou[1].text.splitlines()
            index_cards = [ou_lines.index(i) for i in ou_lines if 'Cards' in i]
        
        #Hinzufügen von Heim- u. Auswärtsteam
        #Entfernen von Over / Under bei den Teamnamen
        cards[counter].append(ou_lines[0].replace(' Over', ''))
        cards[counter].append(ou_lines[1].replace('Under ', ''))

        """
        for j in range(2,7):
            container = browser.find_elements_by_class_name("total_rep8_" + str(j) + "5")

            for x in range(0, len(container)):
                browser.execute_script("arguments[0].style.display = 'block';", container[x])


            ou = browser.find_elements_by_class_name("data_h2h_last20")

            try:
                #Falls ja, dann wird aus dem nächsten Element der Liste die Karten-Info ausgelesen
                ou_lines = ou[2].text.splitlines()
                #ou_number = ou_lines.
                index_cards = [ou_lines.index(i) for i in ou_lines if 'Cards' in i]
            except:
                #Falls nein, dann wird nur die Karten Info ausgelesen
                ou_lines = ou[1].text.splitlines()
                index_cards = [ou_lines.index(i) for i in ou_lines if 'Cards' in i]

                
            print(index_cards)
            print(ou_lines)
        """

        #Hinzufügen des Vergleichswerts
        check = ou_lines[index_cards[0]].split(' ')
        cards[counter].append(check[4].replace('.', ','))
        #Hinzufügen der Informationen für die beiden Teams
        #index = index_cards[0] - 2
        cards[counter].append(ou_lines[index_cards[0] - 2] + ' | ' + ou_lines[index_cards[0] - 1])
        cards[counter].append(ou_lines[index_cards[0] + 3] + ' | ' + ou_lines[index_cards[0] + 4])

        #Überprüfung. ob ein Ref in den Infos gefunden wurde
        if (index_ref == 0):
            #Aufteilen der Infos am Leerzeichen
            refs_match = ref_lines[2].split(' ')

            ref_name = []

            for i in range(len(refs_match)-6, -1, -1):
                ref_name.append(refs_match[i])
                
            ref = ref_name[len(ref_name)-1]  
            
            for i in range(len(ref_name)-2, -1, -1):
                ref += ' ' + ref_name[i]

            ref_stats = [s for s in refs if ref in s]

            ref_stats = ref_stats[0].split(' ')

            home = ref_stats[len(ref_stats)-5].split('(')

            away = ref_stats[len(ref_stats)-4].split('(')

            cards[counter].append(str(ref))

            cards[counter].append(str(home[0]) + ' | ' + str(away[0]))

            #cards[counter].append(str(home[0]))
            #cards[counter].append(str(away[0]))
        else:
            cards[counter].append('No Ref')
            cards[counter].append('0 | 0')

        #print(cards)
        
        counter+= 1

    #Ergebnis wird als csv Datei gespeichert
    #Dateiname ist der jeweilige Eintrag aus dem countries-Array
    #Delimiter ist das Semikolon und Zeilenumbrüche werden mir Enter hinterlegt
    results = [nested for nested in cards if nested]

    np.savetxt(".\\output\\" + countries[ref_counter] + ".csv", results, delimiter=';', fmt='%s', newline='\n')

    ref_counter += 1

#Schliessen dees Browsers
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