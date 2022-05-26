import mysql.connector


def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text
    if not cur_user.isAdmin:
        bot.send_message(chat_id, text="У вас нет прав для работы с бд")
    else:
        if ms_text == "Пользователи":
            bot.send_message(chat_id, text="Последние пользователи: \n" + get_last_users())
        elif ms_text == "Сообщения":
            input_user(bot, message.chat.id)


def input_user(bot, chat_id):
    ResponseHandler = lambda message: bot.send_message(chat_id, message.text)
    my_input(bot, chat_id, "Введите id пользователя", ResponseHandler)


# -----------------------------------------------------------------------
def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(get_user_messages(message.text), ResponseHandler)


def message_into_db(user, message):
    print(user)
    print(message)

    try:
        with connect(
                host="localhost",
                user="username",
                password="password",
                database="db",
        ) as connection:
            with connection.cursor() as cursor:
                select_query = f"SELECT * FROM users WHERE id = {user.id}"
                cursor.execute(select_query)
                result = cursor.fetchall()
                if result == "":
                    query = f"INSERT INTO users (id, first_name, last_name, last_message) VALUES ({user.id},{user.firstName}, {user.userName}, {datetime.datetime.now()})"
                    with connection.cursor() as cursor2:
                        cursor2.execute(query)

            with connection.cursor() as cursor:
                try:
                    query = f"INSERT INTO messages (id_user, message, date) VALUES ({user.id},{message},{datetime.datetime.now()})"
                    cursor.execute(query)
                except Error as e:
                    print(e)
                    print("Message insert error")
                else:
                    print(f"{message} from {user.firstName} {user.userName} // Inserted successfully")
                try:
                    query = f"UPDATE users SET last_message = {datetime.datetime.now()})"
                    cursor.execute(query)
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
                user="username",
                password="password",
                database="db",
        ) as connection:
            with connection.cursor() as cursor:
                select_query = "SELECT * FROM users ORDER BY last_message DESC LIMIT 10"
                cursor.execute(select_query)
                result = cursor.fetchall()
    except Error as e:
        print(e)
        result = "Connection to db error"
    return result


def get_user_messages(userid):
    try:
        with connect(
                host="localhost",
                user="username",
                password="password",
                database="db",
        ) as connection:
            with connection.cursor() as cursor:
                select_query = f"SELECT message FROM messages where id_user = {userid}"
                cursor.execute(select_query)
                result = cursor.fetchall()
                if ursor.fetchall() == "":
                    result = "Пользователя не существует или у него нет сообщений"
                else:
                    result = f"Сообщения от пользователя {userid}:\n" + cursor.fetchall()
    except Error as e:
        print(e)
        result = "Connection to db error"
    return result
