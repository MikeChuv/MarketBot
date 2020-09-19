import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
import parsingLib
import re
import urllib.parse


def prices_soup(soup):
    price_page = soup.find("div", {'class': 'cia-cs'})
    price_page = price_page.find('a').get('href')
    price_page = 'https://market.yandex.ru' + price_page
    print(price_page)
    price_soup = parsingLib.makeSoup(price_page)
    return price_soup


def get_price(soup):
    price_soup = prices_soup(soup)
    prices = parsingLib.allDIV(price_soup, "price")
    return prices


def get_shop(soup):
    shop_soup = prices_soup(soup)
    shops = shop_soup.findAll("a", {'class': 'n-shop-logo'})
    return shops


def cmd_img(soup, imgs, event, vk_session):
    vk = vk_session.get_api()
    attachments = []
    main_img = soup.find("div", {'class': 'img200'})
    main_img_src = "https://www.e-katalog.ru" + re.search(r'/jpg_zoom1/([0-9])+', str(main_img)).group(0) + ".jpg"
    upload = VkUpload(vk_session)
    main_image = requests.get(main_img_src, stream=True)
    main_photo = upload.photo_messages(photos=main_image.raw)[0]
    attachments.append('photo{}_{}'.format(main_photo['owner_id'], main_photo['id']))
    print(main_img_src)
    for img in imgs:
        img_source = re.search(r'https://mzimg.com/big(?:[a-zA-Z]|[0-9]|[/.-_])+', str(img)).group(0)
        image = requests.get(img_source, stream=True)
        photo = upload.photo_messages(photos=image.raw)[0]
        attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
    vk.messages.send(
        user_id=event.user_id,
        attachment=','.join(attachments),
        message='Фото товара',
        random_id=get_random_id())


def cmd_price(soup, event, vk_session):
    vk = vk_session.get_api()
    vk.messages.send(user_id=event.user_id,
                     message='Получаю цены',
                     random_id=get_random_id())
    my_prices = get_price(soup)
    my_prices1 = []
    my_shops = get_shop(soup)
    print(my_shops)
    for my_shop in my_shops:
        print(my_shop.find('img').get('alt'))
    i = 1
    for my_price in my_prices:
        my_prices1.append('\n' + my_price.text)
    # for my_shop in my_shops:
    #     my_prices1.insert(i, my_shop.find('img').get('alt'))
    #     i += 2

    vk.messages.send(user_id=event.user_id,
                     message=my_prices1,
                     random_id=get_random_id())


def cmd_search_get_url(event, vk_session):
    vk = vk_session.get_api()
    message_list = event.text.split()
    del message_list[0]
    word_string = ""
    for word in message_list:
        word_encoded = urllib.parse.quote_plus(word)
        word_string = word_string + "+" + word_encoded  # сохраняет плюс перед первым словом
    search_url = "https://www.e-katalog.ru/ek-list.php?search_=" + word_string
    vk.messages.send(user_id=event.user_id,
                     message=search_url,
                     random_id=get_random_id())
    return search_url
