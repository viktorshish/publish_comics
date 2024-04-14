from random import randint
import os
from urllib.parse import urlparse

from environs import Env
import requests


def get_latest_comics_number():
    url = f'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_comics_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_comics(url):
    response = requests.get(url)
    response.raise_for_status()

    with open('comics.png', 'wb') as file:
        file.write(response.content)


def get_upload_vk_url(access_token, group_id):
    params = {
        'access_token': access_token,
        'v': '5.199',
        'group_id': group_id
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_response(response)
    return response.json()


def upload_image(url):
    with open('comics.png', 'rb') as file:
        files = {'photo': file}
        response = requests.post(url, files=files)
        response.raise_for_status()
    return response.json()


def save_image_in_albom(access_token, group_id, photo, server_url, photo_hash):
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'photo': photo,
        'server': server_url,
        'hash': photo_hash,
        'v': '5.199',
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=params)
    response.raise_for_status()
    check_response(response)
    return response.json()


def publish_image(access_token, group_id, image_owner_id, image_media_id, image_url, comics_alt):
    parsed_url = urlparse(image_url)
    without_protocol_url = f'{parsed_url.netloc}{parsed_url.path}{parsed_url.params}'
    attachments = f'photo{image_owner_id}_{image_media_id}HTTPS{without_protocol_url}'
    params = {
        'access_token': access_token,
        'owner_id': f'-{group_id}',
        'message': comics_alt,
        'attachments': attachments,
        'v': '5.199'
    }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=params)
    response.raise_for_status()
    check_response(response)
    return response.json()


def check_response(response):
    decoded_response = response.json()
    if 'error' in decoded_response:
        error_code = decoded_response['error']['error_code']
        error_message = decoded_response['error']['error_msg']
        raise requests.exceptions.HTTPError(f'VK API Error {error_code}: {error_message}')


def main():
    env = Env()
    env.read_env()

    access_token = env.str('APP_ACCESS_TOKEN')
    group_id = env.str('VK_GROUP_ID')

    try:
        comics_id = randint(1, get_latest_comics_number()['num'])
        comics_url = f'https://xkcd.com/{comics_id}/info.0.json'

        comics = get_comics_page(comics_url)
        comics_alt = comics['alt']
        img_url = comics['img']
        download_comics(img_url)

        upload_url = get_upload_vk_url(access_token, group_id)['response']['upload_url']
        uploaded_image = upload_image(upload_url)

        photo = uploaded_image['photo']
        server_url = uploaded_image['server']
        photo_hash = uploaded_image['hash']
        saved_image = save_image_in_albom(access_token, group_id, photo, server_url, photo_hash)['response'][-1]

        image_owner_id = saved_image['owner_id']
        image_media_id = saved_image['id']
        image_url = saved_image['sizes'][-1]['url']
        publish_image(access_token, group_id, image_owner_id, image_media_id, image_url, comics_alt)
    except requests.exceptions.HTTPError as error:
        print(f'HTTP error: {error}')
    except requests.exceptions.ConnectionError:
        print('Проблеммы с соединением')
    except FileNotFoundError:
        print('Отсутствует комикс для публикации')

    os.remove('comics.png')


if __name__ == '__main__':
    main()
