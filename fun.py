# ======================================= Развлечения
import requests



def exaltExchangeRate():
    import json
    req = requests.get('https://poe.ninja/api/data/currencyoverview?league=Archnemesis&type=Currency')
    Exchange_json = req.json()
    ExaltExchangeInt = None
    for i in Exchange_json["lines"]:
        if "Exalted Orb" in [i['currencyTypeName']]:
            ExaltExchangeInt = i['chaosEquivalent']
            break
    return ExaltExchangeInt


def getRandomAnek():
    from random import randint
    import bs4
    array = []
    anek = requests.get("http://anekdotme.ru/anekdot/random")
    soup = bs4.BeautifulSoup(anek.text, "html.parser")
    result = soup.select(".anekdot_text")
    for finalResult in result:
        array.append(finalResult.getText().strip())
    return array[0]


# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Курс экза":
        bot.send_message(chat_id, text="Экзальт стоит " + str(exaltExchangeRate()) + " хаосов")

    elif ms_text == "Прислать анекдот":
        bot.send_message(chat_id, text=getRandomAnek())



