import asyncio
import io
import os
import drawer
import model

import telebot

from PIL import Image

# TODO: убрать токен
bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])


# Начальное сообщение
def start_message(message):
    bot.send_message(message.chat.id, "Приветствую! Вы можете отправить только фотографии. Документы и не сжатые фото на данный момент ботом не поддерживаются!")


@bot.message_handler(commands=['start'])
def handle_start(message):
    start_message(message)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]
    temp_message = bot.send_message(message.chat.id, '⌛️ Фотография `' + photo.file_unique_id + '` в обработке! Пожалуйста подождите!')

    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    fp = io.BytesIO(downloaded_file)
    user_image = Image.open(fp)

    prediction = model.predict(user_image)
    image = drawer.draw_bbox(user_image, prediction.labels)

    output_text = '✅ Выполнено! Проблем не обнаружено!\n'
    labels_count = len(prediction.labels)

    if labels_count != 0:
        if labels_count == 1:
            output_text = '⚠️ Найден дефект: ' + model.get_russian_classname(prediction.labels[0].classifier)
        else:
            output_text = '⚠️ Найдены дефекты: \n\n'
            for label in prediction.labels:
                output_text += " * " + model.get_russian_classname(label.classifier) + "\n"

    bot.delete_message(message.chat.id, temp_message.id)
    bot.send_photo(message.chat.id, photo=image, caption=output_text)



def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
