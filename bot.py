import time
import requests
import random
from commands.calculator import calculate_expression
from commands.weather import get_weather
import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv("TOKEN")
URL = os.getenv("URL")
url = f"{URL}{bot_key}/"


class Bot:
    COMMANDS = {
        'hi', 'hello', 'hey',
        'csc31', 'gin', 'python',
        'dice', 'weather',
        'coin', 'ball', 'joke',
        '/help'
    }

    def __init__(self, token, url):
        self.token = token
        self.url = url

    def _last_update(self, request):
        response = requests.get(request + 'getUpdates')
        response = response.json()
        results = response['result']
        if not results:
            return None
        total_updates = len(results) - 1
        return results[total_updates]

    def _get_chat_id(self, update):
        return update['message']['chat']['id']

    def _get_message_text(self, update):
        return update['message']['text']

    def _send_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        return requests.post(url + 'sendMessage', data=params)

    def _handle_csc31(self, update):
        chat_id = self._get_chat_id(update)
        return self._send_message(chat_id, 'Python')

    def _handle_help(self, chat_id):
        help_text = (
            "📌 Available commands:\n"
            "hi / hello / hey — greeting\n"
            "csc31 — about CSC31\n"
            "python — python version\n"
            "dice — roll the dice\n"
            "coin — flip a coin\n"
            "ball — magic 8 ball\n"
            "joke — random joke\n"
            "weather <city> — weather info\n"
        )
        self._send_message(chat_id, help_text)

    def _handle_coin(self, chat_id):
        self._send_message(chat_id, random.choice(['Орёл 🦅', 'Решка 🪙']))

    def _handle_ball(self, chat_id):
        answers = [
            'Да ', 'Нет ', 'Скорее да ',
            'Скорее нет ', 'Точно да ',
            'Точно нет ', 'Спроси позже '
        ]
        self._send_message(chat_id, random.choice(answers))

    def _handle_joke(self, chat_id):
        jokes = [
            'Программист пошёл в магазин и купил 1 хлеб, потом купил ещё 1 хлеб, потому что цикл.',
            'Почему Python не лает? Потому что он интерпретатор.',
            'Баг — это не ошибка, а неожиданная функция.',
            'Программист без кофе — как сервер без питания.'
        ]
        self._send_message(chat_id, random.choice(jokes))

    def run(self):
        bot_work = True
        while bot_work:
            last_update = self._last_update(self.url)
            if last_update is None:
                time.sleep(3)
                continue

            update_id = last_update['update_id']

            try:
                while bot_work:
                    time.sleep(1)
                    self.update = self._last_update(url)
                    if update_id == self.update['update_id']:

                        text = self._get_message_text(self.update).lower()
                        chat_id = self._get_chat_id(self.update)

                        if text in ('hi', 'hello', 'hey'):
                            self._send_message(chat_id, 'Greetings! Type /help to see commands.')

                        elif text == '/help':
                            self._handle_help(chat_id)

                        elif text == 'csc31':
                            self._handle_csc31(self.update)

                        elif text == 'gin':
                            self._send_message(chat_id, 'Finish')
                            bot_work = False

                        elif text == 'python':
                            self._send_message(chat_id, 'version 3.10')

                        elif 'weather' in text:
                            city = text.replace('weather ', '')
                            weather = get_weather(city)
                            self._send_message(chat_id, weather)

                        elif text == 'dice':
                            _1 = random.randint(1, 6)
                            _2 = random.randint(1, 6)
                            self._send_message(
                                chat_id,
                                f'You have {_1} and {_2}!\nYour result is {_1 + _2}!'
                            )

                        elif text == 'coin':
                            self._handle_coin(chat_id)

                        elif text == 'ball':
                            self._handle_ball(chat_id)

                        elif text == 'joke':
                            self._handle_joke(chat_id)

                        else:
                            result = calculate_expression(self._get_message_text(self.update))
                            if result is not None:
                                self._send_message(chat_id, result)
                            else:
                                self._send_message(chat_id, 'Sorry, I don\'t understand you :(')

                        update_id += 1

            except KeyboardInterrupt:
                print('\nБот зупинено')


if __name__ == '__main__':
    bot = Bot(bot_key, url)
    bot.run()
