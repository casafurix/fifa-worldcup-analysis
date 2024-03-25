from bs4 import BeautifulSoup
import pandas as pd
import requests

years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018]


def get_matches(year):
    if year == 2022:
        url = "https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup"
    else:
        url = f"https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup"

    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "lxml")

    matches = soup.find_all("div", class_="footballbox")

    home = []
    score = []
    away = []
    for match in matches:
        home.append(match.find("th", class_="fhome").get_text())
        score.append(match.find("th", class_="fscore").get_text())
        away.append(match.find("th", class_="faway").get_text())

    dict_football = {"home": home, "score": score, "away": away}
    df_football = pd.DataFrame(dict_football)
    df_football["year"] = year

    return df_football


# all FIFA World Cup matches (1930-2018)
fifa = [get_matches(year) for year in years]
df_fifa_till_2018 = pd.concat(fifa, ignore_index=True)
df_fifa_till_2018.to_csv("fifa_worldcup_matches_till_2018.csv", index=False)

# fixtures for 2022 FIFA WC
df_2022_fixtures = get_matches(2022)
df_2022_fixtures.to_csv("2022_fixtures.csv", index=False)
