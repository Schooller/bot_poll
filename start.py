import telebot
from telebot import types
from options import TELEGRAM_TOKEN, MAIN_URL
from functions import *
from time import sleep

bot = telebot.AsyncTeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    if not user_check(message.chat.id):
        return
    bot.send_message(message.chat.id, 'Введите свой индивидуальный код. Формат (XXX-XXX)')
    sleep(0.1)


@bot.message_handler(commands=['admin'])
def start_message(message):
    if not admin_check(message.chat.id):
        return
    result = message.text[6:]
    bot.send_message(message.chat.id, find_user(result))
    sleep(0.1)


@bot.message_handler(commands=['stats'])
def start_message(message):
    if not admin_check(message.chat.id):
        return
    array = get_stats()
    S = 'Статистика кандидатов на президента:\n'
    for key in array['Президент']:
        S+=key[1]+" - "+str(key[0])+" голосов\n"
    S += '\nСтатистика кандидатов на вице-президента:\n'
    for key in array['Вице-президент']:
        S+=key[1]+" - "+str(key[0])+" голосов\n"
    S += '\nВсего голосующих - '+get_max()
    bot.send_message(message.chat.id, S)
    sleep(0.1)


@bot.message_handler(commands=['change'])
def start_message(message):
    if not admin_check(message.chat.id):
        return
    result = message.text[8:]
    if change_user(result):
        bot.send_message(message.chat.id, 'Успешно измененно! Результат ->\n\n'+find_user(result.split(" ")[0]))
    else:
        bot.send_message(message.chat.id, 'Не измененно, ошибка!')
    sleep(0.1)


@bot.message_handler(commands=['info'])
def info_message(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Подробнее...", url=MAIN_URL)
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, 'Спасибо за интерес к жизни РЛ! Ознакомиться с программой наших кандидатов можно здесь.', reply_markup=keyboard)
    sleep(0.1)


@bot.message_handler(content_types=["text"])
def answer_message(message):
    if not user_check(message.chat.id):
        return
    if not code_check(message.text):
        bot.send_message(message.chat.id, 'Код недействителен, если Вы уверены, что делаете все правильно, обратитесь к @dinaduong, @alexvlight или @kovalevix.')
        return
    key_block(message.chat.id, message.text)
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Подробнее...", url=MAIN_URL)
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, 'Спасибо, '+get_name(message.chat.id)+'! Ознакомиться с программой наших кандидатов можно здесь.', reply_markup=keyboard)
    array = get_value('president')
    #Для президента
    keyboard = types.InlineKeyboardMarkup()
    for candidate in array:
        keyboard.add(types.InlineKeyboardButton(text=candidate, callback_data=candidate+'p'))
    keyboard.add(types.InlineKeyboardButton(text="Воздержаться", callback_data="Воздержатьсяp"))
    bot.send_message(message.chat.id, 'Чтобы проголосовать за президента(10 классы) РЛ нажмите на кнопку', reply_markup=keyboard)
    array = get_value('vice-president')
    #Для вице-президента
    keyboard = types.InlineKeyboardMarkup()
    for candidate in array:
        keyboard.add(types.InlineKeyboardButton(text=candidate, callback_data=candidate+'v'))
    keyboard.add(types.InlineKeyboardButton(text="Воздержаться", callback_data="Воздержатьсяv"))
    bot.send_message(message.chat.id, 'Чтобы проголосовать за вице-президента(9 классы) РЛ нажмите на кнопку', reply_markup=keyboard)
    sleep(0.1)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data[-1:]=='p':
            set_answer(call.data, call.message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Изменить свой выбор", callback_data="change1"))
            if call.data[:-1]=='Воздержаться':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Успешная операция, спасибо! Вы воздержались", reply_markup=keyboard)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Успешная операция, спасибо! Вы проголосовали за кандидата ("+call.data[:-1]+")", reply_markup=keyboard)
        elif call.data[-1:]=='v':
            set_answer(call.data, call.message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Изменить свой выбор", callback_data="change2"))
            if call.data[:-1]=='Воздержаться':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Успешная операция, спасибо! Вы воздержались", reply_markup=keyboard)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Успешная операция, спасибо! Вы проголосовали за кандидата ("+call.data[:-1]+")", reply_markup=keyboard)
        elif call.data=='change1':
            array = get_value('president')
            #Для президента
            keyboard = types.InlineKeyboardMarkup()
            for candidate in array:
                keyboard.add(types.InlineKeyboardButton(text=candidate, callback_data=candidate+'p'))
            keyboard.add(types.InlineKeyboardButton(text="Воздержаться", callback_data="Воздержатьсяp"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Чтобы проголосовать за президента(10 классы) РЛ нажмите на кнопку', reply_markup=keyboard)
        else:
            array = get_value('vice-president')
            #Для вице-президента
            keyboard = types.InlineKeyboardMarkup()
            for candidate in array:
                keyboard.add(types.InlineKeyboardButton(text=candidate, callback_data=candidate+'v'))
            keyboard.add(types.InlineKeyboardButton(text="Воздержаться", callback_data="Воздержатьсяv"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Чтобы проголосовать за вице-президента(9 классы) РЛ нажмите на кнопку', reply_markup=keyboard)
    sleep(0.1)

if __name__ == '__main__':
    bot.polling(none_stop=True)
