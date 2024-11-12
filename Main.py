from datetime import datetime
import random
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot("7703654756:AAGuuX6h4XhwNIbkzfoak4CSN_j1WMWKwS8")

lidername = None
money = None
last_time1 = {}
last_time2 = {}
last_time3 = {}

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
	
@bot.message_handler(content_types = ["photo"])
def get_photo(message):
	if message.from_user.username == "Ashita_No_Joe_2009":
		bot.reply_to(message, "Имба фото")
	else:
		bot.reply_to(message, f"Ебать хуйню скинул, {message.from_user.first_name}")
		
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
	
    cur.execute("SELECT * FROM liders")
    liders = cur.fetchall()
	
    info = ""
    for el in liders:
        info += f"Имя: {el[1]}, деньги: {el[4]}\n"
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, info)
    
@bot.message_handler(commands = ["dep", "deposit"])
def dep(message):
    global lidername
    global money
    depMoney = None
    conn = sqlite3.connect("liders.sql")
    cur = conn.cursor()
 
    cur.execute("SELECT money FROM liders WHERE name = ?", (lidername))
    result = cur.fetchone()
    if result != 0:
        cur.execute("UPDATE liders SET money = ? WHERE name = ?" (-depMoney, lidername))
        cur.execute("UPDATE liders SET bank = ? WHERE name = ?" (depMoney, lidername))
    conn.commit()
    cur.close()
    conn.close()
    
@bot.message_handler(commands = ["roulette"])
def roulette(message):
	bot.send_message(message.chat.id, "Don't work!!!")
	
@bot.message_handler()
def chating(message):
	if message.text.lower() == "привет" or message.text.lower() == "даров":
		bot.reply_to(message, f"Даров {message.from_user.first_name}")
	elif message.text.lower() == "пока":
		bot.reply_to(message, f"Бб {message.from_user.first_name}")
	elif message.text.lower() == "да":
		bot.reply_to(message, "Пизда")
	elif message.text.lower() == "нет":
		bot.reply_to(message, "Пидора ответ")

bot.infinity_polling()
