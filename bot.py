# bot.py
import requests
from telegram import Bot
from datetime import datetime, timedelta
import schedule
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

def get_today_timings():
    response = requests.get("https://api.aladhan.com/v1/timingsByCity?city=Istanbul&country=Turkey&method=13")
    timings = response.json()['data']['timings']
    return {
        "İmsak": timings["Fajr"],
        "Güneş": timings["Sunrise"],
        "Öğle": timings["Dhuhr"],
        "İkindi": timings["Asr"],
        "Akşam": timings["Maghrib"],
        "Yatsı": timings["Isha"]
    }

def send_vakit_message(vakit_adi):
    bot.send_message(chat_id=CHAT_ID, text=f"🕌 {vakit_adi} vakti geçti. Allah kabul etsin.")

def schedule_today_messages():
    timings = get_today_timings()
    for vakit, saat_str in timings.items():
        try:
            now = datetime.now()
            saat = datetime.strptime(saat_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            saat += timedelta(minutes=10)
            if saat > now:
                schedule_time = saat.strftime("%H:%M")
                print(f"{vakit} mesajı planlandı: {schedule_time}")
                schedule.every().day.at(schedule_time).do(send_vakit_message, vakit)
        except Exception as e:
            print(f"{vakit} için zamanlama hatası: {e}")

schedule.every().day.at("00:01").do(schedule_today_messages)
schedule_today_messages()

print("Bot çalışıyor...")

while True:
    schedule.run_pending()
    time.sleep(30)
