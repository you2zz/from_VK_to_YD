import os
import json
from pprint import pprint
import requests
from tqdm import tqdm

class YandexDisk:

    def __init__(self, folder_name, token, num=5):
        self.token = token
        self.file_upload_num = num
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.headers = self.get_headers()
        self.folder = self.create_folder(folder_name)

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
    
    def create_folder(self, folder_name):
        """Метод создает папку на Yandex Disk для загрузки фотографий"""
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code != 200:
            response = requests.put(url, headers=self.headers, params=params)
            if response.status_code == 201:
                print(f'Папка {folder_name} создана в корневом каталоге Яндекс диска')
            else:
                print(f'Папке не была создана! Код ошибки: {response.status_code}')
        else:
            print(f'Папка {folder_name} уже существует. Файлы с одинаковыми именами не будут скопированы')
        return folder_name
        
    def folder_contents(self, folder_name):
        """Метод возвращает содержимое целевой папки"""
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        response = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        folder_contents_list = []
        for el in response:
            folder_contents_list.append(el['name'])
        return folder_contents_list

    
    def create_copy(self, dict_files):
        """Метод загружает фото на Я-диск"""
        content_in_folder = self.folder_contents(self.folder)
        counter = 0
        for key, i in zip(dict_files.keys(), tqdm(range(self.file_upload_num))):
            if counter < self.file_upload_num:
                if key not in content_in_folder:
                    params = {'path': f'{self.folder}/{key}',
                            'url': dict_files[key],
                            'overwrite': 'false'}
                    response = requests.post(self.url, headers=self.headers, params=params)
                    counter += 1
                else:
                    print(f'В папке {self.folder} уже существует файл {key}')
            else:
                break
                
        print(f'Процесс завершен, скопировано новых файлов: {counter} (по умолчанию: 5)\nВсего в исходном альбоме VK файлов: {len(dict_files)}')