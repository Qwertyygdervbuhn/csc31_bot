import time
import requests
import random
import os
from dotenv import load_dotenv

from commands.calculator import calculate_expression
from commands.weather import get_weather

load_dotenv()

bot_key = os.getenv("TOKEN", "")
BASE_URL = os.getenv("URL", "https://api.telegram.org/bot").rstrip("/")
url = f"{BASE_URL}{bot_key}/"


def last_update(request: str):
    r = requests.get(request + "getUpdates")
    data = r.json()
    results = data.get("result", [])
    if not results:
        return None
    return results[-1]


def get_updates(offset=None):
    params = {"timeout": 10}
    if offset:
        params["offset"] = offset
    r = requests.get(url + "getUpdates", params=params)
    return r.json().get("result", [])


def send_message(chat, text: str):
    return requests.post(url + "sendMessage", data={"chat_id": chat, "text": text})


def main():
    update_id = None

    while True:
        updates = get_updates(update_id)

        if not updates:
            continue

        for upd in updates:
            update_id = upd["update_id"] + 1

            if "message" not in upd:
                continue

            chat_id = upd["message"]["chat"]["id"]
            text = upd["message"].get("text", "")
            t = text.lower().strip()

            if t in ("hi", "hello", "hey", "привет"):
                send_message(chat_id, "Салем! Черкани /help, чтобы увидеть, что я умею")
                continue

            if t == "csc31":
                send_message(chat_id, "Python")
                continue

            if t == "gin":
                send_message(chat_id, "Finish")
                return

            if t == "python":
                send_message(chat_id, "Версия 3.13🐍")
                continue

            if t == "/help":
                send_message(
                    chat_id,
                    "🛠 Доступные команды:\n\n"
                    "/help — показать команды\n"
                    "/mood — настроение\n"
                    "/rest — как я себя чувствую\n"
                    "/advice — совет\n"
                    "weather <город> — погода\n"
                    "dice — бросить кости 🎲\n"
                    "калькулятор: просто напиши выражение, например 2+2*2\n",
                )
                continue

            if t == "/mood":
                send_message(chat_id, random.choice([
                    "Дайте чашечку кофе.",
                    "Нормально. Перезагрузился, теперь снова живой.",
                    "Хочу спать.",
                    "В ударе! Как студент за 3 часа до дедлайна!",
                    "Сплю, не мешай...",
                ]))
                continue

            if t == "/rest":
                send_message(chat_id, random.choice([
                    "Сегодня я не работаю, лень.",
                    "Не хочу работать. Подожди до завтра.",
                    "Ну сказал же, жди завтра :)",
                ]))
                continue

            if t == "/advice":
                send_message(chat_id, random.choice([
                    "Не делай сегодня то, что можно отложить на после дедлайна.",
                    "Если я работаю — не спрашивай, как я работаю.",
                    "Сохраняй код, не забывай.",
                    "Не пиши комментарии в коде — пусть другой страдает.",
                    "Пей энергетики. Или кофе. Или оба сразу.",
                ]))
                continue

            if t.startswith("weather ") or t.startswith("/weather "):
                city = text.split(" ", 1)[1] if " " in text else ""
                if not city:
                    send_message(chat_id, "Напиши город: weather Kyiv")
                else:
                    send_message(chat_id, get_weather(city))
                continue

            if t == "dice":
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                send_message(chat_id, f"Ты выбросил {a} и {b}!\nИтого: {a + b} 🎲")
                continue

            result = calculate_expression(text)
            if result is not None:
                send_message(chat_id, result)
                continue

            send_message(chat_id, "Сорян, не пониманте. черкани /help для списка команд.")


if __name__ == "__main__":
    main()
