import requests
from bs4 import BeautifulSoup
import shutil
import parsingLib
import vk_api
import xlsxwriter
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


def get_price():
    price_page = soup.find("li", {'data-name': 'offers'})
    price_page = price_page.find('a').get('href')
    price_page = 'https://market.yandex.ru' + price_page
    # print(pricePage)
    price_soup = parsingLib.makeSoup(price_page)
    prices = parsingLib.allDIV(price_soup, "price")
    return prices


url = ""
attachments = []

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
                        vk.messages.send(user_id=event.user_id, message='Получаю цены',
                                         random_id=get_random_id())
                        myPrices = get_price()
                        myPrices1 = []
                        for myPrice in myPrices:
                            myPrices1.append('\n' + myPrice.text)
                        vk.messages.send(user_id=event.user_id, message=myPrices1,
                                         random_id=get_random_id())
                    if keys == "cIMG":
                        for img in imgs:
                            imgSource = img.find('img').get('src')
                            imgSource = "https:" + imgSource
                            upload = VkUpload(vk_session)
                            image = requests.get(imgSource, stream=True)
                            photo = upload.photo_messages(photos=image.raw)[0]
                            attachments.append(
                                'photo{}_{}'.format(photo['owner_id'], photo['id'])
                            )
                        vk.messages.send(
                            user_id=event.user_id,
                            attachment=','.join(attachments),
                            message='Фото товара',
                            random_id=get_random_id()
                        )

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