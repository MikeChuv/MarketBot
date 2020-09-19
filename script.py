import requests
from bs4 import BeautifulSoup
import shutil
import parsingLib
import vk_api
import xlsxwriter
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import cmds
import re
import urllib.parse




url = ""
# attachments = []

# soup = parsingLib.makeSoup(url)
workbook = xlsxwriter.Workbook("prices.xlsx")               # создаем новый Excel-документ
worksheet = workbook.add_worksheet()                        # создаем в нем новый лист
# imgs = parsingLib.allDIV(soup, "n-gallery__item")
vk_session = vk_api.VkApi(token='3d845b2a4ef1487db3289577b38b1ceca74997182e00470743e8166e3f8b52d459bf89183f55e5aabcc53')

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


# lets make a dictionary
opts = {
    "tbr": (),
    "cmds": {
        "tbr": ('покажи', 'сколько', 'скинь', 'расскажи'),
        "cIMG": ('скинь картинки', 'фото', 'покажи картинки'),
        "cPrice": ('сколько стоит', 'какая цена', 'цена', 'стоимость'),
        "cShop": ('где продают', 'где купить', 'магазины'),
        "cSearch": ('найди', 'поиск')
    }

}


for event in longpoll.listen():
    tracked_item = False
    search_url = ""
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:  # and event.text:
        # Слушаем longpoll, если пришло сообщение то:
        if event.text == 'Привет' or event.text == 'привет':
            if event.from_user:
                vk.messages.send(user_id=event.user_id,
                                 message='Привет!\n Напиши мне то, что ты хочешь',
                                 random_id=get_random_id())

            # elif event.from_chat:
            #     vk.messages.send(chat_id=event.chat_id, message='Ваш текст', random_id=get_random_id())

        for keys, values in opts["cmds"].items():
            for value in values:
                if len(event.text.split()) != 0:
                    if event.text.split()[0] == value:
                        if keys == "cPrice":
                            cmds.cmd_price(soup, event, vk_session)
                        if keys == "cIMG":
                            cmds.cmd_img(soup, imgs, event, vk_session)
                        if keys == "cSearch":
                            search_url = cmds.cmd_search_get_url(event, vk_session)

        # event.attachments - это словарь с вложениями
        # for key, value in event.attachments.items():
        #     print(key, value)
        if (event.text[12:24] == 'e-katalog.ru') or (event.attachments.get("attach1_type") == 'link'):
            if event.from_user:
                vk.messages.send(user_id=event.user_id,
                                 message='Ссылка получена',
                                 random_id=get_random_id())
            if len(event.attachments) == 0:
                url = event.text
            else:
                url = event.attachments.get("attach1_url")
            soup = parsingLib.makeSoup(url)
            tracked_item = True
            imgs = soup.find_all(onclick=re.compile("mzimg.com/big"), attrs={'class': 'i15-item'})
            prices = soup.find_all(link=re.compile("/ek-item.php\?resolved_name_"), title="Сравнить цены!")
            for price in prices:
                price_page_url = 'https://www.e-katalog.ru' + price['link']
                price_page_soup = parsingLib.makeSoup(price_page_url)
                some_prices = price_page_soup.find_all(attrs={'class': re.compile("shop-([0-9])+")})
                for some_price in some_prices:
                    print(str(some_price.find('a').get('onmouseover')).split('\"')[1])

# переписать этот блок в место со словарем и добавить в словарь команду для картинок
# добавить модуль нечеткого сравнения для комманд словаря





# token: 3d845b2a4ef1487db3289577b38b1ceca74997182e00470743e8166e3f8b52d459bf89183f55e5aabcc53