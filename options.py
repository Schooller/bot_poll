from random import choice
import sqlite3
import pandas as pd

TELEGRAM_TOKEN = '696629284:AAGejq46isCFK3vL2FertLrQzJq-3SMRjYM'
MAIN_URL = 'https://telegra.ph/Golosovanie-za-Prezidenta-i-Vice-prezidenta-parlamenta-RL-2019-11-26'


def get_keys(value: int):
    array = []
    for i in range(value):
        test = True
        new_key = ''.join(choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(3))+'-'+''.join(choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(3))
        for key in array:
            if new_key==key:
                i-=1
                test = False
                break
        if test:
            array.append(new_key)
    return array    


def newDB():
    df = pd.read_csv('names.csv', sep=',')
    array = get_keys(len(df['value']))
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.executescript("""
        BEGIN TRANSACTION;
			CREATE TABLE "user" (
				`id`    INTEGER PRIMARY KEY AUTOINCREMENT,
                `name`    TEXT,
                `class`    TEXT,
                `gender`    TEXT,
				`key`    TEXT,
                `tg_id`    TEXT,
                `president_poll`    TEXT,
                `vice_president_poll`    TEXT
			);
            
			COMMIT;
    """)
    conn.commit()
    for i in range(len(array)):
        cursor.execute("INSERT INTO user  (name, class, gender, key, tg_id, president_poll, vice_president_poll) VALUES(('" + df['name'][i].replace("'","`") + "'), ('" + df['class'][i] + "'), ('" + df['gender'][i] + "'), ('" + array[i] + "'), '0', 'Воздержаться', 'Воздержаться');")
        conn.commit()
    conn.close()
    

def set_candidates():
    array = {'type': ['president','president','vice-president','vice-president','vice-president','vice-president'],
             'name': ['Щур Александр', 'Семен Моргеншерн', 'Шиндер 	Михаил', 'Генч Дениз', 'Гуренко Анастасия', 'Олареско Никита'],
            }
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.executescript("""
        BEGIN TRANSACTION;
			CREATE TABLE "candidates" (
				`id`    INTEGER PRIMARY KEY AUTOINCREMENT,
                `type`    TEXT,
                `name`    TEXT
			);
            
			COMMIT;
    """)
    for i in range(len(array['name'])):
        cursor.execute("INSERT INTO candidates  (type, name) VALUES(('"+array['type'][i]+"'),('"+array['name'][i]+"'))")
        conn.commit()
    conn.commit()
    conn.close()


def set_admins():
    array = [395809791, 332888133, 410596608]
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.executescript("""
        BEGIN TRANSACTION;
			CREATE TABLE "admins" (
				`id`    INTEGER PRIMARY KEY AUTOINCREMENT,
                `type`    TEXT
			);
            
			COMMIT;
    """)
    for key in array:
        cursor.execute("INSERT INTO admins  (type) VALUES('"+str(key)+"')")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    #start options
    newDB()
    set_admins()
    set_candidates()