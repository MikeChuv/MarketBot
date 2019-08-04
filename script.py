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





url = ""
# attachments = []

# soup = parsingLib.makeSoup(url)
workbook = xlsxwriter.Workbook("prices.xlsx")                # создаем новый Excel-документ
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
        "cURL": ('держи ссылку', 'вот это'),
        "cPrice": ('сколько стоит', 'какая цена', 'цена', 'стоимость'),
        "cShop": ('где продают', 'где купить', 'магазины')
    }

}


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        # Слушаем longpoll, если пришло сообщение то:
        print(event.text[8:24])
        if event.text == 'Привет' or event.text == 'привет':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message='Привет!\n Напиши мне то, что ты хочешь',
                                 random_id=get_random_id())

            elif event.from_chat:
                vk.messages.send(chat_id=event.chat_id, message='Ваш текст', random_id=get_random_id())

        for keys, values in opts["cmds"].items():
            for value in values:
                if event.text == value:
                    if keys == "cPrice":
                        cmds.cmd_price(soup, event, vk_session)

                    if keys == "cIMG":
                        cmds.cmd_img(imgs, event, vk_session)

        if event.text[8:24] == 'market.yandex.ru':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message='Ссылка получена',
                                 random_id=get_random_id())
            url = event.text
            soup = parsingLib.makeSoup(url)
            imgs = parsingLib.allDIV(soup, "n-gallery__item")

# переписать этот блок в место со словарем и добавить в словарь команду для картинок
# добавить модуль нечеткого сравнения для комманд словаря





# token: 3d845b2a4ef1487db3289577b38b1ceca74997182e00470743e8166e3f8b52d459bf89183f55e5aabcc53