from random import randint
from urllib.parse import urlparse

from environs import Env
import requests


def get_latest_comics_number():
    url = f'https://xkcd.com/info.0.json'
    response = requests.get(url)
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
    return response.json()['response']['upload_url']


def upload_image(url):
    with open('comics.png', 'rb') as file:
        files = {'photo': file}
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()


def save_image_in_albom(access_token, group_id, uploaded_image):
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'photo': uploaded_image['photo'],
        'server': uploaded_image['server'],
        'hash': uploaded_image['hash'],
        'v': '5.199',
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=params)
    return response.json()


def publicate_image(access_token, group_id, saved_image, comics_alt):
    image_owner_id = saved_image['owner_id']
    image_media_id = saved_image['id']
    image_url = saved_image['sizes'][-1]['url']
    image_url_netloc = urlparse(image_url).netloc
    image_url_path = urlparse(image_url).path
    image_url_params = urlparse(image_url).params
    without_protokol_url = image_url_netloc + image_url_path + image_url_params
    attachments = f'photo{image_owner_id}_{image_media_id}HTTPS{without_protokol_url}'
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
    return response.json()


def main():
    env = Env()
    env.read_env()

    access_token = env.str('APP_ACCESS_TOKEN')
    group_id = env.str('VK_GROUP_ID')

    comics_id = randint(1, get_latest_comics_number()['num'])
    comics_url = f'https://xkcd.com/{comics_id}/info.0.json'
    comics = get_comics_page(comics_url)
    comics_alt = comics['alt']
    img_url = comics['img']
    download_comics(img_url)

    upload_url = get_upload_vk_url(access_token, group_id)
    uploaded_image = upload_image(upload_url)
    saved_image = save_image_in_albom(access_token, group_id, uploaded_image)
    publicate_image(
        access_token,
        group_id,
        saved_image['response'][-1],
        comics_alt
    )


if __name__ == '__main__':
    main()
