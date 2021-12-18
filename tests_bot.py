import unittest
import time
from telethon.sync import TelegramClient
api_id = 18272629
with open('token.txt', 'r') as file:
    api_hash = file
client = TelegramClient('test_alias', api_id, api_hash)
client.start()


class BotTests(unittest.TestCase):
    def test_start(self):
        client.send_message('your_alias_bot', '/start')
        time.sleep(2)
        message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('Суть игры' in message.message, True)
        time.sleep(2)
        self.change_msg_by_button()

    def change_msg_by_button(self):
        message_start = client.get_messages('your_alias_bot')[0]
        message_start.click(text='Поехали')
        message_mainMenu = client.get_messages('your_alias_bot')
        self.assertEqual(message_mainMenu is not message_start, True)

    def test_start_game_without_teams(self):
        self.test_start()
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='Начать игру')
        message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('добавить хотя бы одну команду' in message.message, True)
        message.click()

    def test_time_changing(self):
        self.test_start()
        message = (client.get_messages('your_alias_bot'))[0]
        message.click(text='Длительность раунда')
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='5')
        message.click(text='ОК')
        message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('Длительность раунда: 5' in message.message, True)

    def test_game_length_changing(self):
        self.test_start()
        message = (client.get_messages('your_alias_bot'))[0]
        message.click(text='Длительность игры')
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='20')
        message.click(text='ОК')
        message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('надо набрать 20' in message.message, True)
        time.sleep(2)

    def add_teams(self):
        self.test_start()
        message = (client.get_messages('your_alias_bot'))[0]
        message.click(text='Добавить команды')
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='Псы Волколаки 🐺')
        message.click(text='ОК')
        message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('Псы Волколаки' in message.message, True)

    def test_game_with_teams(self):
        self.add_teams()
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='Начать игру')
        time.sleep(2)
        message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('Очки команд:' in message.message, True)
        message.click(text='Да!')
        time.sleep(2)
        message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('ваше слово' in message.message, True)
        message.click(text='Отгадано')
        new_message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('ваше слово' in message.message and new_message.message != message.message, True)
        new_message.click(text='Пропущено')
        message = new_message
        new_message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('ваше слово' in message.message and new_message.message != message.message, True)
        new_message.click(text='Отгадано')
        new_message = client.get_messages('your_alias_bot')[0]
        self.assertEqual('Псы Волколаки 2' in new_message.message, True)

    if __name__ == '__main__':
        client.start()
        unittest.main()