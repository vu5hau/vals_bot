from flask import Flask, request
from flask_sslify import SSLify
from telebot import types
import requests
import telebot
import random
import sqlite3 as sql
import base64

token = '5141156955:AAFdRpLdzn7vESVJ10aYn5B-hzwMxmL5hIA'
sign = "🚫"
#for imgdb
key = "f7de424a94c063e10998757ceac68ab5"

# app = Flask(__name__)
# sslify = SSLify(app)
#
# url = 'https://ZFreeX.pythonanywhere.com'
#
bot = telebot.TeleBot(token, threaded=False)
bot.remove_webhook()
# bot.set_webhook(url=url)

#
# @app.route('/', methods=['POST'])
# def webhook():
#     update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
#     bot.process_new_updates([update])
#     return 'ok', 200
#
# @app.route('/', methods=['GET'])
# def fuck():
#     return "куда ты лезешь?)", 200


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    data = str(call.data)
    id = int(data[data.find('_')+1:])
    con = sql.connect("linder.db")
    cur = con.cursor()
    #mode = 0 => closed profile
    cur.execute("CREATE TABLE IF NOT EXISTS `users`(`id` INTEGER, `name` STRING, `username` STRING, `gender` STRING, `profile` STRING, `text` STRING, `photo` STRING, `likes` STRING, `macthes` STRING, `mode` INTEGER, `last` INTEGER)")
    cur.execute("SELECT * FROM `users`")
    rows = cur.fetchall()
    indb = False
    for row in rows:
        if row[0] == call.message.chat.id:
            indb = True


    if indb == False:
        cur.execute(f"INSERT INTO `users` VALUES('{call.message.chat.id}', '🚫', '{call.message.chat.username}', '🚫', '🚫', '🚫', '🚫', '', '', '1', '1')")

    if data.startswith("start"):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row('🍓 Лента', '📊 Статистика')
        kb.row('⚙️ Настройки', '🌀 О боте')
        kb.row('🏆 Рейтинг')
        text = "запоминай, детка\n" \
               "Лента - ареал обитания твоего краша.\nздесь ты будешь ставить лайки и перфорировать взглядом фотки на анкетах.\n\n" \
               "В статистике не будет среднего чека за каждую твою пятницу, но зато свои лайки и мэтчи ты там найдешь\n\n" \
               "Настройки - именно в них ты будешь загружать свою фотку с грязным зеркалом\nи записывать любимый профиль 10ФИЛ😍🤤🥰🥵😋\n\n" \
               "Рейтинг - не нужно переезжать в соединенные штаты истерики, если ты не увидишь свое имя в этом списке, у этих ботов все куплено"


        bot.send_message(call.message.chat.id, text, reply_markup=kb)
        bot.send_message(call.message.chat.id, "топай в настройки)")
    elif data.startswith("photo"):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("❌ Отмена")
        bot.send_message(call.message.chat.id, "отправляй фотку)", reply_markup=kb)
        bot.register_next_step_handler(call.message, get_photo)
    elif data.startswith("gender"):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("🙎‍♂️ Парень", "🙍‍♀️ Девушка")
        kb.row("❌ Отмена")
        bot.send_message(call.message.chat.id, "choose ur", reply_markup=kb)
        bot.register_next_step_handler(call.message, get_gender)
    elif data.startswith("name"):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("❌ Отмена")
        bot.send_message(call.message.chat.id, "пиши)\n\nлимит на буквы: 30", reply_markup=kb)
        bot.register_next_step_handler(call.message, get_name)
    elif data.startswith("about"):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("❌ Отмена")
        bot.send_message(call.message.chat.id, "мы внимательно тебя слушаем, 23-летний дизайнер из Санкт-Петербурга)\n\nлимит на буквы: 50", reply_markup=kb)
        bot.register_next_step_handler(call.message, get_about)
    elif data.startswith("profile"):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("❌ Отмена")
        bot.send_message(call.message.chat.id, "", reply_markup=kb)
        bot.register_next_step_handler(call.message, get_about)

    con.commit()
    cur.close()

def get_about(msg):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('🍓 Лента', '📊 Статистика')
    kb.row('⚙️ Настройки', '🌀 О боте')
    kb.row('🏆 Рейтинг')
    con = sql.connect("linder.db")
    cur = con.cursor()
    if msg.text == "❌ Отмена":
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(msg.chat.id, "велкам бэк", reply_markup=kb)
    text = msg.text[:51]
    cur.execute(f"UPDATE users SET text = '{text}' WHERE id = '{msg.from_user.id}'")
    con.commit()
    cur.close()
    bot.send_message(msg.chat.id, 'атака прошла успешно ✅', reply_markup=kb)




def get_name(msg):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('🍓 Лента', '📊 Статистика')
    kb.row('⚙️ Настройки', '🌀 О боте')
    kb.row('🏆 Рейтинг')
    con = sql.connect("linder.db")
    cur = con.cursor()
    if msg.text == "❌ Отмена":
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(msg.chat.id, "велкам бэк", reply_markup=kb)
    name = msg.text[:31]
    cur.execute(f"UPDATE users SET name = '{name}' WHERE id = '{msg.from_user.id}'")
    con.commit()
    cur.close()
    bot.send_message(msg.chat.id, 'как скажешь ✅', reply_markup=kb)


def get_gender(msg):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('🍓 Лента', '📊 Статистика')
    kb.row('⚙️ Настройки', '🌀 О боте')
    kb.row('🏆 Рейтинг')
    con = sql.connect("linder.db")
    cur = con.cursor()
    if msg.text == "❌ Отмена":
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(msg.chat.id, "велкам бэк", reply_markup=kb)
    elif msg.text == "🙎‍♂️ Парень":
        cur.execute(f"UPDATE users SET gender = 'парень' WHERE id = '{msg.from_user.id}'")
        bot.send_message(msg.chat.id, "альфач записан 🥵", reply_markup=kb)
    elif msg.text == "🙍‍♀️ Девушка":
        cur.execute(f"UPDATE users SET gender = 'девушка' WHERE id = '{msg.from_user.id}'")
        bot.send_message(msg.chat.id, "принцесса зафиксирована 🥵", reply_markup=kb)
    con.commit()
    cur.close()




def get_photo(msg):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('🍓 Лента', '📊 Статистика')
    kb.row('⚙️ Настройки', '🌀 О боте')
    kb.row('🏆 Рейтинг')
    if msg.text == "❌ Отмена":
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(msg.chat.id, "велкам бэк", reply_markup=kb)
    else:
        if msg.content_type != "photo":
            bot.send_message(msg.chat.id, "а фотка где? 🤡", reply_markup=kb)
            return
        fileID = msg.photo[-1].file_id
        # print 'fileID =', fileID
        file_info = bot.get_file(fileID)
        # print 'file.file_path =', file_info.file_path
        downloaded_file = bot.download_file(file_info.file_path)
        id = msg.from_user.id
        with open("{}.jpg".format(id), 'wb') as new_file:
            new_file.write(downloaded_file)
        fr = open("{}.jpg".format(id), "rb")
        res = requests.post("https://api.imgbb.com/1/upload", {"image":  base64.b64encode(fr.read()), "key": key})
        res = res.json()
        print(res['data']['url'])
        con = sql.connect("linder.db")
        cur = con.cursor()
        cur.execute(f"UPDATE users SET photo = '{res['data']['url']}' WHERE id = '{id}'")
        con.commit()
        cur.close()
        bot.send_message(msg.chat.id, "пикча добавлена ✅", reply_markup=kb)










@bot.message_handler(commands=['start'])
def start_message(message):
    text = "оооооооо, вы посмотрите!! кто к нам пришееееел!!" \
           "\n\nа че ты тут забыл? ты в курсе вообще, <b>куда ты попал?</b>\n\n<i>ладно, вафля, давай без предисловий</i>\n\n " \
           "короче, ты сейчас в лучшем боте планеты, плагиатами которого являются тиндер и баду, " \
           "кошмарный сон Билла Гейста, эго которого царапает обшивки орбитальных станций и дальше по списку.\n\n" \
           "вещи, которые у тебя появятся здесь:\n\n💦 <b>друзья</b> 💦\n\nда, и такое тоже бывает. " \
           "на самом деле здесь просто спавн твоих будущих кентов и подружек." \
           "\n\n✨ <b>связи</b> ✨\n\nи даже нейронные - две кнопки тыкать будешь все-таки\n\n" \
           "🔥 <b>пара на вальс</b> 🔥\n\nну тут вообще нет слов, да?\n\n<i>все, хватит ждать, го делать из твоего профиля конфетку</i> 👇"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="хочу хочу хочу 😍", callback_data="start_{}".format(message.from_user.id)))
    bot.send_message(message.chat.id, text, reply_markup=kb, parse_mode="HTML")

@bot.message_handler(commands=['menu'])
def start_message(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('🍓 Лента', '📊 Статистика')
    kb.row('⚙️ Настройки', '🌀 О боте')
    kb.row('🏆 Рейтинг')
    bot.send_message(message.chat.id, "ты в главном🤙", reply_markup=kb)


@bot.message_handler(content_types=['text'])
def start_message(msg):
    if msg.text == "⚙️ Настройки":
        con = sql.connect("linder.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM `users`")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == msg.from_user.id:
                text = f"<b>🔮 Имя:</b> {row[1]}\n<b>👤 Пол: </b>{row[3]}\n<b>🍒 Профиль: </b>{row[4]}\n\n"
                if row[5] != sign:
                    text += row[5]
                kb = types.InlineKeyboardMarkup()
                kb.add(types.InlineKeyboardButton(text="Фото 🌅", callback_data="photo_{}".format(msg.from_user.id)))
                kb.add(types.InlineKeyboardButton(text="Имя 📝", callback_data="name_{}".format(msg.from_user.id)))
                kb.add(types.InlineKeyboardButton(text="Профиль 🍭", callback_data="profile_{}".format(msg.from_user.id)))
                kb.add(types.InlineKeyboardButton(text="Пол 🧬", callback_data="gender_{}".format(msg.from_user.id)))
                kb.add(types.InlineKeyboardButton(text="О себе 🎈", callback_data="about_{}".format(msg.from_user.id)))
                if row[6] != sign:
                    bot.send_photo(msg.chat.id, row[6], caption=text, reply_markup=kb, parse_mode="HTML")
                else:
                    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=kb)
                break
        con.commit()
        cur.close()
    elif msg.text == "🍓 Лента":
        con = sql.connect("linder.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        start = 1
        for row in rows:
            if row[0] == msg.from_user.id:
                pass
                """
                start = row[10]
        row = rows[start]
        text = f"<b>🔮 Имя:</b> {row[1]}\n<b>👤 Пол: </b>{row[3]}\n<b>🍒 Профиль: </b>{row[4]}\n\n"
        if row[5] != sign:
            text += row[5]
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb.add(types.InlineKeyboardButton(text="◀️", callback_data="left_{}".format(msg.from_user.id)))
        kb.add(types.InlineKeyboardButton(text="❤️", callback_data="like_{}".format(msg.from_user.id)))
        kb.add(types.InlineKeyboardButton(text="▶️️", callback_data="right_{}".format(msg.from_user.id)))
        bot.send_message(msg.chat.id, text, reply_markup=kb)
        """

print("started")
bot.polling()