import requests
import matplotlib.pyplot as plt
from datetime import datetime

USERNAME = "Brandon_small"

url = f"https://api.chess.com/pub/player/{USERNAME}/games/archives"
response = requests.get(url)


if response.status_code == 200:
    data = response.json()

    
    if "archives" in data:
        archives = data["archives"]
    else:
        print("No archives found.")
        exit(1)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit(1)

games = []
for archive_url in archives[-3:]:
    archive_response = requests.get(archive_url)
    
 
    if archive_response.status_code == 200:
        archive_data = archive_response.json()
        games.extend(archive_data["games"])
    else:
        print(f"Failed to fetch archive: {archive_url}")

ratings = []
dates = []

for game in games[-100:]:
    if "pgn" not in game:
        continue

    rating = game["white"]["rating"] if game["white"]["username"].lower() == USERNAME.lower() else game["black"]["rating"]
    game_date = datetime.fromtimestamp(game["end_time"])

    ratings.append(rating)
    dates.append(game_date)

plt.figure(figsize=(10, 5))
plt.plot(dates, ratings, marker="o", linestyle="-", color="b", markersize=4)
plt.title(f"{USERNAME}'s Chess.com Rating Over Time")
plt.xlabel("Date")
plt.ylabel("Rating")
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()

plt.savefig("rating_chart.png")
