import requests
import matplotlib.pyplot as plt
from datetime import datetime

USERNAME = "Brandon_small4512"
url = f"https://lichess.org/api/user/{USERNAME}/rating-history"

response = requests.get(url, headers={"Accept": "application/json"})

if response.status_code == 200:
    data = response.json()
    
    # Выбираем рейтинги блица
    blitz_data = next((d for d in data if d["name"] == "Blitz"), None)
    
    if blitz_data:
        years = blitz_data["points"]
        dates = []
        ratings = []

        for year_data in years:
            year = year_data[0]
            for month_index, rating in enumerate(year_data[1:]):
                if rating:  # Если рейтинг не пустой
                    date = datetime(year, month_index + 1, 15)  # 15-е число месяца
                    dates.append(date)
                    ratings.append(rating)

        # Строим график
        plt.figure(figsize=(10, 5))
        plt.plot(dates, ratings, marker="o", linestyle="-", color="b", markersize=4)
        plt.title(f"{USERNAME}'s Lichess Blitz Rating Over Time")
        plt.xlabel("Date")
        plt.ylabel("Rating")
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.savefig("rating_chart.png")
        print("График сохранен: rating_chart.png")
    else:
        print("Нет данных о рейтинге в блице.")
else:
    print("Ошибка запроса:", response.status_code)
