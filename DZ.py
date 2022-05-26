def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Ввод имени":
        input_name(bot, chat_id)

    if ms_text == "Ввод возраста":
        input_age(bot, chat_id)

    if ms_text == "Задача":
        task(bot, chat_id)


def input_name(bot, chat_id):
    dz6_ResponseHandler = lambda message: bot.send_message(chat_id,
                                                           f"Добро пожаловать {message.text}! У тебя красивое имя, в нём {len(message.text)} букв!"
                                                           f"{message.text.upper()} ,{message.text.lower()} ,{message.text[::-1].capitalize()} ,{message.text.capitalize()}")

    my_input(bot, chat_id, "Как тебя зовут?", dz6_ResponseHandler)


# -----------------------------------------------------------------------
def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)


# -----------------------------------------------------------------------
def input_age(bot, chat_id):
    my_inputInt(bot, chat_id, "Сколько вам лет?", dz5_ResponseHandler)


def dz5_ResponseHandler(bot, chat_id, age_int):
    bot.send_message(chat_id,
                     text=f"О! тебе уже {age_int}! \nА через год будет уже {age_int + 1}!!!\n" + ageCalc(age_int))


def ageCalc(age):
    i = 0
    summ = 0
    mult = 1
    agestr = str(age)
    while i < len(str(age)):
        summ = summ + int(agestr[i])
        mult = mult * int(agestr[i])
        i += 1
    string = "Сумма твоего возраста " + str(summ) + "\nПроизведение твоего возраста " + str(mult)
    return string


# -----------------------------------------------------------------------
def my_inputInt(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt,
                                   ResponseHandler=ResponseHandler)
    # bot.register_next_step_handler(message, my_inputInt_return, bot, txt, ResponseHandler)  # то-же самое, но короче


def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        var_int = int(message.text)
        # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                                 text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже
        # у нас пара процедур, которые вызывают друг-друга, пока пользователь не введёт корректные данные,
        # и тогда этот цикл прервётся, и управление перейдёт "наружу", в ResponseHandler


# -----------------------------------------------------------------------
def taskLogic(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        var_int = int(message.text)
        # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
        if var_int == 6:
            ResponseHandler(botQuestion, chat_id, "Правильно")
        else:
            ResponseHandler(botQuestion, chat_id, "Неправильно")
    except ValueError:
        botQuestion.send_message(chat_id,
                                 text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        taskInput(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже

        # у нас пара процедур, которые вызывают друг-друга, пока пользователь не введёт корректные данные,
        # и тогда этот цикл прервётся, и управление перейдёт "наружу", в ResponseHandler


def taskInput(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, taskLogic, botQuestion=bot, txtQuestion=txt,
                                   ResponseHandler=taskResponseHandler)


def task(bot, chat_id):
    taskInput(bot, chat_id, "Сколько будет 2+2*2?", taskResponseHandler)


def taskResponseHandler(bot, chat_id, text):
    bot.send_message(chat_id, text=text)
