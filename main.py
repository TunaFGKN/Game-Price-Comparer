from bs4 import BeautifulSoup
import csv
import requests

headerParams = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

name = input("Enter the name of the game which you want to compare prices: ")

def gameNameHandler(name):
    global game_name_steam
    game_name_steam = ""

    global game_name_epic
    game_name_epic = ""

    words = name.lower().split()
    for word in words:
        game_name_steam += word
        if word is not words[-1]:
            game_name_steam += "+"

        game_name_epic += word
        if word is not words[-1]:
            game_name_epic += "%20"

gameNameHandler(name)

steam_url = "https://store.steampowered.com/search/?term=" + game_name_steam
epic_url = "https://store.epicgames.com/en-US/browse?q=" + game_name_epic + "&sortBy=releaseDate&sortDir=DESC&count=40"

response_steam = requests.get(steam_url, headers=headerParams)
html_steam = BeautifulSoup(response_steam.text, "html.parser")

response_epic = requests.get(epic_url, headers=headerParams)
html_epic = BeautifulSoup(response_epic.text, "html.parser")

games_steam = html_steam.find(id="search_results").find_all(id="search_resultsRows")
games_epic = html_epic.find(class_="css-cnqlhg").find_all(class_="css-lrwy1y")
    
print(games_epic)

for game in games_steam:
    anchor = game.a
    title = anchor.find(class_="title").string
    if title.lower() == name.lower():
        price_steam = anchor.find(class_="discount_final_price").string
        print(price_steam)
    else:
        print("Bulunmadi")

    
for game in games_epic:
    anchor = game.a
    title = anchor.find(class_="css-rgqwpc").string
    if title.lower() == name.lower():
        price_epic = anchor.find(class_="eds_1ypbntd0 eds_1ypbntdc eds_1ypbntdk css-12s1vua").string
        print(price_epic)

# print(steam_url)
# print(epic_url)

# todo
# todo
# todo
# todo

# Traceback (most recent call last):
#   File "C:\Users\hp\Desktop\Folders\Scripts\Game Price Comparer\main.py", line 38, in <module>
#     games_epic = html_epic.find(class_="css-cnqlhg").find_all(class_="css-lrwy1y")
#                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# AttributeError: 'NoneType' object has no attribute 'find_all'