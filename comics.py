from urllib.parse import urlparse

import requests


def get_comics_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_comics(url, filename):
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    comics_id = 353
    url = f'https://xkcd.com/{comics_id}/info.0.json'
    comics = get_comics_response(url)

    img_url = comics['img']
    file_name = urlparse(img_url).path.split('/')[-1]
    get_comics(img_url, file_name)

    print(comics['alt'])




if __name__ == '__main__':
    main()
