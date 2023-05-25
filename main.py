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
    vk_token = os.getenv('VK_API_TOKEN')
    yd_token = 'y0_AgAAAAABSEDuAADLWwAAAADi8j6CmHzAb6WNSFuHd3Vip8Dfr0Pycxo'
    
    vk= VkApiHandler(vk_token, '106420704', 30)
    try:
        with open('vk_photo.json', 'w') as file:
            json.dump(vk.json, file)
    
        yd = YandexDisk('анины фото вк',token=yd_token, num = 20)
        yd.create_copy(vk.export_dict)
    except AttributeError as ex:
        print(f'YD: проблемы на стороне VK! У нас все в порядке :-)')