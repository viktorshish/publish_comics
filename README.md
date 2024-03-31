# publish_comics

Publish comics автоматизирует публикацию комиксов с [сайта XKCD](https://xkcd.com). При запуске скрипта, происходит публикация
рандомного комикса на стене вашего сообщества в ВК.


## Получение [Access token](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/tokens/access-token) для работы с API VK

1) Пройдите верификацию аккаунта в [новом сервисе авторизации](https://id.vk.com/business/go?utm_source=vk_editapp&utm_medium=referral&utm_campaign=seo_auth_con_serv), чтобы получить необходимые права. Нажмите на
шестеренку в самом верху. Введите личные данные и дождитесь окончания проверки личных данных - это займет несколько
рабочих дней.

2) Создайте WEB приложение. Обязательно укажите домен и редирект(можно указать недействительный). Настройте права, 
которые будут предоставленны приложению.

3) Создйте в корне каталога файл ``.env`` и добавьте в него:

```
VK_APP_ID=ID_приложения
APP_SERVICE_TOKEN=Сервисный_ключ_доступа
```
Данные находятся в параметрах приложения в сервисе авторизации.

4) Подcтавте в URL свои данные:

<https://id.vk.com/auth?uuid=12345&app_id=ВАШ_ID_APP&response_type=silent_token&redirect_uri=ВАШ_REDIRECT_URL&redirect_state=12345>

Где: 
```
ВАШ_ID_APP - ID приложения
ВАШ_REDIRECT_URL - Доверенный Redirect URL
uuid = любое число , в дальнейшем понадобится для получения access token
```

5) Перейдите по полученому URL. Подтвердите вход в акаунт ВК.
Произойдет переход на ваш несуществующий редирект - скопируйте URL. **URL действителен 5 минут.**

6) Добавьте полученный url в файл ``.env``:
```
SILENT_URL=ВАШ УРЛ
```

7) Запустите скрипт access.py для извлечения Silent token и замены его на постоянный Access token:

```bash 
python access.py
```

8) Добавьте полученный Access token в файл ``.env``:

```
APP_ACCESS_TOKEN=ВАШ_ACCESS_TOKEN
```

## Как установить

Создайте сообщество в ВК и внесите его ID в файл ``.env``:

```VK_GROUP_ID=ВАШ_ID_СООБЩЕСТВА```

Узнать ``VK_GROUP_ID`` можно на [сайте](https://regvk.com/id/) 

Для изоляции проекта рекомендуется развернуть виртуальное окружение:

```
python3 -m venv env
source env/bin/activate
```

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```


## Использование

Для публикации комикса:

```bash
python comics.py
```

