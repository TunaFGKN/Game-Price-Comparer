import os
import requests
import json
from bs4 import BeautifulSoup
from steam_web_api import Steam
from fuzzywuzzy import fuzz

KEY = os.environ.get("STEAM_API_KEY")
steam = Steam(KEY) # steam object

class GamePriceComparer:
    def __init__(self, game_name):
        self.game_name = game_name
        self.header_params = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
        self.epic_base_url = "https://store.epicgames.com/en-US/browse?q="

        self.epic_game_name = self.format_game_name_for_epic(game_name)

    def format_game_name_for_epic(self, name):
        return "%20".join(name.lower().split())

    def fetch_steam_data(self):
        name = self.game_name
        game_result = None
        highest_ratio = 0
        game_data = []

        games = steam.apps.search_games(name)['apps']

        for game in games:
            ratio = fuzz.ratio(name.lower(), game['name'].lower())
            if ratio > highest_ratio:
                highest_ratio = ratio
                game_result = game

        if highest_ratio > 80:
            title = game_result['name']
            price = game_result['price']
            game_data.append({"title": title, "price":price})
            return game_data
        else:
            raise Exception("Weak match or not found.")

    def fetch_epic_data(self):
        epic_url = self.epic_base_url + self.epic_game_name + "&sortBy=releaseDate&sortDir=DESC&count=40" # https://store.epicgames.com/en-US/browse?q=god%20of%20war&sortBy=relevancy&sortDir=DESC&count=40
        response = requests.get(epic_url, headers=self.header_params)
        html_content = BeautifulSoup(response.text, "html.parser")
        return html_content

    def parse_epic_data(self, html_content):
        game_data = []
        ul_element = html_content.find("ul", class_="css-cnqlhg")  # 'css-cnqlhg' class'lı ul elemanını bul
        if ul_element:
            li_elements = ul_element.find_all("li")  # Tüm <li> elemanlarını bul

            for li in li_elements:
                # Oyun ismini buluyoruz
                title_div = li.find("div", class_="css-rgqwpc")  # Oyun ismini içeren div
                if title_div:
                    title = title_div.string
                    price_span = li.find("span", class_="eds_1ypbntd0 eds_1ypbntdc eds_1ypbntdk css-12s1vua")
                    if price_span:
                        price = price_span.string
                    else:
                        price = "Free"

                    game_data.append({"title": title, "price": price})
        
        return game_data

    def compare_prices(self, steam_data, epic_data):
        # Burada oyunları karşılaştırabilir ve en uygun fiyatı gösterebilirsin.
        for steam_game in steam_data:
            for epic_game in epic_data:
                if steam_game["title"].lower() == epic_game["title"].lower():
                    print(f"Steam: {steam_game['title']} - Price: {steam_game['price']}")
                    print(f"Epic Games: {epic_game['title']} - Price: {epic_game['price']}")
                    # Fiyat karşılaştırması ve en ucuzunu bulma işlemi yapılabilir.

    def run(self):
        epic_html = self.fetch_epic_data()

        steam_data = self.fetch_steam_data()
        epic_data = self.parse_epic_data(epic_html)

        # self.compare_prices(steam_data, epic_data)
        print(steam_data)
        print(epic_data)
       

if __name__ == "__main__":
    name = input("Enter the name of the game which you want to compare prices: ")
    comparer = GamePriceComparer(name)
    comparer.run()




# games = html_content.find_all("div", class_="css-1qhzmhg")
# game_data = []
# for game in games:
#     title = game.find("span", class_="css-2ucwu").get_text()
#     price = game.find("span", class_="css-1y2vzg9").get_text().strip()
#     game_data.append({"title": title, "price": price})
# return game_data