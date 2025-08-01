import requests
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

USERNAME = "Brandon_small4512"
url = f"https://lichess.org/api/user/{USERNAME}/rating-history"

response = requests.get(url, headers={"Accept": "application/json"})

if response.status_code == 200:
    data = response.json()
    
    # Ищем данные блица
    blitz_data = next((d for d in data if d["name"] == "Blitz"), None)
    
    if blitz_data:
        dates = []
        ratings = []
        
        # Обрабатываем каждую точку данных
        for point in blitz_data["points"]:
            # Формат точки: [год, месяц, день, рейтинг]
            if len(point) >= 4:
                year, month, day, rating = point[:4]
                try:
                    date = datetime(year, month, day)
                    dates.append(date)
                    ratings.append(rating)
                except ValueError:
                    continue  # Пропускаем невалидные даты
        
        if not dates:
            print("Нет данных для построения графика.")
            exit()

        # Создаем график с настройками
        plt.figure(figsize=(10, 5))
        plt.plot(dates, ratings, marker="o", linestyle="-", color="#1a759f", 
                 markersize=4, linewidth=1.5)
        
        # Настройка формата дат
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        
        # Подписи и оформление
        plt.title(f"{USERNAME}'s Lichess Blitz Rating", fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Rating", fontsize=12)
        plt.grid(alpha=0.3)
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.tight_layout()
        
        # Сохраняем изображение
        plt.savefig("rating_chart.png", dpi=120)
        print("График успешно сохранен: rating_chart.png")
    else:
        print("Нет данных о рейтинге в блице.")
else:
    print("Ошибка запроса:", response.status_code)
