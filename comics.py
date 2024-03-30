from urllib.parse import urlparse

from environs import Env
import requests


def get_comics_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_comics(url, filename):
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_download_url(params):
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_image(url):
    with open('python.png', 'rb') as file:
        files = {'photo': file}
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()


def main():
    env = Env()
    env.read_env()

    access_token = env.str('APP_ACCESS_TOKEN')
    group_id = env.str('VK_GROUP_ID')

    comics_id = 353
    url = f'https://xkcd.com/{comics_id}/info.0.json'
    comics = get_comics_page(url)
    comics_alt = comics['alt']
    img_url = comics['img']
    file_name = urlparse(img_url).path.split('/')[-1]
    download_comics(img_url, file_name)

    params = {
        'access_token': access_token,
        'v': '5.199',
        'group_id': group_id
    }
    download_url = get_download_url(params)
    print(f'{upload_image(download_url)}')


if __name__ == '__main__':
    main()
