import telebot 

from bd import *
from kboard import *
import time


TOKEN = "1621900333:AAHXAQiX9VYlSkFrGr_C1EM-fEi8hRX4Tqk"
admin_id = 472430201

bot = telebot.TeleBot(TOKEN)



# Нататкі ў будучыню
# Дадаць магчымасць:
# 1. выдаляць карыстальнікаў
# 2. забіраць адміна
# 3. усе калі, звязаныя з адмінам, можна занесці пад адзін if
# 4. 





try:
    bot.send_message(admin_id, "Я зноў працую")
except:
    pass


def admin_check_quest(message,id,start):
    if message.text in "yY":
        change_checked(id,start)
        bot.send_message(message.chat.id,"Гэтая праца прайшла мадэрацыю і чалавек атрымаў за яе балы")
    else:
        bot.send_message(message.chat.id,"Гэтая праца не прайшла мадэрацыю і вяртаецца ў спіс")

# def get_profile_str(id):
#     result = "Ваш профіль 👤:" + "\n" + "\n"
#     user = get_user(id)
#     result += "Ваш id: " + str(user[0]) + "\n"
#     result += "Вашае імя: " + user[3] + "\n"
#     result += "Ваш клас: " + user[2] + "\n"
#     result += "У Вас балаў: " + str(user[4]) + "\n"
#     result += "Вашыя сацыяльныя сеткі: " + user[5] + "\n"*4 
#     result += "Калі Вы зрабілі памылку падчас рэгістрацыі ці ў Вас з'явіліся пытанні, націсніце /contacts"
#     return result

def ans_send_all_checker(message,text):
    if message.text in "yY":
        users = get_users()
        # print(users)
        for i in range(len(users)):
            try:
                bot.send_message(users[i][1],text)
            except:
                bot.send_message(admin_id, "Чалавек з наступным id не атрымаў паведамленне, якое для ўсіх " + str(users[i][1]))
            time.sleep(1)
    else:
        bot.send_message(message.chat.id,"Вы скасавалі адпраўку")

def ans_send_all(message):
    bot.send_message(message.chat.id, "Вы ўпэўнены, што жадаеце даслаць усім наступны тэкст(y/n): " + "\n"*3 + message.text)
    bot.register_next_step_handler(message, ans_send_all_checker, message.text)


def ans_add_points_2(message,list_of_id):
    reason = message.text
    bot.send_message(message.chat.id,"Якую колькасць балаў дадаць людзям з id: " + str(list_of_id))
    bot.register_next_step_handler(message, ans_add_points_3,list_of_id,reason)

def ans_add_points_3(message,list_of_id,reason):
    score = int(message.text)

    for i in range(len(list_of_id)):
        add_points(list_of_id[i],score)
        try:
            bot.send_message(get_user_id(list_of_id[i])[1],"Вашая колькасць балаў змянілася. Вы атрымалі " + str(score) + " бал(аў)" + "\n" + "Вы атрымалі балы за " + reason)
            time.sleep(1)
        except:
            bot.send_message(admin_id, "Чалавек з наступным id не атрымаў паведамленне пра балы " + str(list_of_id[i])[1])
    bot.send_message(message.chat.id,"Вы дадалі "  + str(score) +  " балаў " + str(len(list_of_id)) +  " удзельнікам")


def ans_add_points(message):
    users_with_new_points = message.text.split()
    bot.send_message(message.chat.id,"Вы атрымалі балы за  ... [АДКАЖЫЦЕ так, каб гэты сказ меў сэнс!]" )
    bot.register_next_step_handler(message, ans_add_points_2, users_with_new_points)


def ans_quest(message):
    with open("quest.txt","w+", encoding="utf-8") as f:
        f.write(message.text)
    bot.send_message(message.chat.id,"Тэкст зменены")

def ans_admin(message):
    with open("timetable.txt","w+", encoding="utf-8") as f:
        f.write(message.text)
    bot.send_message(message.chat.id,"Тэкст зменены")

def ans_new_admin(message):
    id_of_new_admins = message.text.split()
    for i in range(len(id_of_new_admins)):
        if(len(get_user(id_of_new_admins[i]))):
            add_admin(id_of_new_admins[i])
        else:
            bot.send_message(message.chat.id,"Няма карыстальніка з id " + str(id_of_new_admins[i]))
    bot.send_message(message.chat.id,"Дадаў " + str(len(id_of_new_admins)) + " адмінаў")


def ans_links(message,name,form):
    links = message.text
    if len(links) > 1024:
        bot.send_message(message.chat.id,"Колькасць сімвалаў абмежавана ў 1024. Пачніце працэс рэгістрацыі зноў",reply_markup= kboard)
    else:
        add_user(message.chat.id,name,form,links,message.from_user.username)
        bot.send_message(message.chat.id,"Віншуем!🥳 Вы паспяхова зарэгістраваны!🤟",reply_markup=kboard_auth)
        bot.send_message(message.chat.id,get_profile_str(message.chat.id))

def ans_form(message,name):
    form = message.text
    if len(form) > 128:
        bot.send_message(message.chat.id,"Колькасць сімвалаў абмежавана ў 128. Пачніце працэс рэгістрацыі зноў",reply_markup=kboard)
    else:
        bot.send_message(message.chat.id,"Дашліце спасылкі на Вашыя сацыяльныя сеткі(https://vk.com/tydzenrodnajmovy) альбо '-'")
        bot.register_next_step_handler(message, ans_links, name,form)

def ans_name(message):
    name = message.text
    if len(name) > 128:
        bot.send_message(message.chat.id,"Колькасць сімвалаў абмежавана ў 128. Пачніце працэс рэгістрацыі зноў",reply_markup=kboard)
    else:
        bot.send_message(message.chat.id,"Да якой групы Вы адносіцеся? Адказвайце, калі ласка, наступным чына:" + "\n"*2 + "- Вучань(10 Філ)" + "\n"+ "- Настаўніца(кафедра інфарматыкі)" + "\n"  + "- Выпускніца(12 Гіст)")
        bot.register_next_step_handler(message, ans_form, name)





# ПАЧАТАК РАБОТЫ !!!
@bot.message_handler(commands= ['start'])
def start_cmd(message):
    if len(get_user(message.chat.id)):
        bot.send_message(message.chat.id,"Вітаем!👋" + "\n"*2 + "Гэта бот Тыдня роднай мовы ў Ліцэі БДУ. Тутака Вы можаце даведацца раскалад актыўнасцяў на сёння ды даслаць вашыя адказ на тэсты і квесты." + "\n" +  "За Вашую дзейнасць падчас тыдня(наведванне мерапрыемств, удзел у квестах і г.д.) Вы будзеце атрымліваць балы, а потым самыя адданыя гэтай справе атрымаюць ад нас падарункі!🎁" + "\n"*2 + "Хутчэй цісніце РЭГІСТРАЦЫЯ, каб прыняць удзел! "  + "Поспехаў!",reply_markup=kboard_auth)
    else:
        bot.send_message(message.chat.id,"Вітаем!👋" + "\n"*2 + "Гэта бот Тыдня роднай мовы ў Ліцэі БДУ. Тутака Вы можаце даведацца раскалад актыўнасцяў на сёння ды даслаць вашыя адказ на тэсты і квесты." + "\n"  + "За Вашую дзейнасць падчас тыдня(наведванне мерапрыемств, удзел у квестах і г.д.) Вы будзеце атрымліваць балы, а потым самыя адданыя гэтай справе атрымаюць ад нас падарункі!🎁" + "\n"*2 + "Хутчэй цісніце РЭГІСТРАЦЫЯ, каб прыняць удзел! " + "Поспехаў!",reply_markup=kboard)


@bot.message_handler(content_types= ['text'])
def send(message):
    text = message.text
    if(text == "Рэгістрацыя"):
        if(len(get_user(message.chat.id))):
            bot.send_message(message.chat.id,"Вы ўжо прайшлі працэс рэгістрацыі")
        else:
            bot.send_message(message.chat.id,"Увядзіце, калі ласка, Вашае прозвішча і імя:")
            bot.register_next_step_handler(message,ans_name)
    elif(text == "Расклад на сёння🗓"):
        # print(message)
        # print()
        # print(message.from_user.username)
        try: 
            f = open("timetable.txt",encoding="utf-8")
            timetable = f.read()
            f.close()
            bot.send_message(message.chat.id,timetable)
        except:
            bot.send_message(message.chat.id,"Расклад хутка з'явіцца")


    elif(text == "Квесты, апытанкі ды іншыя прыгоды🤟"):
        if(len(get_user(message.chat.id))):
            try: 
                f = open("quest.txt",encoding="utf-8")
                quest_text = f.read()
                f.close()
                bot.send_message(message.chat.id,quest_text,reply_markup=kboard_answer)
            except:
                bot.send_message(message.chat.id, "Спіс актыўнасцяў хутка з'явіцца.",reply_markup=kboard_answer)
        else:
            bot.send_message(message.chat.id,"Прайдзіце спачатку рэгістрацыю")
        


    elif(text == "Ваш профіль👤"):
        if len(get_user(message.chat.id)):
            bot.send_message(message.chat.id, get_profile_str(message.chat.id))
        else:
            bot.send_message(message.chat.id, "Вы яшчэ не зарэгістраваны")


    elif(text == "/contacts"):
        if len(get_user(message.chat.id)):
            bot.send_message(message.chat.id, "Калі ў вас з'явілася пытанне, праблема ці запыт. Калі ласка, звяртайцеся да @vushauv",reply_markup=kboard_auth)
        else:
            bot.send_message(message.chat.id, "Калі ў вас з'явілася пытанне, праблема ці запыт. Калі ласка, звяртайцеся да @vushauv",reply_markup=kboard)
             
    elif(text == "add_points" and len(get_user(message.chat.id)) and (message.chat.id == admin_id or get_user(message.chat.id)[6] == 1)):
        bot.send_message(message.chat.id,"Увядзіце спіс усіх, каму вы жадаеце дадаць аднолькавую колькасць балаў")
        bot.register_next_step_handler(message,ans_add_points)

    elif(text == "add_admin" and len(get_user(message.chat.id)) and message.chat.id == admin_id):
        bot.send_message(message.chat.id,"Дашлі мне id новых адмінаў")
        bot.register_next_step_handler(message,ans_new_admin)

    elif(text == "change_agenda" and len(get_user(message.chat.id)) and message.chat.id == admin_id):
        bot.send_message(message.chat.id,"Дашлі мне тэкст раскладу на сёння")
        bot.register_next_step_handler(message,ans_admin)
    
    elif(text == "change_quest" and len(get_user(message.chat.id)) and message.chat.id == admin_id):
        bot.send_message(message.chat.id,"Дашлі мне тэкст квестаў на сёння")
        bot.register_next_step_handler(message,ans_quest)

    elif(text == "send_all" and len(get_user(message.chat.id)) and message.chat.id == admin_id):
        bot.send_message(message.chat.id,"Які тэкст Вы жадаеце даслаць усім?")
        bot.register_next_step_handler(message,ans_send_all)

    elif(text == "get_kboard" and len(get_user(message.chat.id)) and (message.chat.id == admin_id or get_user(message.chat.id)[6] == 1)):
        bot.send_message(message.chat.id,"Вы атрымалі новую клавіятуру", reply_markup=kboard_admin)

    elif(text == "work_with_quest" and len(get_user(message.chat.id)) and (message.chat.id == admin_id or get_user(message.chat.id)[6] == 1)):
        bot.send_message(message.chat.id, "Не апрацованых адказаў: " + str(len(get_quest_answer())))
        if len(get_quest_answer()):
            ans = get_quest_answer()[0]
            bot.send_message(message.chat.id,"Адказ ад: " + str(ans[5]) + "\n" +  "id:" + str(ans[0]) +  "\n" + "Атрыманы: " + str(ans[4]))
            bot.send_message(message.chat.id,"BEGIN")
            try:
                for i in range(ans[2],ans[3]):
                    try:
                        bot.forward_message(message.chat.id, ans[1], i)
                        time.sleep(0.1)
                    except:
                        pass 
                        # КОСТЫЛЬ !!!
                        # print("Trouble")
            except:
                bot.send_message(admin_id,"Адказ быў выдалены")
                bot.send_message(message.chat.id,"Адказ быў выдалены")

            bot.send_message(message.chat.id,"END")
            bot.send_message(message.chat.id,"Вы праверылі гэтую працу?(y/n)" + "\n"+"НЕ ЗАБУДЗЬЦЕСЯ ДАДАЦЬ БАЛЫ!!!" + "\n" + "id = " + str(ans[0]))
            bot.register_next_step_handler(message,admin_check_quest,ans[0],ans[2])
        else:
            bot.send_message(message.chat.id,"Няма адказаў на квесты")


    elif(text[0:7] == 'message' and len(get_user(message.chat.id)) and message.chat.id == admin_id):
        try :
            text_list = text.split()
            bot.forward_message(admin_id,int(text_list[1]) ,int(text_list[2]) )         # time.sleep(0.05)
        except:
            bot.send_message(message.chat.id,"Немагчыма атрымаць гэтае паведамленне")
    elif(text == "get_data" and len(get_user(message.chat.id)) and message.chat.id == admin_id):
        users = get_users()
        result = "Спіс людзей:" + "\n"*3
        for i in range(len(users)):
            result+= str(users[i]) + "\n"*2
        bot.send_message(admin_id,result)

    elif (text == "get_answers" and len(get_user(message.chat.id)) and message.chat.id == admin_id):
        users = get_answers()
        result = "Спіс адказаў:" + "\n"*3
        for i in range(len(users)):
            result+= str(users[i]) + "\n"*2
        bot.send_message(admin_id,result)
    else:
        if(message.chat.id == admin_id):
            bot.send_message(message.chat.id,"Вашае паведамленне не з'яўляецца камандай. Напішыце /start, каб пачаць зноў", reply_markup=kboard_admin)
        elif len(get_user(message.chat.id)):
            bot.send_message(message.chat.id,"Вашае паведамленне не з'яўляецца камандай. Напішыце /start, каб пачаць зноў", reply_markup=kboard_auth)
        else:
            bot.send_message(message.chat.id,"Вашае паведамленне не з'яўляецца камандай. Напішыце /start, каб пачаць зноў", reply_markup=kboard)



def quest_photo(message,start_id):
    # print(jsonpickle.encode(message))

    if message.content_type == "text" and message.text == "Я даслаў/ла ўсе фотаздымкі":
        bot.send_message(message.chat.id,"Вы даслалі ўсе фотаздымкі", reply_markup=kboard_auth)
        bot.send_message(admin_id,str(message.chat.id) + " даслаў адказ на тэст/квест")
        add_answer(get_user(message.chat.id)[0],message.chat.id,start_id+1,message.id,str(time.ctime()),get_user(message.chat.id)[3] )
    elif message.content_type == "photo":
        bot.send_message(message.chat.id,"Ваш фотаздымак прыняты",reply_markup=kboard_photo)
        bot.register_next_step_handler(message,quest_photo,start_id)
    elif message.content_type == "text" and message.text == "Скасаваць дасыланне фотаздымкаў":
        bot.send_message(message.chat.id,"Дасыл фотаздымкаў скасованы",reply_markup=kboard_auth)
    else:
        bot.send_message(message.chat.id,"Вы даслалі не фота",reply_markup=kboard_photo)
        bot.register_next_step_handler(message,quest_photo,start_id)



@bot.callback_query_handler(func=lambda call:True)
def callback_worker(call):
    if call.data == "get_answer_from_user":
        try:
            bot.send_message(call.message.chat.id,"Вы знаходзіцеся ў рэжыме дасылання вынікаў тэста/квеста/іншага. Дасылайце фотаздымкі з вынікамі, калі скончыце, націсніце на кнопку ніжэй(квадрацік)", reply_markup=kboard_photo)
            bot.register_next_step_handler(call.message,quest_photo, call.message.id)
            # print(call.message.id)
        except:
            bot.send_message(call.message.chat.id,"Дашліце яшчэ раз, на жаль, штосьці пайшло не так(")




bot.polling()