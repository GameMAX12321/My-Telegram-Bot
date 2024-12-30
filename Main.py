from datetime import datetime
import random
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot("NO")

# Global variable
lidername = None
money = None
dilerCards = {}
yourCards = {}
dilerPoints = {}
yourPoints = {}
deposit = {}
inGame = []
start = {}
last_time1 = {}
last_time2 = {}
last_time3 = {}
last_time4 = {}
last_time5 = {}

# Basic comands
def starting():
    conn = sqlite3.connect("liders.sql")
    cur = conn.cursor()
	
    cur.execute("CREATE TABLE IF NOT EXISTS liders (id int primary key, name varchar(50), user_id int, reputation int, money int, bank int, allmoney int)")
    
    conn.commit()
    cur.close()
    conn.close()

starting()

@bot.callback_query_handler(func = lambda callback: True)
def callbacks(callback):
    global dilerCards
    global yourCards
    global deposit
    global dilerPoints
    global yourPoints
    global start
    user_id = callback.from_user.id
    if callback.data == "thanks":
        bot.answer_callback_query(callback_query_id = callback.id, text = "Спасибо")
    elif callback.data == "takecard" and callback.from_user.id == user_id:
        try:
            dilerCards[user_id] += CreateCards()
        except KeyError:
            dilerCards[user_id] = CreateCards()
        try:
            yourCards[user_id] += CreateCards()
        except KeyError:
            yourCards[user_id] = CreateCards()
        dilerCards1 = dilerCards[user_id][::-1]
        yourCards1 = yourCards[user_id][::-1]
        if dilerCards1[1] == "2":
            dilerPoints[user_id] += 2
        elif dilerCards1[1] == "3":
            dilerPoints[user_id] += 3
        elif dilerCards1[1] == "4":
            dilerPoints[user_id] += 4
        elif dilerCards1[1] == "5":
            dilerPoints[user_id] += 5
        elif dilerCards1[1] == "6":
            dilerPoints[user_id] += 6
        elif dilerCards1[1] == "7":
            dilerPoints[user_id] += 7
        elif dilerCards1[1] == "8":
            dilerPoints[user_id] += 8
        elif dilerCards1[1] == "9":
            dilerPoints[user_id] += 9
        elif dilerCards1[1] == "10":
            dilerPoints[user_id] += 10
        elif dilerCards1[1] == "J":
            dilerPoints[user_id] += 10
        elif dilerCards1[1] == "Q":
            dilerPoints[user_id] += 10
        elif dilerCards1[1] == "K":
            dilerPoints[user_id] += 10
        elif dilerCards1[1] == "A":
            dilerPoints[user_id] += 11
        if yourCards1[1] == "2":
            yourPoints[user_id] += 2
        elif yourCards1[1] == "3":
            yourPoints[user_id] += 3
        elif yourCards1[1] == "4":
            yourPoints[user_id] += 4
        elif yourCards1[1] == "5":
            yourPoints[user_id] += 5
        elif yourCards1[1] == "6":
            yourPoints[user_id] += 6
        elif yourCards1[1] == "7":
            yourPoints[user_id] += 7
        elif yourCards1[1] == "8":
            yourPoints[user_id] += 8
        elif yourCards1[1] == "9":
            yourPoints[user_id] += 9
        elif yourCards1[1] == "10":
            yourPoints[user_id] += 10
        elif yourCards1[1] == "J":
            yourPoints[user_id] += 10
        elif yourCards1[1] == "Q":
            yourPoints[user_id] += 10
        elif yourCards1[1] == "K":
            yourPoints[user_id] += 10
        elif yourCards1[1] == "A":
            yourPoints[user_id] += 11
        info = f"Карты дилера: Неизвесты\n"
        info += f"\nТвои очки: {yourPoints[user_id]}\nТвои карты:\n"
        for el in yourCards[user_id]:
            sim = str(el)
            info += f"{sim} "
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Взять карту", callback_data = "takecard"))
        markup.add(types.InlineKeyboardButton("Закончить игру", callback_data = "stopgame"))  
        bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = info, reply_markup = markup)
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()

        cur.execute("SELECT money, allmoney FROM liders WHERE user_id = ?", (user_id,))
        result = cur.fetchone()

        if start[user_id] == 0:
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] - deposit[user_id], result[1] - deposit[user_id], user_id))
            conn.commit()
            start[user_id] = 1
        else:
            pass
        
        if yourPoints[user_id] < 21 and dilerPoints[user_id] < 21:
            pass
        elif yourPoints[user_id] > 21:
            bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = f"Ты проиграл: {deposit[user_id]}💸")
            inGame.remove(user_id)
        elif dilerPoints[user_id] > 21:
            bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = f"Ты выиграл: {deposit[user_id] * 2}💸")
            inGame.remove(user_id)
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + deposit[user_id] * 2, result[1] + deposit[user_id] * 2, user_id))
            
            conn.commit()
        elif yourPoints[user_id] == 21 and dilerPoints[user_id] == 21:
            bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = "Ничья")
            inGame.remove(user_id)
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + deposit[user_id], result[1] + deposit[user_id], user_id))
            
            conn.commit()
        elif yourPoints[user_id] == 21:
            bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = f"Ты выиграл: {deposit[user_id] * 2}💸")
            inGame.remove(user_id)
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + deposit[user_id] * 2, result[1] + deposit[user_id] * 2, user_id))
            
            conn.commit()
        elif dilerPoints[user_id] == 21:
            bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = f"Ты проиграл: {deposit[user_id]}💸")
            inGame.remove(user_id)
        cur.close()
        conn.close()
    elif callback.data == "stopgame" and callback.from_user.id == user_id:
        info = f"Очки Дилеррра: {dilerPoints[user_id]}\nКарты дилера:\n"
        for el in dilerCards[user_id]:
            sim = str(el)
            info += f"{sim} "
        info += f"\nТвои очки: {yourPoints[user_id]}\nТвои карты:\n"
        for el in yourCards[user_id]:
            sim = str(el)
            info += f"{sim} "
        bot.send_message(callback.message.chat.id, info)
        user_id = callback.from_user.id
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()

        cur.execute("SELECT money, allmoney FROM liders WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        
        if yourPoints[user_id] < dilerPoints[user_id]:
            bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = f"Ты проиграл: {deposit[user_id]}💸")
            inGame.remove(user_id)
        elif yourPoints[user_id] > dilerPoints[user_id]:
            bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = f"Ты выиграл: {deposit[user_id] * 2}💸")
            inGame.remove(user_id)
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + deposit[user_id] * 2, result[1] + deposit[user_id] * 2, user_id))
            conn.commit()
        elif yourPoints[user_id] == dilerPoints[user_id]:
            bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = "Ничья")
            inGame.remove(user_id)
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + deposit[user_id], result[1] + deposit[user_id], user_id))
            
            conn.commit()
        bot.answer_callback_query(callback_query_id = callback.id, text = f"Игра закончилась")
        cur.close()
        conn.close()

@bot.message_handler(commands = ["start"])
def starts(message):	
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Ок, начнём", callback_data = "thanks"))
    bot.reply_to(message, "Начнем работу!", reply_markup = markup)

@bot.message_handler(commands = ["help"])
def help(message):
    command = ["work", "slut", "crime", "liders", "liderboard", "dep", "deposit", "withdraw", "stat", "stats", "rob", "robbing", "give", "givemoney", "give", "givemoney", "add", "addmoney", "roulette", "slots", "slotmachine", "blackjack", "kick", "mute", "unmute"]
    args = message.text.split()[1:]
    try:
        argument = args[0]
    except IndexError:
        argument = None
    if argument is None:
        bot.send_message(message.chat.id, "Все мои команды:\n\nСтартовые команды:\n\n/start - команда старта\n/help - выдает все команды, но если добавить к команде другую команду без знака / то выдаст как использовать команду\n\nЕкономические команды:\n\n/work - способ заработать денег\n/slut - возможно заработать денег или проиграть их\n/crime - возможность выиграть много или проиграть много денег\n/liders или /liderboard - выводит таблицу лидеров в порядке спадания\n/dep или /deposit - ложит деньги в банк не давая их украсть\n/withdraw - позволяет вывести деньги из банка\n/stat или /stats - показывает твою или чужую статистику: деньги, деньги в банке, все деньги\n/rob или /robbing - позволяет украсть деньги у другого\n/give или /givemoney - переводить деньги на счёт другого\n/add или /addmoney - позволяет владельцу выдать себе на счет любую суму денег\n/roulette - ставит ставку на рулетку\n/slots или /slotmacine - позволяет крутить слоты\n/blackjack - позволяет начать игру в блэкджек\n\nАдмин команды:\n\n/kick - удаляет юзера из беседы\n/mute - запрещяет говорить человеку некоторое время\n/unmute - разрешает говорить человеку")
    elif argument in command:
        if argument == "work":
            bot.reply_to(message, "Правильный ввод команды:\n/work\nОписание:\nПозволят раз в 4 часа только заработать деньги, не требует никаких аргументов")
        elif argument == "slut":
            bot.reply_to(message, "Правильный ввод команды:\n/slut\nОписание:\nПозволяет раз в 3 часа заработать или потерять деньги, не требует никаких аргументов")
        elif argument == "crime":
            bot.reply_to(message, "Правильный ввод команды:\n/crime\nОписание:\nПозволяет раз в 5 часов заработать или потерять деньги, не требует никаких аргументов")
        elif argument == "liders" or argument == "liderboard":
            bot.reply_to(message, "Правильный ввод команды:\n/liders или /liderboard\nОписание:\nПозволяет посмотреть таблицу лидеров по мере спадания, не требует никаких аргументов")
        elif argument == "dep" or argument == "deposit":
            bot.reply_to(message, "Правильный ввод команды:\n/dep или /deposit Обязательно(args1)\nОписание:\nПозволяет положить деньги в банк, args1 число не должно быть больше чем твои деньги")
        elif argument == "withdraw":
            bot.reply_to(message, "Правильный ввод команды:\n/withdraw Обязательно(args1)\nОписание:\nПозволяет снять деньги я банка, args1 число не должно быть больше чем твои деньги в банке")
        elif argument == "stat" or argument == "stats":
            bot.reply_to(message, "Правильный ввод команды:\n/stat или /stats Необязательно(args1)\nОписание:\nПозволяет посмотеть твои статы без аргументов и посмотерть чужие если, ты введешь его айди так что args1 число или будет ответом на его сообщение")
        elif argument == "rob" or argument == "robbing":
            bot.reply_to(message, "Правильный ввод команды:\n/rob или /robbing Необязательно(args1)\nОписание:\nПозволяет украсть деньги другого игрока если, ты введешь его айди так что args1 число или будет ответом на его сообщение")
        elif argument == "give" or argument == "givemoney":
            bot.reply_to(message, "Правильный ввод команды:\n/give или /givemoney Необязательно(args1) Обязательно(args2)\nОписание:\nПозволяет отправить деньги на счет другого человека если, ты введешь его айди так что args1 число или будет ответом на его сообщение")
        elif argument == "add" or argument == "addmoney":
            bot.reply_to(message, "Правильный ввод команды:\n/add или /addmoney Обязательно(args1)\nОписание:\nПозволяет добавлять владельцу любую сумму денег, args1 число(НЕ досупна простым смертным)")
        elif argument == "roulette":
            bot.reply_to(message, "Правильный ввод команды:\n/roulette Обязательно(args1, args2)\nОписание:\nПозволяет поставить ставку на рулетку, args1 число это твоя ставка не может быть больше чем твои деньги args2 может быть: black, red, odd, even и числом от 0 до 36")
        elif argument == "slots" or argument == "slotmachine":
            bot.reply_to(message, "Правильный ввод команды:\n/slots или /slotmachine Обязательно(args1)\nОписание:\nПозволяет крутить слоты, args1 число твоя ставка не может быть больше чем твои деньги")
        elif argument == "blackjack":
            bot.reply_to(message, "Правильный ввод команды:\n/blackjack Обязательно(args1)\nОписание:\nПозволяет начать игру в блэкджек, args1 число твоя ставка не может быть больше чем твои деньги")
        elif argument == "kick":
            bot.reply_to(message, "Правильный ввод команды:\n/kick Необязательно(args1)\nОписание:\nПозволяет админу или владельцу кикнуть юзера из беседы, args1 айди юзера которого хотите кикнуть или может быть ответом на сообщение юзера(НЕ доступно простым смертным)")
        elif argument == "mute":
            bot.reply_to(message, "Правильный ввод команды:\n/mute Необязательно(args1) Обязательно(args2)\nОписание:\n Позволяет админу или владельцу заставить молчать неопределлёное время, args1 число айди юзера которго хотите замутить или ответ на сообщение юзера args2 число время на которое хотите замутить до 3 дней")
        elif argument == "unmute":
            bot.reply_to(message, "Правильный ввод команды:\n/unmute Необязательно(args1)\nОписание:\nПозволяет админк или владельцу размутить юзера, args1 число айди юзера которого хотите размутить или ответ на сообщение юзера")
    else:
        bot.reply_to(message, "Нету такой команды")
		
# Economy bot commands
@bot.message_handler(commands=["work"])
def work(message):
    global last_time1
    global lidername
    global money
    user_id = message.from_user.id
    if user_id not in last_time1:
        delta = 14500
    else:
        delta = (datetime.now() - last_time1[user_id]).total_seconds()
    if delta > 14400:
        lidername = message.from_user.id
        user_name = message.from_user.first_name
        money = random.randint(150, 500)
        bot.send_message(message.chat.id, f"Ты заработал: {money}💸")
    
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
    
        cur.execute("SELECT money, bank FROM liders WHERE user_id = ?", (lidername,))
        result = cur.fetchone()
    
        if result:
            new_money = result[0] + money
            bank_money = result[1]
            cur.execute("UPDATE liders SET money = ? WHERE user_id = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE user_id = ?", (new_money + bank_money, lidername))
            cur.execute("UPDATE liders SET name = ? WHERE user_id = ?", (user_name, lidername))
        else:
            cur.execute("INSERT INTO liders (user_id, money, allmoney, name) VALUES (?, ?, ?, ?)", (lidername, money, money, user_name))
    
        conn.commit()
        cur.close()
        conn.close()
        last_time1[user_id] = datetime.now()
    else:
    	bot.reply_to(message, "Еще не прошло 4 часа")
        
@bot.message_handler(commands = ["slut"])
def slut(message):
    global lidername
    global money
    global last_time2
    user_id = message.from_user.id
    if user_id not in last_time2:
    	delta = 11000
    else:
    	delta = (datetime.now() - last_time2[user_id]).total_seconds()
    if delta > 10800:
        chance = random.randint(1, 3)
        lidername = message.from_user.id
        user_name = message.from_user.first_name
        if chance != 3:
            money = random.randint(430, 1000)
            bot.send_message(message.chat.id, f"Ты заработал: {money}💸")
        else:
    	    money = random.randint(0, 150)
    	    bot.send_message(message.chat.id, f"Тебя обокрали на: -{money}💸")
    
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
    
        cur.execute("SELECT money, bank FROM liders WHERE user_id = ?", (lidername,))
        result = cur.fetchone()
    
        if result and chance != 3:
            new_money = result[0] + money
            bank_money = result[1]
            cur.execute("UPDATE liders SET money = ? WHERE user_id = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE user_id = ?", (new_money + bank_money, lidername))
            cur.execute("UPDATE liders SET name = ? WHERE user_id = ?", (user_name, lidername))
        elif result and chance == 3:
            new_money = result[0] - money
            bank_money = result[1]
            cur.execute("UPDATE liders SET money = ? WHERE user_id = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE user_id = ?", (new_money + bank_money, lidername))
            cur.execute("UPDATE liders SET name = ? WHERE user_id = ?", (user_name, lidername))
        elif chance != 3:
            cur.execute("INSERT INTO liders (user_id, money, allmoney, name) VALUES (?, ?, ?, ?)", (lidername, money, money, user_name))
        else:
    	    cur.execute("INSERT INTO liders (user_id, money, allmoney, name) VALUES (?, ?, ?, ?)", (lidername, -money, -money, user_name))
    
        conn.commit()
        cur.close()
        conn.close()
        last_time2[user_id] = datetime.now()
    else:
        bot.reply_to(message, "Еще не прошло 3 часа")
        
@bot.message_handler(commands = ["crime"])
def crime(message):
    global lidername
    global money
    global last_time3
    user_id = message.from_user.id
    if user_id not in last_time3:
    	delta = 18001
    else:
    	delta = (datetime.now() - last_time3[user_id]).total_seconds()
    if delta > 18000:
        chance = random.randint(1, 3)
        lidername = message.from_user.id
        user_name = message.from_user.first_name
        if chance != 3:
            money = random.randint(700, 1300)
            bot.send_message(message.chat.id, f"Ты заработал: {money}💸")
        else:
    	    money = random.randint(0, 400)
    	    bot.send_message(message.chat.id, f"Тебя обокрали на: -{money}💸")
    
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
    
        cur.execute("SELECT money, bank FROM liders WHERE user_id = ?", (lidername,))
        result = cur.fetchone()
    
        if result and chance != 3:
            new_money = result[0] + money
            bank_money = result[1]
            cur.execute("UPDATE liders SET money = ? WHERE user_id = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE user_id = ?", (new_money + bank_money, lidername))
            cur.execute("UPDATE liders SET name = ? WHERE user_id = ?", (user_name, lidername))
        elif result and chance == 3:
            new_money = result[0] - money
            bank_money = result[1]
            cur.execute("UPDATE liders SET money = ? WHERE user_id = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE user_id = ?", (new_money + bank_money, lidername))
            cur.execute("UPDATE liders SET name = ? WHERE user_id = ?", (user_name, lidername))
        elif chance != 3:
            cur.execute("INSERT INTO liders (user_id, money, allmoney, name) VALUES (?, ?, ?, ?)", (lidername, money, money, user_name))
        else:
    	    cur.execute("INSERT INTO liders (user_id, money, allmoney, name) VALUES (?, ?, ?, ?)", (lidername, -money, -money, user_name))
    
        conn.commit()
        cur.close()
        conn.close()
        last_time3[user_id] = datetime.now()
    else:
    	bot.reply_to(message, "Еще не прошло 5 часов")
    
	
@bot.message_handler(commands = ["liders", "liderboard"])
def liderboard(message):
    global lidername
    args = message.text.split()[1:]
    try:
        args[0]
    except IndexError:
        bot.reply_to(message, "Команда должна иметь аргуметы: money или cash - для вывода лидеров по деньгам, rep или reputation - для вывода лидеров по репутации")
        return
    lidername = message.from_user.id
    user_name = message.from_user.first_name
    conn = sqlite3.connect("liders.sql")
    cur = conn.cursor()
    
    cur.execute("UPDATE liders SET name = ? WHERE user_id = ?", (user_name, lidername))
    
    conn.commit()

    if args[0].lower() == "money" or args[0].lower() == "cash":
        cur.execute("SELECT name, allmoney FROM liders ORDER BY allmoney DESC")
        liders = cur.fetchall()
        if not liders:
            bot.send_message(message.chat.id, "Пока нет лидеров по деньгам.")
        else:
            info = "Топ лидеров:\n"
            for idx, el in enumerate(liders, start = 1):
                info += f"{idx}. Имя: {el[0]}, 💸деньги: {el[1]}\n"
            bot.send_message(message.chat.id, info)
    elif args[0].lower() == "rep" or args[0].lower() == "reputation":
        cur.execute("SELECT name, reputation FROM liders ORDER BY reputation DESC")
        liders = cur.fetchall()
        if not liders:
            bot.send_message(message.chat.id, "Пока нет лидеров по репутации.")
        else:
            info = "Топ лидеров:\n"
            for idx, el in enumerate(liders, start = 1):
                info += f"{idx}. Имя: {el[0]}, репутация: {el[1]}\n"
            bot.send_message(message.chat.id, info)
    else:
        bot.reply_to(message, "Нет таких лидеров")
    	
    cur.close()
    conn.close()
    
@bot.message_handler(commands = ["dep", "deposit"])
def dep(message):
    global lidername
    global money
    lidername = message.from_user.id
    args = message.text.split()[1:]
    try:
        depMoney = int(args[0])
    except ValueError:
        bot.reply_to(message, "Введи натуральное число")
        return
    except IndexError:
        bot.reply_to(message, "Введи натуральное число")
        return
    if depMoney < 0:
        bot.reply_to(message, "Число должно быть больше 0")
    else:
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
		
        cur.execute("SELECT money, bank FROM liders WHERE user_id = ?", (lidername,))
        result = cur.fetchone()
        if result[1] is None:
            res = 0
        else:
            res = result[1]
        if result and result[0] > 0 and result[0] >= depMoney:
            cur.execute("UPDATE liders SET money = ? WHERE user_id = ?", (result[0] - depMoney, lidername))
            cur.execute("UPDATE liders SET bank = ? WHERE user_id = ?", (res + depMoney, lidername))
            bot.reply_to(message, f"{message.from_user.first_name} положил в банк {depMoney} денег💰")
        else:
            bot.reply_to(message, "Невозможно положить в банк деньги если их нет🏦")
        conn.commit()
        cur.close()
        conn.close()
    
@bot.message_handler(commands = ["withdraw"])
def withdraw(message):
    global lidername
    global money
    lidername = message.from_user.id
    args = message.text.split()[1:]
    try:
        withMoney = int(args[0])
    except ValueError:
        bot.reply_to(message, "Введи натуральное число")
        return
    except IndexError:
        bot.reply_to(message, "Введи натуральное число")
        return
    if withMoney < 0:
        bot.reply_to(message, "Число должно быть больше 0")
    else:
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
		
        cur.execute("SELECT bank, money FROM liders WHERE user_id = ?", (lidername,))
        result = cur.fetchone()
        if result[0] is None:
            res = 0
        else:
            res = result[0]
        if result and result[0] > 0 and result[0] >= withMoney:
            cur.execute("UPDATE liders SET bank = ? WHERE user_id = ?", (res - withMoney, lidername))
            cur.execute("UPDATE liders SET money = ? WHERE user_id = ?", (result[1] + withMoney, lidername))
            bot.reply_to(message, f"{message.from_user.first_name} снял с банка {withMoney} денег💸")
        else:
            bot.reply_to(message, "Невозможно снять деньги если их нету в банке🏦")
        conn.commit()
        cur.close()
        conn.close()
		
@bot.message_handler(commands=["stats", "stat"])
def stat(message):
    args = message.text.split()[1:]
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id

        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
        
        cur.execute("SELECT name, money, bank, allmoney, reputation FROM liders WHERE user_id = ?", (user_id,))
        result = cur.fetchone()

        if result is None:
            bot.reply_to(message, "Его нет в базе.")
        else:
            bot.reply_to(message, f"Статы {result[0]}:\n💸Деньги: {result[1]}\n🏦Деньги в банке: {result[2]}\n💰Все деньги: {result[3]}\nРепутация: {result[4]}")
        cur.close()
        conn.close()
    elif not args:
        userId = message.from_user.id
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
        
        cur.execute("SELECT name, money, bank, allmoney, reputation FROM liders WHERE user_id = ?", (userId,))
        result = cur.fetchone()
        
        if result is None:
            bot.reply_to(message, "Ваших данных нет в базе.")
        else:
            bot.reply_to(message, f"Твои статы:\nИмя: {result[0]}\n💸Деньги: {result[1]}\n🏦Деньги в банке: {result[2]}\n💰Все деньги: {result[3]}\nРепутация: {result[4]}")
        cur.close()
        conn.close()
    else:
        try:
            user_id = int(args[0])
        except ValueError:
            bot.reply_to(message, "Введи ID пользователя в цифрах")
            return
        except IndexError:
            bot.reply_to(message, "Введи ID пользователя в цифрах")
            return

        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
        
        cur.execute("SELECT name, money, bank, allmoney, reputation FROM liders WHERE user_id = ?", (user_id,))
        result = cur.fetchone()

        if result is None:
            bot.reply_to(message, "Его нет в базе.")
        else:
            bot.reply_to(message, f"Статы {result[0]}:\n💸Деньги: {result[1]}\n🏦Деньги в банке: {result[2]}\n💰Все деньги: {result[3]}\nРепутация: {result[4]}")
        cur.close()
        conn.close()

@bot.message_handler(commands = ["rob", "robbing"])
def rob(message):
    global money
    global last_time4
    args = message.text.split()[1:]
    user_id = message.from_user.id
    if user_id not in last_time4:
    	delta = 43201
    else:
    	delta = (datetime.now() - last_time4[user_id]).total_seconds()
    if delta > 43200:
        user_id = message.from_user.id
        if message.reply_to_message:
            chance = random.randint(1, 3)
            from_user = message.reply_to_message.from_user.id
            if chance != 3:
                conn = sqlite3.connect("liders.sql")
                cur = conn.cursor()

                cur.execute("SELECT money, allmoney, name, user_id FROM liders WHERE user_id = ?", (from_user,))
                result = cur.fetchone()
                cur.execute("SELECT money, allmoney, user_id FROM liders WHERE user_id = ?", (user_id,))
                res = cur.fetchone()

                cur.close()
                conn.close()
                if result is None:
                    bot.reply_to(message, "Его нет в базе🤷")
                    return
                elif res[2] == result[3]:
                    bot.reply_to(message, "Нельзя у самого себя украсть деньги")
                    return
                elif result[0] <= 0:
                    bot.reply_to(message, "У него нет денег")
                else:
                    robMoney = random.randint(1, result[0])
                    conn = sqlite3.connect("liders.sql")
                    cur = conn.cursor()

                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] - robMoney, result[1] - robMoney, from_user))
                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + robMoney, res[1] + robMoney, user_id))

                    conn.commit()
                    cur.close()
                    conn.close()
                    bot.reply_to(message, f"Ты украл у {result[2]}, {robMoney} денег💸")
            else:
                conn = sqlite3.connect("liders.sql")
                cur = conn.cursor()

                cur.execute("SELECT money, allmoney, user_id FROM liders WHERE user_id = ?", (user_id,))
                res = cur.fetchone()
                cur.execute("SELECT money, allmoney, user_id FROM liders WHERE user_id = ?", (from_user,))
                result = cur.fetchone()

                cur.close()
                conn.close()
                if result is None:
                    bot.reply_to(message, "Его нет в базе🤷")
                    return
                elif res[2] == result[2]:
                    bot.reply_to(message, "Нельзя у самого себя украсть деньги")
                    return
                else:
                    robMoney = random.randint(0, 150)
                    conn = sqlite3.connect("liders.sql")
                    cur = conn.cursor()

                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] - robMoney, res[1] - robMoney, user_id))

                    conn.commit()
                    cur.close()
                    conn.close()
                    bot.reply_to(message, f"Тебя споймали твой штраф, {robMoney} денег💸")
        else:
            chance = random.randint(1, 3)
            if chance != 3:
                try:
                    from_user = int(args[0])
                except ValueError:
                    bot.reply_to(message, "Введи ID в цифрах")
                    return
                except IndexError:
                    bot.reply_to(message, "Введи ID в цифрах")
                    return
                conn = sqlite3.connect("liders.sql")
                cur = conn.cursor()

                cur.execute("SELECT money, allmoney, name, user_id FROM liders WHERE user_id = ?", (from_user,))
                result = cur.fetchone()
                cur.execute("SELECT money, allmoney, user_id FROM liders WHERE user_id = ?", (user_id,))
                res = cur.fetchone()

                cur.close()
                conn.close()
                if result is None:
                    bot.reply_to(message, "Его нет в базе🤷")
                    return
                elif res[2] == result[3]:
                    bot.reply_to(message, "Нельзя у самого себя украсть деньги")
                    return
                elif result[0] <= 0:
                    bot.reply_to(message, "У него нет денег")
                    return
                else:
                    robMoney = random.randint(1, result[0])
                    conn = sqlite3.connect("liders.sql")
                    cur = conn.cursor()

                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] - robMoney, result[1] - robMoney, from_user))
                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + robMoney, res[1] + robMoney, user_id))

                    conn.commit()
                    cur.close()
                    conn.close()
                    bot.reply_to(message, f"Ты украл у {result[2]}, {robMoney} денег💸")
            else:
                try:
                    from_user = int(args[0])
                except ValueError:
                    bot.reply_to(message, "Введи ID в цифрах")
                    return
                except IndexError:
                    bot.reply_to(message, "Введи ID в цифрах")
                    return
                conn = sqlite3.connect("liders.sql")
                cur = conn.cursor()

                cur.execute("SELECT money, allmoney, user_id FROM liders WHERE user_id = ?", (user_id,))
                res = cur.fetchone()
                cur.execute("SELECT money, allmoney, user_id FROM liders WHERE user_id = ?", (from_user,))
                result = cur.fetchone()

                cur.close()
                conn.close()
                if result is None:
                    bot.reply_to(message, "Его нет в базе🤷")
                    return
                elif res[2] == result[2]:
                    bot.reply_to(message, "Нельзя у самого себя украсть деньги")
                    return
                else:
                    robMoney = random.randint(0, 150)
                    conn = sqlite3.connect("liders.sql")
                    cur = conn.cursor()

                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] - robMoney, res[1] - robMoney, user_id))

                    conn.commit()
                    cur.close()
                    conn.close()
                    bot.reply_to(message, f"Тебя споймали твой штраф, {robMoney} денег💸")
        last_time4[user_id] = datetime.now()
    else:
    	bot.reply_to(message, "Еще не прошло 12 часов")

@bot.message_handler(commands = ["give", "givemoney"])
def givemoney(message):
    args = message.text.split(" ")
    user_id = message.from_user.id
    try:
        userId = int(args[1])
    except ValueError:
        bot.reply_to(message, "Правильный ввод команды: /give или /givemoney args1(int) или ответ на сообщение того кому хочешь перевести деньги, args2(int > 0) но если ответ то это первый аргумент")
        return
    except IndexError:
        bot.reply_to(message, "Правильный ввод команды: /give или /givemoney args1(int) или ответ на сообщение того кому хочешь перевести деньги, args2(int > 0) но если ответ то это первый аргумент")
        return
    if message.reply_to_message:
        money = int(args[1])
        userID = int(message.reply_to_message.from_user.id)
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()

        cur.execute("SELECT money, allmoney, name, user_id FROM liders WHERE user_id = ?", (userID,))
        result = cur.fetchone()
        cur.execute("SELECT money, allmoney, user_id FROM liders WHERE user_id = ?", (user_id,))
        res = cur.fetchone()

        mon = int(res[0]) - money
        if result is None:
            bot.reply_to(message, "Его нет в базе🤷")
            return
        elif res[2] == result[3]:
            bot.reply_to(message, "Нельзя перевести самому себе деньги")
            return
        if mon < 0:
           bot.reply_to(message, "У тебя не хватает денег")
           conn.commit()
           cur.close()
           conn.close()
           return
        else:
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] - money, res[1] - money, user_id))
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + money, result[1] + money, userID))

        conn.commit()
        cur.close()
        conn.close()
        bot.reply_to(message, f"Ты перевёл {result[2]}, {args[1]} денег💸")
    else:
        try:
            money = int(args[2])
            if money <= 0:
                bot.reply_to(message, "Правильный ввод команды: /give или /givemoney args1(int) или ответ на сообщение того кому хочешь перевести деньги, args2(int > 0) но если ответ то это первый аргумент")
                return
            else:
                pass
        except ValueError:
            bot.reply_to(message, "Правильный ввод команды: /give или /givemoney args1(int) или ответ на сообщение того кому хочешь перевести деньги, args2(int > 0) но если ответ то это первый аргумент")
            return
        except IndexError:
            bot.reply_to(message, "Правильный ввод команды: /give или /givemoney args1(int) или ответ на сообщение того кому хочешь перевести деньги, args2(int > 0) но если ответ то это первый аргумент")
            return
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()

        cur.execute("SELECT money, allmoney, name, user_id FROM liders WHERE user_id = ?", (userId,))
        result = cur.fetchone()
        cur.execute("SELECT money, allmoney, user_id FROM liders WHERE user_id = ?", (user_id,))
        res = cur.fetchone()

        mon = int(res[0]) - money
        if result is None:
            bot.reply_to(message, "Его нет в базе🤷")
            return
        elif res[2] == result[3]:
            bot.reply_to(message, "Нельзя перевести самому себе деньги деньги")
            return
        if mon < 0:
            bot.reply_to(message, "У тебя не хватает денег")
            conn.commit()
            cur.close()
            conn.close()
            return
        else:
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] - money, res[1] - money, user_id))
            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + money, result[1] + money, userId))

        conn.commit()
        cur.close()
        conn.close()
        bot.reply_to(message, f"Ты перевёл {result[2]}, {args[2]} денег💸")

@bot.message_handler(commands = ["add", "addmoney"])
def addmoney(message):
    your_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if your_status == "creator":
        args = message.text.split()[1:]
        try:
            addMoney = int(args[0])
        except ValueError:
            bot.reply_to("Правильный ввод команды: /add /addmoney args1(int)")
            return
        except IndexError:
            bot.reply_to("Правильный ввод команды: /add /addmoney args1(int)")
            return
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()

        cur.execute("SELECT money, allmoney FROM liders WHERE user_id = ?", (message.from_user.id,))
        result = cur.fetchone()

        cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + addMoney, result[1] + addMoney, message.from_user.id))
        bot.reply_to(message, f"Вы добавили себе на баланс {addMoney} денег💸")

        conn.commit()
        cur.close()
        conn.close()
    else:
        bot.reply_to(message, f"У {message.from_user.first_name} нет прав на это😄")

@bot.message_handler(commands = ["roulette"])
def roulette(message):
    global inGame
    roulette = random.randint(0, 36)
    user_id = message.from_user.id
    redNum = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    blackNum = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    oddNum = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
    evenNum = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
    inRoul = ["red", "black", "odd", "even", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"]
    args = message.text.split(" ")
    try:
        dep = int(args[1])
        if dep <= 0:
            bot.reply_to(message, "Правильный ввод команды: /roulette args1(int) args2(black, red, odd, even, number от 0 до 36)")
            return
        else:
            pass
    except ValueError:
        bot.reply_to(message, "Правильный ввод команды: /roulette args1(int) args2(black, red, odd, even, number от 0 до 36)")
        return
    except IndexError:
        bot.reply_to(message, "Правильный ввод команды: /roulette args1(int) args2(black, red, odd, even, number от 0 до 36)")
        return
    try:
        num = int(args[1])
    except ValueError:
        num = args[1]
        return
    except IndexError:
        bot.reply_to(message, "Правильный ввод команды: /roulette args1(int) args2(black, red, odd, even, number от 0 до 36)")
        return
    conn = sqlite3.connect("liders.sql")
    cur = conn.cursor()

    cur.execute("SELECT money, allmoney FROM liders WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if user_id not in inGame:
        if args[2].lower() in inRoul:
            if result[0] >= dep:
                now = int(datetime.now().timestamp())
                waiting = (now + 30)
                bot.reply_to(message, f"Вы поствили на {args[2]}, {args[1]} денег💸\nПодождите 30 секунд.")
                conn = sqlite3.connect("liders.sql")
                cur = conn.cursor()
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] - dep, result[1] - dep, user_id))
                cur.execute("SELECT money, allmoney FROM liders WHERE user_id = ?", (user_id,))
                res = cur.fetchone()
                conn.commit()
                inGame.append(user_id)
                while waiting != int(datetime.now().timestamp()):
                    pass
                if args[2].lower() == "red" and roulette in redNum:
                    win = dep * 2
                        
                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + (dep * 2), res[1] + (dep * 2), user_id))
                    conn.commit()
                    if roulette in redNum:
                        colour = "🟥"
                    else:
                        colour = "⬛"
                    bot.reply_to(message, f"Вы выиграли {win} денег💸\nСтавка была {roulette} {colour}")
                elif args[2].lower() == "black" and roulette in blackNum:
                    win = dep * 2
                        
                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + (dep * 2), res[1] + (dep * 2), user_id))
                    conn.commit()
                    if roulette in redNum:
                        colour = "🟥"
                    else:
                        colour = "⬛"
                    bot.reply_to(message, f"Вы выиграли {win} денег💸\nСтавка была {roulette} {colour}")
                elif args[2].lower() == "odd" and roulette in oddNum:
                    win = dep * 2
                        
                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + (dep * 2), res[1] + (dep * 2), user_id))
                    conn.commit()
                    if roulette in redNum:
                        colour = "🟥"
                    else:
                        colour = "⬛"
                    bot.reply_to(message, f"Вы выиграли {win} денег💸\nСтавка была {roulette} {colour}")
                elif args[2].lower() == "even" and roulette in evenNum:
                    win = dep * 2
                        
                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + (dep * 2), result[1] + (dep * 2), user_id))
                    conn.commit()
                    if roulette in redNum:
                        colour = "🟥"
                    else:
                        colour = "⬛"
                    bot.reply_to(message, f"Вы выиграли {win} денег💸\nСтавка была {roulette} {colour}")
                elif num == roulette:
                    win = dep * 4
                        
                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + (dep * 4), result[1] + (dep * 4), user_id))
                    conn.commit()
                    if roulette in redNum:
                        colour = "🟥"
                    else:
                        colour = "⬛"
                    bot.reply_to(message, f"Вы выиграли {win} денег💸\nСтавка была {roulette} {colour}")
                elif args[2].lower() == "0" and roulette == 0:
                    win = dep * 6
                        
                    cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] + (dep * 6), result[1] + (dep * 6), user_id))
                    conn.commit()
                    bot.reply_to(message, f"Вы выиграли {win} денег💸\nСтавка была {roulette} 🟩")
                else:
                    if roulette in redNum:
                        colour = "🟥"
                    elif roulette in blackNum:
                        colour = "⬛"
                    else:
                        colour = "🟩"
                    bot.send_message(message.chat.id, f"Вы проиграли\nСтавка была {roulette} {colour}")
                cur.close()
                conn.close()
                inGame.remove(user_id)
            else:
                bot.reply_to(message, "Нельзя поставить, ставку выше чем твой баланс")
        else:
            bot.reply_to(message, "Правильный ввод команды: /roulette args1(int > 0) args2(black, red, odd, even, number от 0 до 36)")
    else:
        bot.reply_to(message, "Ты уже поставил на что-то ставку")

@bot.message_handler(commands = ["slots", "slotmachine"])
def slots(message):
    global inGame
    user_id = message.from_user.id
    args = message.text.split()[1:]
    try:
        dep = int(args[0])
        if dep <= 0:
            bot.reply_to(message, "Правильный ввод команды: /slots или /slotmachine arg(int > 0)")
            return
        else:
            pass
    except ValueError:
        bot.reply_to(message, "Правильный ввод команды: /slots или /slotmachine arg(int > 0)")
        return
    except IndexError:
        bot.reply_to(message, "Правильный ввод команды: /slots или /slotmachine arg(int > 0)")
        return
    slotStik = ["💎", "💵", "🍒", "🍊", "7️⃣"]
    oneSlot = random.choice(slotStik)
    twoSlot = random.choice(slotStik)
    threeSlot = random.choice(slotStik)
    conn = sqlite3.connect("liders.sql")
    cur = conn.cursor()

    cur.execute("SELECT money, allmoney FROM liders WHERE user_id = ?", (user_id,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if user_id not in inGame:
        if result[0] >= dep:
            now = int(datetime.now().timestamp())
            waiting = (now + 30)
            conn = sqlite3.connect("liders.sql")
            cur = conn.cursor()

            cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (result[0] - dep, result[1] - dep, user_id))
            cur.execute("SELECT money, allmoney FROM liders WHERE user_id = ?", (user_id,))
            res = cur.fetchone()

            conn.commit()
            bot.reply_to(message, f"Ваша ставка: {dep} денег💸\nПодожди 30 секунд чтобы узнать результат")
            inGame.append(user_id)
            while waiting != int(datetime.now().timestamp()):
                pass
            if oneSlot == twoSlot and twoSlot == threeSlot and threeSlot == "7️⃣":
                win = dep * 6
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + dep * 6, res[1] + dep * 6, user_id))
                conn.commit()
                bot.reply_to(message, f"Тебе выпал джекпот:\n{oneSlot}{twoSlot}{threeSlot}\nТы выиграл: {win} денег💸")
            elif oneSlot == twoSlot and twoSlot == threeSlot and threeSlot == "🍊":
                win = dep * 2
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + dep * 2, res[1] + dep * 2, user_id))
                conn.commit()
                bot.reply_to(message, f"Тебе выпало:\n{oneSlot}{twoSlot}{threeSlot}\nТы выиграл: {win} денег💸")
            elif oneSlot == twoSlot and twoSlot == threeSlot and threeSlot == "🍒":
                win = dep * 2
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + dep * 2, res[1] + dep * 2, user_id))
                conn.commit()
                bot.reply_to(message, f"Тебе выпало:\n{oneSlot}{twoSlot}{threeSlot}\nТы выиграл: {win} денег💸")
            elif oneSlot == twoSlot and twoSlot == threeSlot and threeSlot == "💵":
                win = dep * 2
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + dep * 2, res[1] + dep * 2, user_id))
                conn.commit()
                bot.reply_to(message, f"Тебе выпало:\n{oneSlot}{twoSlot}{threeSlot}\nТы выиграл: {win} денег💸")
            elif oneSlot == twoSlot and twoSlot == threeSlot and threeSlot == "💎":
                win = dep * 3
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + dep * 3, res[1] + dep * 3, user_id))
                conn.commit()
                bot.reply_to(message, f"Тебе выпало:\n{oneSlot}{twoSlot}{threeSlot}\nТы выиграл: {win} денег💸")
            elif oneSlot == twoSlot and twoSlot == "🍊":
                win = round(dep * 1.25, 0)
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + round(dep * 1.25, 0), res[1] + round(dep * 1.25, 0), user_id))
                conn.commit()
                bot.reply_to(message, f"Тебе выпало:\n{oneSlot}{twoSlot}{threeSlot}\nТы выиграл: {win} денег💸")
            elif oneSlot == twoSlot and twoSlot == "🍒":
                win = round(dep * 1.25, 0)
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + round(dep * 1.25, 0), res[1] + round(dep * 1.25, 0), user_id))
                conn.commit()
                bot.reply_to(message, f"Тебе выпало:\n{oneSlot}{twoSlot}{threeSlot}\nТы выиграл: {win} денег💸")
            elif oneSlot == twoSlot and twoSlot == "💵":
                win = round(dep * 1.5, 0)
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + round(dep * 1.5, 0), res[1] + round(dep * 1.5, 0), user_id))
                conn.commit()
                bot.reply_to(message, f"Тебе выпало:\n{oneSlot}{twoSlot}{threeSlot}\nТы выиграл: {win} денег💸")
            elif oneSlot == twoSlot and twoSlot == "💎":
                win = dep * 2
                cur.execute("UPDATE liders SET money = ?, allmoney = ? WHERE user_id = ?", (res[0] + dep * 2, res[1] + dep * 2, user_id))
                conn.commit()
                bot.reply_to(message, f"Тебе выпало:\n{oneSlot}{twoSlot}{threeSlot}\nТы выиграл: {win} денег💸")
            else:
                bot.reply_to(message, f"Тебе выпало:\n{oneSlot}{twoSlot}{threeSlot}\nТы проиграл: {dep} денег💸")
            cur.close()
            conn.close()
            inGame.remove(user_id)
        else:
            bot.reply_to(message, "Нельзя поставить, ставку выше чем твой баланс")
    else:
        bot.reply_to(message, "Ты уже поставил на что-то ставку")

def CreateCards():
    card = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    mast = ["♠", "♥", "♣", "♦"]

    ranCard = random.choice(card)
    ranMast = random.choice(mast)
    return ranCard, ranMast

@bot.message_handler(commands = ["blackjack"])
def blackjack(message):
    global dilerCards
    global dilerPoints
    global yourPoints
    global deposit
    global start
    user_id = message.from_user.id
    args = message.text.split()[1:]
    yourPoints[user_id] = 0
    dilerPoints[user_id] = 0
    start[user_id] = 0
    try:
        dep = int(args[0])
        if dep <= 0:
            bot.reply_to(message, "Правильный ввод команды: /blackjack arg(int > 0)")
            return
        else:
            pass
    except ValueError:
        bot.reply_to(message, "Правильный ввод команды: /blackjack arg(int > 0)")
        return
    except IndexError:
        bot.reply_to(message, "Правильный ввод команды: /blackjack arg(int > 0)")
        return
    
    conn = sqlite3.connect("liders.sql")
    cur = conn.cursor()

    cur.execute("SELECT money, allmoney FROM liders WHERE user_id = ?", (user_id,))
    result = cur.fetchone()

    deposit[user_id] = dep
    if user_id not in inGame:
        if result[0] >= dep:
            dilerCards[user_id] = ()
            yourCards[user_id] = ()
            cur.execute("SELECT money, allmoney FROM liders WHERE user_id = ?", (user_id,))
            res = cur.fetchone()

            conn.commit() 
            inGame.append(user_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Взять карту", callback_data = "takecard"))
            bot.send_message(message.chat.id, "Начать игру?", reply_markup = markup)
        else:
            bot.reply_to(message, "Нельзя поставить, ставку выше чем твой баланс")
    else:
        bot.reply_to(message, "Ты уже поставил на что-то ставку")
    cur.close()
    conn.close()

# Admin comands
@bot.message_handler(commands = ["kick"])
def kick(message):
    your_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if your_status in ["administrator", "creator"]:
        args = message.text.split()[1:]
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, "Невозможно кикнуть админa, гений")
            else:
                bot.kick_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Вы выгнали {message.reply_to_message.from_user.first_name}🔨")
        else:
            chat_id = message.chat.id
            try:
                user_id = args[0]
            except ValueError:
                bot.reply_to(message, "ID должен быть числом")
                return
            except IndexError:
                bot.reply_to(message, "ID должен быть числом")
                return
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, "Невозможно кикнуть админа, гений")
            else:
                conn = sqlite3.connect("liders.sql")
                cur = conn.cursor()

                cur.execute("SELECT name FROM liders WHERE user_id = ?", (user_id,))
                result = cur.fetchone()
            
                cur.close()
                conn.close()
                bot.kick_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Вы выгнали {result[0]}🔨")
    else:
        bot.reply_to(message, f"У {message.from_user.first_name} нет прав на это😄")
		
@bot.message_handler(commands=["mute"])
def mute(message):
    your_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if your_status in ["administrator", "creator"]:
        args = message.text.split(" ")
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, "Невозможно замутить админa, гений")
            else:
                duration = 60
                if args:
                    try:
                        duration = int(args[1])
                    except ValueError:
                        bot.reply_to(message, "Неправильный формат времени.")
                        return
                    except IndexError:
                        bot.reply_to(message, "Неправильный формат времени.")
                        return
                    if duration < 1:
                        bot.reply_to(message, "Время должно быть положительным числом.")
                        return
                    if duration > 4320:
                        bot.reply_to(message, "Максимальное время - 3 дня.")
                        return
                until_date = int(datetime.now().timestamp()) + duration * 60
                bot.restrict_chat_member(chat_id, user_id, until_date=until_date)
                bot.reply_to(message, f"{message.reply_to_message.from_user.first_name} был замучен на {duration} минут.🤐")
        else:
            chat_id = message.chat.id
            try:
                user_id = int(args[1])
            except ValueError:
                bot.reply_to(message, "ID должно быть числом")
                return
            except IndexError:
                bot.reply_to(message, "ID должно быть числом")
                return
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, "Невозможно замутить админa, гений")
            else:
                duration = 60
                if args:
                    try:
                        duration = int(args[2])
                    except ValueError:
                        bot.reply_to(message, "Неправильный формат времени.")
                        return
                    except IndexError:
                        bot.reply_to(message, "Неправильный формат времени.")
                        return
                    if duration < 1:
                        bot.reply_to(message, "Время должно быть положительным числом.")
                        return
                    if duration > 4320:
                        bot.reply_to(message, "Максимальное время - 3 дня.")
                        return
                until_date = int(datetime.now().timestamp()) + duration * 60
                bot.restrict_chat_member(chat_id, user_id, until_date=until_date)
                conn = sqlite3.connect("liders.sql")
                cur = conn.cursor()

                cur.execute("SELECT name FROM liders WHERE user_id = ?", (user_id,))
                result = cur.fetchone()
            
                cur.close()
                conn.close()
                bot.reply_to(message, f"{result[0]} был замучен на {duration} минут.🤐")
    else:
        bot.reply_to(message, f"У {message.from_user.first_name} нет прав на это😄")

@bot.message_handler(commands=["unmute"])
def unmute(message):
    your_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if your_status in ["administrator", "creator"]:
        args = message.text.split()[1:]
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
            bot.reply_to(message, f"{message.reply_to_message.from_user.first_name} был размучен.😮")
        else:
            chat_id = message.chat.id
            try:
                user_id = args[0]
            except ValueError:
                bot.reply_to(message, "ID должно быть числом")
                return
            except IndexError:
                bot.reply_to(message, "ID должно быть числом")
                return
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
            conn = sqlite3.connect("liders.sql")
            cur = conn.cursor()

            cur.execute("SELECT name FROM liders WHERE user_id = ?", (user_id,))
            result = cur.fetchone()
            
            cur.close()
            conn.close()
            bot.reply_to(message, f"{result[0]} был размучен.😮")
    else:
        bot.reply_to(message, f"У {message.from_user.first_name} нет прав на это😄")

#Debug comand
@bot.message_handler(commands = ["self"])
def self(message):
    bot.send_message(message.from_user.id, "bb")

# Chat bot answering. Without commands
@bot.message_handler(content_types = ["text"])
def chating(message):
    global last_time5
    conn = sqlite3.connect("liders.sql")
    cur = conn.cursor()
    if message.text.lower() == "привет" or message.text.lower() == "даров":
        bot.reply_to(message, f"Даров {message.from_user.first_name}")
    elif message.text.lower() == "пока":
        bot.reply_to(message, f"Бб {message.from_user.first_name}")
    elif message.text[0] == "+" and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        your_id = message.from_user.id

        cur.execute("SELECT reputation FROM liders WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        if user_id == your_id:
            bot.reply_to(message, "Нельзя себе добавить репутацию")
            return
        elif result[0] is None:
            cur.execute("UPDATE liders SET reputation = ? WHERE user_id = ?", (0, user_id))
            conn.commit()
        else:
            pass
        cur.execute("SELECT reputation FROM liders WHERE user_id = ?", (user_id,))
        res = cur.fetchone()
        if user_id not in last_time5:
            delta = 14500
        else:
            delta = (datetime.now() - last_time5[user_id]).total_seconds()
        if delta > 14400:
            cur.execute("UPDATE liders SET reputation = ? WHERE user_id = ?", (res[0] + 1, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Репутация оказана {message.reply_to_message.from_user.first_name}")
            last_time5[user_id] = datetime.now()
        else:
            bot.reply_to(message, "Ещё не прошло 4 часа")
    elif message.text[0] == "-" and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        your_id = message.from_user.id

        cur.execute("SELECT reputation FROM liders WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        if user_id == your_id:
            bot.reply_to(message, "Нельзя отнять у себя репутацию")
            return
        elif result[0] is None:
            cur.execute("UPDATE liders SET reputation = ? WHERE user_id = ?", (0, user_id))
            conn.commit()
        else:
            pass
        cur.execute("SELECT reputation FROM liders WHERE user_id = ?", (user_id,))
        res = cur.fetchone()
        if user_id not in last_time5:
            delta = 14500
        else:
            delta = (datetime.now() - last_time5[user_id]).total_seconds()
        if delta > 14400:
            cur.execute("UPDATE liders SET reputation = ? WHERE user_id = ?", (res[0] - 1, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Минус репутация у {message.reply_to_message.from_user.first_name}")
            last_time5[user_id] = datetime.now()
        else:
            bot.reply_to(message, "Ещё не прошло 4 часа")
    cur.close()
    conn.close()
		
@bot.message_handler(content_types = ["photo"])
def get_photo(message):
    if message.from_user.username == "Ashita_No_Joe_2009":
        bot.reply_to(message, "Имба фото😄")
    else:
        bot.reply_to(message, f"Это фото скинул, {message.from_user.first_name}")

bot.infinity_polling()

