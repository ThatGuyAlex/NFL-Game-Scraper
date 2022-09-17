import requests
import re
from bs4 import BeautifulSoup
import pprint


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/39.0.2171.95 Safari/537.36'}
games = {}
endUrl = 0
# ---------------------------PickWise Game Grabber-------------------------------------------------#
page = requests.get("https://www.pickswise.com/nfl/", headers={'Cache-Control': 'no-cache'})
soup = BeautifulSoup(page.content, 'lxml')
box = soup.find_all("div", class_="predictions_eventGrid__xDIPy")
game_urls = []

# Grabs all URLs for the upcoming games and adds it to game_urls list.
for time in box:
    links = time.find('div', class_='EventGrid_eventContainer__39T3x')
    for urls in links:
        url = urls.get('href')
        game_urls.append(url)

# ------------Visits each game url and populated dict with info------------------------#
for i in game_urls:
    endUrl += 1
    info = {f"Game{endUrl}": {"Record": {"team1": "",
                                         "team2": ""},
                              "Projected W": "",
                              "Trust Factor": 0,
                              "+/-": 0,
                              }
            }
    # ----- Finds URLS and fills data from webpage ---- #
    updated_url = requests.get(f"https://www.pickswise.com{i}").text
    soup = BeautifulSoup(updated_url, "lxml")
    box = soup.find_all('div', class_="PredictionHeaderTeam_name__Pf64F")
    record = soup.find('table', class_="PredictionEnhancedInfo_predictionEnhancedInfo__35ubN")
    test = soup.find('div', class_="PredictionHeaderTeam_enhancedInfo__3lhgr")

    # ----------Spread Finder
    spread = soup.find_all('div', class_="SelectionInfo_outcome__2Q_iV")[0].get_text()
    spread = re.split(r"-\d{3}", spread, maxsplit=0)[0]
    #pattern = re.compile(r"[a-zA-Z]+\s[a-zA-Z\d]+\s.[\d...]+")  # Activate this to find via regex
    #match = re.findall(pattern, spread)    # Activate this to find via regex

    # ------ Odds Checker ---- #
    plusMinus = soup.find('span', class_="SelectionInfo_line__7hP17").text

    # ------- Best Bet Checker -------- #


    # ------ Finds Over and Under ----- #
    oau = soup.find_all('div', class_="SelectionInfo_outcome__2Q_iV")[1].get_text()
    oau = oau.split('-')[0]


    # ----- Finds the home and away scores ---- #
    pom = test.find('tbody').get_text()
    pomtest = pom[12:24]
    new = re.findall("\d", pomtest)
    awayRecord = '-'.join(new)
    new.reverse()
    homeRecord = '-'.join(new)

    # ----- Adds everything to dict ---- #
    info[f"Game{endUrl}"] = {"Record": {"Away": awayRecord, "Home": homeRecord}}
    info[f"Game{endUrl}"] = {"+/-": plusMinus}
    info[f"Game{endUrl}"]["Away"] = box[0].get_text()
    info[f"Game{endUrl}"]["Home"] = box[1].get_text()
    info[f"Game{endUrl}"]["spread"] = spread
    info[f"Game{endUrl}"]["Over/Under"] = oau
    games.update(info)

# ------------Gets the confidence rating for each team on PickWise-------------------


pprint.pprint(games, sort_dicts=False)

