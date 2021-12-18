from bs4 import BeautifulSoup
import requests
import re

url = 'http://dict.ruslang.ru/freq.php?act=show&dic=freq_s&title=%D7%E0%F1%F2%EE%F2%ED%FB%E9%20%F1%EF%E8%F1%EE%EA%20%E8%EC%E5%ED%20%F1%F3%F9%E5%F1%F2%E2%E8%F2%E5%EB%FC%ED%FB%F5'
response = requests.get(url)

site_data = BeautifulSoup(response.text, 'html.parser')
site_data.prettify()
x = site_data.find_all('td')
words_list = []
for i in range(8, len(x), 5):
    words_list.append(x[i])
words_list_text =[]
for k in words_list:
    element = re.sub('</td>', '', (re.sub('<td>', '', str(k))))
    words_list_text.append(element)

with open('words.txt', 'a', encoding ='UTF-8') as file:
    for i in range(len(words_list_text)):
        file.write(f"{words_list_text[i]}\n")