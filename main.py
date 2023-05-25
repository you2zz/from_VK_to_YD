import os
import time
import json
from math import ceil
from pprint import pprint
import requests
import datetime
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

from vk_photo import VkApiHandler
from yandex_disk import YandexDisk

if __name__ == '__main__':
    vk_token = os.getenv('VK_API_TOKEN_USER') # c методом 'photos.get' - 'VK_API_TOKEN_SERV'
                                              # c методом 'photos.getAll' - 'VK_API_TOKEN_USER'
    yd_token = 'y0_AgAAAAABSEDuAADLWwAAAADi8j6CmHzAb6WNSFuHd3Vip8Dfr0Pycxo'
    
    vk= VkApiHandler(vk_token, '1', 'photos.getAll', 100) # указываются по порядку: токен, 
                                        #ID пользователя VK, 
                                        # метод 'photos.get' или 'photos.getAll'
                                        # число фотографий (по умолчанию 1000)
                                        # версия API (по умолчанию 5.131)
    try:
        with open('vk_photo.json', 'w') as file:
            json.dump(vk.json, file)
    
        yd = YandexDisk('photos_VK',token=yd_token, num = 100)
        yd.create_copy(vk.export_dict)
    except AttributeError as ex:
        print(f'YD: проблемы на стороне VK! У нас все в порядке :-)')
