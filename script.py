import requests
from bs4 import BeautifulSoup
import shutil
import parsingLib
import vk_api
import xlsxwriter
from vk_api.longpoll import VkLongPoll, VkEventType
import random

url = "https://market.yandex.ru/product--videokarta-gigabyte-geforce-rtx-2060-super-1845mhz-pci-e-3-0-8192mb-14000mhz-256-bit-3xhdmi-hdcp-aorus/508267028?show-uid=15642358034835005982316003&nid=55314&glfilter=7893318%3A431404&context=search"

soup = parsingLib.makeSoup(url)
workbook = xlsxwriter.Workbook("prices.xlsx")                # создаем новый Excel-документ
worksheet = workbook.add_worksheet()                        # создаем в нем новый лист
imgs = parsingLib.allDIV(soup, "n-gallery__item")
vk_session = vk_api.VkApi(token='3d845b2a4ef1487db3289577b38b1ceca74997182e00470743e8166e3f8b52d459bf89183f55e5aabcc53')

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
commands = ['Скинь картинки', 'Скинь магазины', 'Покажи цены']

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        # Слушаем longpoll, если пришло сообщение то:
        if event.text == 'Привет' or event.text == 'привет':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message='Мои комманды', random_id=random.randint(1, 999999999))
                # for command in commands:
                #     print(command)
                vk.messages.send(user_id=event.user_id, message=commands, random_id=random.randint(1, 999999999))
            elif event.from_chat:
                vk.messages.send(chat_id=event.chat_id, message='Ваш текст', random_id=random.randint(1, 999999999))




# i = 1
# for img in imgs:
#     parsingLib.parseImg(img, "card", str(i))
#     i += 1

pricePage = soup.find("li", {'data-name': 'offers'})
pricePage = pricePage.find('a').get('href')
pricePage = 'https://market.yandex.ru' + pricePage
print(pricePage)

priceSoup = parsingLib.makeSoup(pricePage)
prices = parsingLib.allDIV(priceSoup, "price")

for price in prices:
    priceText = price.text
    print(priceText)

# token: 3d845b2a4ef1487db3289577b38b1ceca74997182e00470743e8166e3f8b52d459bf89183f55e5aabcc53