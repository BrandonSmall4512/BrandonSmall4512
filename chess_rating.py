import requests
import matplotlib.pyplot as plt
from datetime import datetime

USERNAME = "Brandon_small4512"

url = f"https://lichess.org/api/games/user/{USERNAME}?max=100&evals=false&opening=false"
response = requests.get(url, headers={"Accept": "application/x-ndjson"})

games = response.text.strip().split("\n") if response.status_code == 200 else []

ratings = []
dates = []

for game in games:
    try:
        game_data = eval(game)  
        rating = game_data["players"]["white"]["rating"] if game_data["players"]["white"]["user"]["name"].lower() == USERNAME.lower() else game_data["players"]["black"]["rating"]
        game_date = datetime.utcfromtimestamp(game_data["createdAt"] // 1000)
        ratings.append(rating)
        dates.append(game_date)
    except Exception as e:
        print(f"Ошибка при обработке игры: {e}")

if ratings and dates:
    plt.figure(figsize=(10, 5))
    plt.plot(dates, ratings, marker="o", linestyle="-", color="b", markersize=4)
    plt.title(f"{USERNAME}'s Lichess Rating Over Time")
    plt.xlabel("Date")
    plt.ylabel("Rating")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.savefig("rating_chart.png")
else:
    print("Нет доступных данных для построения графика.")
