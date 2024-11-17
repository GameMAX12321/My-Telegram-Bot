from datetime import datetime
import random
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot("Не скажу))")

# Global variable
lidername = None
money = None
last_time1 = {}
last_time2 = {}
last_time3 = {}

# Basic comands
@bot.callback_query_handler(func = lambda callback: True)
def callbacks(callback):
	if callback.data == "thanks":
		bot.send_message(callback.message.chat.id, "Спасибо")

@bot.message_handler(commands = ["start"])
def start(message):
	conn = sqlite3.connect("liders.sql")
	cur = conn.cursor()
	
	cur.execute("CREATE TABLE IF NOT EXISTS liders (id int primary key,name varchar(50), money int, bank int, allmoney int)")
	conn.commit()
	cur.close()
	conn.close()
	
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton("Ок, начнём", callback_data = "thanks"))
	bot.reply_to(message, "Начнем работу!", reply_markup = markup)
		
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
        lidername = message.from_user.first_name
        money = random.randint(150, 500)
        bot.send_message(message.chat.id, f"Ты заработал: {money}")
    
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
    
        cur.execute("SELECT money FROM liders WHERE name = ?", (lidername,))
        result = cur.fetchone()
    
        if result:
            new_money = result[0] + money
            cur.execute("UPDATE liders SET money = ? WHERE name = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE name = ?", (new_money, lidername))
        else:
            cur.execute("INSERT INTO liders (name, money, allmoney) VALUES (?, ?, ?)", (lidername, money, money))
    
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
        lidername = message.from_user.first_name
        if chance != 3:
            money = random.randint(430, 1000)
            bot.send_message(message.chat.id, f"Ты заработал: {money}")
        else:
    	    money = random.randint(0, 150)
    	    bot.send_message(message.chat.id, f"Тебя обокрали на: -{money}")
    
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
    
        cur.execute("SELECT money FROM liders WHERE name = ?", (lidername,))
        result = cur.fetchone()
    
        if result and chance != 3:
            new_money = result[0] + money
            cur.execute("UPDATE liders SET money = ? WHERE name = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE name = ?", (new_money, lidername))
        elif result and chance == 3:
            new_money = result[0] - money
            cur.execute("UPDATE liders SET money = ? WHERE name = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE name = ?", (new_money, lidername))
        elif chance != 3:
            cur.execute("INSERT INTO liders (name, money, allmoney) VALUES (?, ?, ?)", (lidername, money, money))
        else:
    	    cur.execute("INSERT INTO liders (name, money, allmoney) VALUES (?, ?, ?)", (lidername, -money, -money))
    
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
        lidername = message.from_user.first_name
        if chance != 3:
            money = random.randint(700, 1300)
            bot.send_message(message.chat.id, f"Ты заработал: {money}")
        else:
    	    money = random.randint(0, 400)
    	    bot.send_message(message.chat.id, f"Тебя обокрали на: -{money}")
    
        conn = sqlite3.connect("liders.sql")
        cur = conn.cursor()
    
        cur.execute("SELECT money FROM liders WHERE name = ?", (lidername,))
        result = cur.fetchone()
    
        if result and chance != 3:
            new_money = result[0] + money
            cur.execute("UPDATE liders SET money = ? WHERE name = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE name = ?", (new_money, lidername))
        elif result and chance == 3:
            new_money = result[0] - money
            cur.execute("UPDATE liders SET money = ? WHERE name = ?", (new_money, lidername))
            cur.execute("UPDATE liders SET allmoney = ? WHERE name = ?", (new_money, lidername))
        elif chance != 3:
            cur.execute("INSERT INTO liders (name, money, allmoney) VALUES (?, ?, ?)", (lidername, money, money))
        else:
    	    cur.execute("INSERT INTO liders (name, money, allmoney) VALUES (?, ?, ?)", (lidername, -money, -money))
    
        conn.commit()
        cur.close()
        conn.close()
        last_time3[user_id] = datetime.now()
    else:
    	bot.reply_to(message, "Еще не прошло 5 часов")
    
	
@bot.message_handler(commands = ["liders", "liderboard"])
def liderboard(message):
    conn = sqlite3.connect("liders.sql")
    cur = conn.cursor()
	
    cur.execute("SELECT name, allmoney FROM liders ORDER BY allmoney DESC")
    liders = cur.fetchall()
	
    if not liders:
    	bot.send_message(message.chat.id, "Пока нет лидеров.")
    else:
    	info = "Топ лидеров:\n"
    	for idx, el in enumerate(liders, start = 1):
    		info += f"{idx}. Имя: {el[0]}, деньги: {el[1]}\n"
    	bot.send_message(message.chat.id, info)
    	
    cur.close()
    conn.close()
    
@bot.message_handler(commands = ["dep", "deposit"])
def dep(message):
	global lidername
	global money
	lidername = message.from_user.first_name
	args = message.text.split()[1:]
	try:
	   depMoney = int(args[0])
	except ValueError:
	   bot.reply_to(message, "Введи натуральное число")
	   return
	if depMoney < 1:
		bot.reply_to(message, "Число доджно быть больше 0")
	else:
		conn = sqlite3.connect("liders.sql")
		cur = conn.cursor()
		
		cur.execute("SELECT money FROM liders WHERE name = ?", (lidername,))
		result = cur.fetchone()
		if result != 0:
			cur.execute("UPDATE liders SET money = ? WHERE name = ?", (-depMoney, lidername))
			cur.execute("UPDATE liders SET bank = ? WHERE name = ?", (depMoney, lidername))
			bot.reply_to(message, f"{message.from_user.first_name} положил в банк {depMoney} денег")
		else:
			bot.reply_to(message, "Невозможно положить в банк деньги если их нет")
		conn.commit()
		cur.close()
		conn.close()
    
@bot.message_handler(commands = ["roulette"])
def roulette(message):
	bot.send_message(message.chat.id, "Don't work!!!")
	
# Admin comands
@bot.message_handler(commands = ["kick"])
def kick(message):
	your_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
	if your_status == "administrator" or your_status == "creator":
		if message.reply_to_message:
			chat_id = message.chat.id
			user_id = message.reply_to_message.from_user.id
			user_status = bot.get_chat_member(chat_id, user_id).status
			if user_status == "administrator" or user_status == "creator":
				bot.reply_to(message, "Невозможно кикнуть админа, гений")
			else:
				bot.kick_chat_member(chat_id, user_id)
				bot.reply_to(message, f"Вы выгнали {message.reply_to_message.from_user.first_name}")
		else:
			args = message.text.split()[1:]
			chat_id = message.chat.id
			if args and args[0].isdigit():
			 	user_id = int(args[0])
			 	try:
			 	   user_status = bot.get_chat_member(chat_id, user_id).status
			 	   if user_status in ["administrator", "creator"]:
			 	   	bot.reply_to(message, "Невозможно кикнуть админа, гений")
			 	   else:
			 	       bot.kick_chat_member(chat_id, user_id)
			 	       bot.reply_to(message, f"Вы выгнали пользователя с ID {user_id}")
			 	except Exception as e:
			 		bot.reply_to(message, f"Ошибка: {e}")
			else:
				bot.reply_to(message, "Пожалуйста, укажите корректный ID пользователя.")
	else:
		bot.reply_to(message, f"У {message.from_user.first_name} нет прав на это")
		
@bot.message_handler(commands=["mute"])
def mute(message):
    your_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if your_status in ["administrator", "creator"]:
        chat_id = message.chat.id
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            args = message.text.split()[1:]
            if args and args[0].isdigit():
                user_id = int(args[0])
            else:
                bot.reply_to(message, "Пожалуйста, укажите корректный ID пользователя.")
                return
        
        try:
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status in ["administrator", "creator"]:
                bot.reply_to(message, "Невозможно замутить администратора, гений")
            else:
                duration = 60  # Default duration in minutes
                if len(args) > 1:
                    try:
                        duration = int(args[1])
                        if duration < 1 or duration > 4320:
                            raise ValueError("Время должно быть от 1 до 4320 минут.")
                    except ValueError:
                        bot.reply_to(message, "Введите корректное время (от 1 до 4320 минут).")
                        return
                
                until_date = int(datetime.now().timestamp()) + duration * 60
                bot.restrict_chat_member(chat_id, user_id, until_date=until_date)
                bot.reply_to(
                    message,
                    f"{message.reply_to_message.from_user.first_name if message.reply_to_message else 'Пользователь'} был замучен на {duration} минут."
                )
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")
    else:
        bot.reply_to(message, f"У {message.from_user.first_name} нет прав на это")

@bot.message_handler(commands=["unmute"])
def unmute(message):
    your_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if your_status in ["administrator", "creator"]:
        chat_id = message.chat.id
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            args = message.text.split()[1:]
            if args and args[0].isdigit():
                user_id = int(args[0])
            else:
                bot.reply_to(message, "Пожалуйста, укажите корректный ID пользователя.")
                return
        
        try:
            bot.restrict_chat_member(
                chat_id, user_id,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
            bot.reply_to(
                message,
                f"{message.reply_to_message.from_user.first_name if message.reply_to_message else 'Пользователь'} был размучен."
            )
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")
    else:
        bot.reply_to(message, f"У {message.from_user.first_name} нет прав на это")

# Chat bot answering. Without commands
@bot.message_handler()
def chating(message):
	if message.text.lower() == "привет" or message.text.lower() == "даров":
		bot.reply_to(message, f"Даров {message.from_user.first_name}")
	elif message.text.lower() == "пока":
		bot.reply_to(message, f"Бб {message.from_user.first_name}")
		
@bot.message_handler(content_types = ["photo"])
def get_photo(message):
	if message.from_user.username == "Ashita_No_Joe_2009":
		bot.reply_to(message, "Имба фото")
	else:
		bot.reply_to(message, f"Это фото скинул, {message.from_user.first_name}")

bot.infinity_polling()
