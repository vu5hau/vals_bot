import telebot


kboard= telebot.types.ReplyKeyboardMarkup(True)
kboard.row("Рэгістрацыя", "Расклад на сёння🗓")

kboard_auth= telebot.types.ReplyKeyboardMarkup(True)
kboard_auth.row("Ваш профіль👤", "Расклад на сёння🗓")
kboard_auth.row("Квесты, апытанкі ды іншыя прыгоды🤟")


kboard_admin = telebot.types.ReplyKeyboardMarkup(True)
kboard_admin.row("Рэгістрацыя", "Расклад на сёння🗓")
kboard_admin.row("Ваш профіль👤","Квесты, апытанкі ды іншыя прыгоды🤟")
kboard_admin.row("change_agenda","change_quest")
kboard_admin.row("work_with_quest", "send_all")
kboard_admin.row("add_points", "add_admin")
kboard_admin.row("get_data","get_answers")

kboard_answer = telebot.types.InlineKeyboardMarkup()
key_row = telebot.types.InlineKeyboardButton(text="Даслаць адказ", callback_data="get_answer_from_user")
kboard_answer.add(key_row)

kboard_photo = telebot.types.ReplyKeyboardMarkup(True,True)
kboard_photo.row("Я даслаў/ла ўсе фотаздымкі")
kboard_photo.row("Скасаваць дасыланне фотаздымкаў")
