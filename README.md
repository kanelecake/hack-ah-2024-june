## Проект Эрис



### Как запустить?

1. Получаем API токен от Telegram через официального бота: https://t.me/botfather
2. После получения токена переходим в корень репозитория и вводим команду:
```shell
 docker build -t eris-tg-bot .
```

> Убедитесь, что Docker запущен и имеет возможность скачивать
> образы из Docker Hub. В ином случае, необходимо настроить прокси.

3. После успешной сборки Docker контейнера, вводим следующую команду.
> Убедитесь, что вы заменили `PLACE_TOKEN_HERE` на ваш токен из Botfather.
```shell
docker run --name eris -e TELEGRAM_TOKEN=PLACE_TOKEN_HERE -t eris-tg-bot
```