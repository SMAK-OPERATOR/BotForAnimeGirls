from datetime import datetime
import telebot  # pyTelegramBotAPI 4.3.1
import mysql.connector
import re
from mysql.connector import connect, Error

def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text
    if not cur_user.isAdmin:
        bot.send_message(chat_id, text="У вас нет прав для работы с бд")
    else:
        if ms_text == "Пользователи":
            userstoout = get_last_users()
            for user in userstoout:
                usersmenu = telebot.types.InlineKeyboardMarkup()
                # bot.send_message(message.chat.id, user.__str__())
                usersmenu.add(telebot.types.InlineKeyboardButton(text="Сообщения пользователя " + str(user.id), callback_data=str(user.id)))
                bot.send_message(message.chat.id, text=user.__str__(), reply_markup=usersmenu)
            # bot.send_message(chat_id, text="Последние пользователи: \n" + get_last_users())
        # elif ms_text == "Сообщения":
        #     input_user(bot, chat_id)





# def input_user(bot, chat_id):
#     ResponseHandler = lambda message: bot.send_message(chat_id, get_user_messages(message.text))
#     my_input(bot, chat_id, "Введите id пользователя", ResponseHandler)
#
#
# # -----------------------------------------------------------------------
# def my_input(bot, chat_id, txt, ResponseHandler):
#     message = bot.send_message(chat_id, text=txt)
#     bot.register_next_step_handler(message,ResponseHandler)


def message_into_db(user, message):

    try:
        with connect(
                host="localhost",
                user="root",
                password="qweasdzxc123",
                database="telebot",
        ) as connection:
            with connection.cursor() as cursor:
                select_query = f"SELECT * FROM users WHERE id = {user.id}"
                cursor.execute(select_query)
                result = cursor.fetchall()
                if not result:
                    try:
                        query = f"UPDATE users SET last_message = \"{datetime.now()}\""
                        cursor.execute(query)
                        query = f"INSERT INTO users (id, first_name, last_name, last_message) VALUES (%s,%s,%s,%s)"
                        queryvalues = (user.id, str(user.firstName), str(user.userName), str(datetime.now()))
                        with connection.cursor() as cursor2:
                            cursor2.execute(query, queryvalues)
                            connection.commit()
                    except Error as e:
                        print(e)
                        print("User creation error")
                    else:
                        print(f"User created successfully")


            with connection.cursor() as cursor:
                try:
                    query = f"INSERT INTO messages (id_user, message, date) VALUES ({user.id},\"{message}\",\"{datetime.now()}\")"
                    cursor.execute(query)
                    connection.commit()
                except Error as e:
                    print(e)
                    print("Message insert error")
                else:
                    print(f"{message} from {user.firstName} {user.userName} // Inserted successfully")
                try:
                    query = f"UPDATE users SET last_message = \"{datetime.now()}\" where id = {user.id}"
                    cursor.execute(query)
                    connection.commit()
                except Error as e:
                    print(e)
                    print("User update error")
                else:
                    print(f"User updated successfully")
    except Error as e:
        print(e)
        print("Connection to db error")


def get_last_users():
    try:
        with connect(
                host="localhost",
                user="root",
                password="qweasdzxc123",
                database="telebot",
        ) as connection:
            with connection.cursor() as cursor:
                select_query = "SELECT * FROM users ORDER BY last_message DESC LIMIT 10"
                cursor.execute(select_query)
                result = cursor.fetchall()
                # finalString = "\n"
                userstoout = []
                for user in result:
                    usertoout = UserToOut(user[0],user[1],user[2],user[3])
                    # finalString += usertoout.__str__() + "\n\n"
                    userstoout.append(usertoout)

    except Error as e:
        print(e)
        finalString = "Connection to db error"
    # return finalString
    return userstoout

def get_user_messages(userid):
    try:
        with connect(
                host="localhost",
                user="root",
                password="qweasdzxc123",
                database="telebot",
        ) as connection:
            with connection.cursor() as cursor:
                resultstr = f"Сообщения от пользователя {userid}:\n "
                try:
                    select_query = f"SELECT message FROM messages where id_user = {int(userid)} ORDER BY date DESC LIMIT 10"
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    if not result:
                        resultstr = "Пользователя не существует или у него нет сообщений"
                    else:
                        for message in result:
                            resultstr += message[0] + "\n"
                except ValueError:
                    resultstr = "Ошибка в id пользователя"

    except Error as e:
        print(e)
        resultstr = "Connection to db error"
    return resultstr


class UserToOut:

    def __init__(self, id, first_name,last_name,date):
        self.id = id
        self.firstName = first_name
        self.userName = last_name
        self.date = date.strftime("%m/%d/%Y, %H:%M:%S")

    def __str__(self):
        return f"Name user: {self.firstName} {self.userName} id:{self.id} last message: {self.date}"
