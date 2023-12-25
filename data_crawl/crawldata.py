# -*- coding: utf-8 -*-
import time
from lxml import html
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# giả là truy cập từ browser
headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }


def convert_currency_to_number(currency_string):
    # Định dạng số và đơn vị tương ứng
    units = {'K': 1e3, 'M': 1e6, 'B': 1e9}

    # Kiểm tra nếu chuỗi không bắt đầu bằng €, trả về None
    if not currency_string.startswith('€'):
        print("tien ko hop le")
        return None

    # Loại bỏ kí hiệu đơn vị tiền và chuyển đổi chuỗi thành số
    value_str = currency_string[1:-1]
    unit = currency_string[-1]

    # Kiểm tra xem đơn vị có phải là K, M, hoặc B không
    if unit in units:
        multiplier = units[unit]
        value = float(value_str.replace(',', '')) * multiplier
        return value
    else:
        # Trường hợp không có đơn vị hoặc đơn vị không phải là K, M, hoặc B
        return None

players = []
# r = requests.get('https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg%5B4%5D=53&pn%5B0%5D=27&pn%5B1%5D=25&pn%5B2%5D=23&pn%5B3%5D=22&pn%5B4%5D=21&pn%5B5%5D=20&col=vl&sort=desc&offset=0',headers=headers)
# tree = html.fromstring(r.content)
# player_names = [el.text for el in tree.xpath('//table//td//a[@data-tippy-top]')]
# player_ages = [el.text for el in tree.xpath('//table//td[@data-col="ae"]')]
# player_links = tree.xpath('//table//td//a[@data-tippy-top]/@href')

# link = "https://sofifa.com" + player_links[0]

# r = requests.get(link, headers=headers)
# tree = html.fromstring(r.content)
# features = tree.xpath('//article//div[@class="grid attribute"]//div[not(.//h5[text()="PlayStyles"]) and @class="col"]//p//span[@data-tippy-right-start]')
# ratings = tree.xpath('//article//div[@class="grid attribute"]//div[@class="col"]//p//em')
# prices = tree.xpath('//div[./div[text()="Value"]]/em')
# for feature in features:
#     print(feature.text)
# print(player_links[0])

start_page = int(input ('Type start page: '))
amount_page = int(input ('Type amount page: '))
while (amount_page > 0):
    r = requests.get('https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg%5B4%5D=53&pn%5B0%5D=27&pn%5B1%5D=25&pn%5B2%5D=23&pn%5B3%5D=22&pn%5B4%5D=21&pn%5B5%5D=20&col=vl&sort=desc&offset={}'.format(str((start_page-1)*60)),headers=headers)
    tree = html.fromstring(r.content)
    player_names = [el for el in tree.xpath('//table//td//a[@data-tippy-top]')]
    #player_ages = [el for el in tree.xpath('//table//td[@data-col="ae"]')]
    player_links = tree.xpath('//table//td//a[@data-tippy-top]/@href')

    for i in range(len(player_links)):
        player = {

        }
        player['name'] = player_names[i].text
        #player['age'] = player_ages[i]
        link = "https://sofifa.com" + player_links[i]

        r = requests.get(link, headers=headers)
        tree = html.fromstring(r.content)
        features = tree.xpath('//article//div[@class="grid attribute"]//div[not(.//h5[text()="PlayStyles"]) and @class="col"]//p//span[@data-tippy-right-start]')
        ratings = tree.xpath('//article//div[@class="grid attribute"]//div[@class="col"]//p//em')
        price = tree.xpath('//div[./div[text()="Value"]]/em')
        price = convert_currency_to_number(price[0].text)
        if price == None:
            print("discard not clean data")
            continue
        player['Value'] = price
        for i in range(len(features)):
            player[features[i].text] = int(ratings[i].text)
        players.append(player)
    amount_page -= 1
    start_page += 1


print(players)
df = pd.DataFrame(players)
df.to_csv('attack.csv', index=False, encoding='utf-8')

# get_info_player('https://sofifa.com' + '/player/230621/gianluigi-donnarumma/230037/')