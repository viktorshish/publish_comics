# publish_comics


## Получение [Access token](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/tokens/access-token)

1) Пройдите верификацию акаунта в [новом сервисе авторизации](https://id.vk.com/business/go?utm_source=vk_editapp&utm_medium=referral&utm_campaign=seo_auth_con_serv)- для получения нужных нам прав. Нажмите на 
шестеренку в самом вверху. Введите личные данные.Дождитесь окончания проверки личных данных - проверка проходит 
несколько рабочих дней.

2) Создайте WEB приложение. Обязательно укажите домен и редирект(можно указать недействительный). Настройте права, с
какие будут предоставленны приложению.

3) Вставте в файл ``.env``

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
Произойдет переход на ваш не указанный несуществующий редирект - скопируйте URL. Из payload необходимо получить 
значение ключа token - действует 5 минут.

6) Вставте полученный url в файл ``.env``:
```
SILENT_URL=ВАШ УРЛ
```

7) Запустите скрипт helper.py для извлечение Silent token и замены его на постоянный Access token

```bash 
python helper.py
```
8) Добавте полученный Access token в файл ``.env``:

```
APP_ACCESS_TOKEN=ВАШ_ACCESS_TOKEN
```



