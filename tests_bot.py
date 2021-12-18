import unittest
import time
from new_db import Team, Session
from telethon.sync import TelegramClient
api_id = 18272629
api_hash = '63ee105f4f0fc9c0657bde7bcbb3a0bb'
client = TelegramClient('test_alias', api_id, api_hash,)
client.start()

class BotTests(unittest.TestCase):
    def test_start(self):
        client.send_message('your_alias_bot', '/start')
        time.sleep(2)
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='Поехали')
    def test_time_5(self) -> True:
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='Длительность раунда')
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='5')
        message.click(text='ОК')
        message = client.get_messages('your_alias_bot')[0]
        if 'Длительность раунда: 5' in message.message:
            return True
        else:
            return False
    def test_time_10(self) -> True:
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='Длительность раунда')
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='10')
        message.click(text='ОК')
        message = client.get_messages('your_alias_bot')[0]
        if 'Длительность раунда: 10' in message.message:
            return True
        else:
            return False
    def test_time_15(self) -> True:
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='Длительность раунда')
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='15')
        message.click(text='ОК')
        message = client.get_messages('your_alias_bot')[0]
        if 'Длительность раунда: 15' in message.message:
            return True
        else:
            return False
    def test_time_50(self) -> True:
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='Длительность раунда')
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='50')
        message.click(text='ОК')
        message = client.get_messages('your_alias_bot')[0]
        if 'Длительность раунда: 50' in message.message:
            return True
        else:
            return False
    def test_time_3(self) -> True:
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='Длительность раунда')
        message = client.get_messages('your_alias_bot')[0]
        message.click(text='3')
        message.click(text='ОК')
        message = client.get_messages('your_alias_bot')[0]
        if 'Длительность раунда: 3' in message.message:
            return True
        else:
            return False
    if __name__ == '__main__':
        client.start()
        unittest.main()