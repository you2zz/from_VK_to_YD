import os
import time
import json
from math import ceil
from pprint import pprint
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

class VkApiHandler:

    base_url = 'https://api.vk.com/method/'
    
    def __init__(self, access_token, id, method, count=1000, version='5.131'):
        self.params = {
            'access_token': access_token,
            'v': version
        }
        self.id = id
        self.count = count
        self.method = method
        try:
            self.json, self.export_dict = self.get_photo_json()
        except:
            print(f'VK: файлы для загрузки получены не были')

    def find_photo_max_size(self, photos_dict):
        """Метод возвращает ссылку на фото максимального размера"""
        photo_max_size = 0
        max_dpi = 0
        types = 'smxopqryzw'
        max_type_index = 0
        for i in range(len(photos_dict)):
            photo_dpi = photos_dict[i].get('width') * photos_dict[i].get('height')
            photo_type = photos_dict[i].get('type')
            if photo_dpi != 0:
                if photo_dpi > max_dpi:
                    max_dpi = photo_dpi
                    photo_max_size = i
            else:
                if types.find(photo_type) > max_type_index:
                    photo_max_size = i
        return photos_dict[photo_max_size].get('url'), photos_dict[photo_max_size].get('type')
    
    def date_time_convert(self, time_unix):
        """Метод преобразует дату загрузки фото в привычный формат"""
        time_conv = datetime.datetime.fromtimestamp(time_unix)
        str_time = time_conv.strftime('%Y-%m-%d_%H-%M-%S')
        return str_time
       
    def get_photo_info(self):
        """Метод для получения количества фотографий и массива фотографий"""
        url = self.base_url + self.method
        params = {
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'rev': 1,
            'owner_id': self.id,
            'count': self.count,
            'offset': 0,
            **self.params
        }
        data_items = []
        x = params['count']        
        finished_count = 0
        while x == params['count']:
            time.sleep(0.33)
            try:
                response = requests.get(url, params=params)
                data = response.json()['response']
            except KeyError as ex:
                print(f'VK: при получении массива фото произошла ошибка: {response.json()["error"]["error_msg"]}! Код ошибки: {response.json()["error"]["error_code"]}')
                return None
            except:
                print(f'VK: ошибка в методе get_photo_info!')
                return None
            data_items.extend(data['items'])
            params['offset'] += params['count']
            finished_count += len(data["items"])
            print(f'Получен массив из {finished_count} фотографий. Выполнено {ceil(finished_count / (data["count"] / 100))} %')
            x = len(data['items'])            
        return data['count'], data_items
    
    def get_photo_params(self):
        """Метод возвращает словарь с параметрами фотографий"""
        try:
            photo_count, photo_items = self.get_photo_info()
        except:
            print('Исключение в методе get_photo_params')
            return None
        result = {}
        for i in range(photo_count):
            number_of_likes = photo_items[i]['likes']['count']
            url_photo, photo_type = self.find_photo_max_size(photo_items[i]['sizes'])
            date_photo = self.date_time_convert(photo_items[i]['date'])
            need_item = result.get(number_of_likes, [])
            need_item.append({
                'number_of_likes': number_of_likes,
                'add_name': date_photo,
                'url_photo': url_photo,
                'size': photo_type
            })
            result[number_of_likes] = need_item            
        return result        

    def get_photo_json(self):
        """Возвращает словарь с параметрами фотографий и список JSON"""
        json_list = []
        upload_dict = {}
        photo_dict = self.get_photo_params()
        try:
            for el in  photo_dict.keys():
                counter = 0
                for value in photo_dict[el]:
                    if len(photo_dict[el]) == 1:
                        file_name = f'{value["number_of_likes"]}.jpeg'
                        upload_dict[file_name] = photo_dict[el][0]['url_photo']
                    else:
                        file_name = f'{value["number_of_likes"]}_{value["add_name"]}.jpeg'
                        upload_dict[file_name] = photo_dict[el][counter]['url_photo']
                        counter += 1
                    json_list.append({'file_name': file_name, 'size':value['size']})                
            return json_list, upload_dict
        except:
            print('get_photo_json')
            return None          