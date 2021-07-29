import telebot
from rosreestr_api.clients import RosreestrAPIClient

api_client = RosreestrAPIClient()
bot = telebot.TeleBot('1915291850:AAEBE-Se_H_1gqGkaIHfRCevwS6LfzoR5pw')
intro = "Программа для проверки кадастрового номера\n" \
        "участка в базе Росреестра\n" \
        "Пожалуйста, введите желаемый кадастроный номер/номера:"


@bot.message_handler(commands=['start'])
def start(message):
    send_mess = f"<b>Здравствуйте, {message.from_user.first_name}!</b>\n" + intro
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    numbers = message.text.split(' ')
    i = 1
    for num in numbers:
        info = kadorder(num)
        send_mess = f"<b>Кадастровый номер №{i}: {num}</b>\n" + info
        bot.send_message(message.chat.id, send_mess, parse_mode='html')
        i += 1


def kadorder(number):
    build = api_client.get_object(number)
    parceldata = build.get('parcelData')
    objectdata = build.get('objectData')
    if build == '':
        return "Кадастровый номер указан неправильно."
    info = f"<b>Статус объекта:</b> {parceldata.get('parcelStatusStr')}\n" \
           f"<b>Дата постановки на кад. учёт:</b> {parceldata.get('dateCreate')}\n" \
           f"<b>Адрес:</b> {objectdata.get('addressNote')}\n" \
           f"<b>Категория земель:</b> {parceldata.get('categoryTypeValue')}\n" \
           f"<b>Разрешённое использование:</b> {parceldata.get('utilByDoc')}\n" \
           f"<b>Площадь (кв. м):</b> {parceldata.get('areaValue')}\n" \
           f"<b>Кад. стоимость:</b> {parceldata.get('cadCost')}\n" \
           f"<b>Удельная стоимость:</b> {parceldata.get('cadCost') / parceldata.get('areaValue')}\n"
    return info


bot.polling(none_stop=True)
