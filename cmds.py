import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
import parsingLib

def cmd_img(imgs, event, vk_session):
    vk = vk_session.get_api()
    attachments = []
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


def get_price(soup):
    price_page = soup.find("li", {'data-name': 'offers'})
    price_page = price_page.find('a').get('href')
    price_page = 'https://market.yandex.ru' + price_page
    # print(pricePage)
    price_soup = parsingLib.makeSoup(price_page)
    prices = parsingLib.allDIV(price_soup, "price")
    return prices


def cmd_price(soup, event, vk_session):
    vk = vk_session.get_api()
    vk.messages.send(user_id=event.user_id, message='Получаю цены',
                     random_id=get_random_id())
    myPrices = get_price(soup)
    myPrices1 = []
    for myPrice in myPrices:
        myPrices1.append('\n' + myPrice.text)
    vk.messages.send(user_id=event.user_id, message=myPrices1,
                     random_id=get_random_id())
