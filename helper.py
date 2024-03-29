from urllib.parse import urlparse, parse_qs
import json

import requests
from environs import Env


def get_silent_token(url):
    payload = parse_qs(urlparse(url).query)['payload'][0]
    token = json.loads(payload)['token']
    uuid = json.loads(payload)['uuid']
    return token, uuid


def get_access_token(params):
    url = 'https://api.vk.com/method/auth.exchangeSilentAuthToken'
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def main():
    env = Env()
    env.read_env()

    silent_url = env.str('SILENT_URL')
    service_token = env.str('APP_SERVICE_TOKEN')

    silent_token, uuid = get_silent_token(silent_url)

    params = {
        'v': 5.131,
        'token': silent_token,
        'access_token': service_token,
        'uuid': uuid
    }
    print(get_access_token(params)['response']['access_token'])


if __name__ == '__main__':
    main()