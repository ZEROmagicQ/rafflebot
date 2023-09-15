import sqlite3
import telebot
from telebot import types
import random

class Constants:
    NUMOFWINNERS = 5
    
bot = telebot.TeleBot('token')

    
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT UNIQUE,
                uid INTEGER UNIQUE)''')
conn.commit()

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, Привет!\nДля участия в розыгрыше отправьте ссылку на ваш профиль\n\n")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def link_handler(message):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (link, uid) VALUES (?, ?)", (message.text, message.chat.id))
        conn.commit()
        bot.send_message(message.chat.id, "Link successfully added!")
    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id, "Has this link already been added or are you already in the draw!")
    cursor.close()
    conn.close()

@bot.message_handler(commands=['finish'])
def end_raffle_handler(message):
    if message.chat.id != 1858539793:
        return        
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    winners = []
    for _ in range(5):
        while True:
            _w = random.choice(results)
            if _w not in winners:
                winners.append(_w)
                break
    
    tosend = 'Winnersа:\n'
    for i in range(1, 5+1):
        tosend+=f"\n{i}. {winners[i-1][1]} (telegramid: {winners[i-1][2]})"
    print(tosend)
    bot.send_message(message.chat.id, tosend)
    cursor.close()
    conn.close()

bot.polling(none_stop=True)