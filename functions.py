import sqlite3

DATABASE_PATH = 'db.sqlite'


def code_check(text):
    isExists = True
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM user WHERE key=('"+str(text)+"') and tg_id=='0'"
    cursor.execute(sql)
    isExists = (not len(cursor.fetchall()) == 0)
    conn.close()
    if isExists:
        return True
    return False


def user_check(tg_id):
    isNew = True
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = """
        SELECT * FROM user WHERE tg_id=?
    """
    cursor.execute(sql, [(str(tg_id))])
    isNew = (not len(cursor.fetchall()) == 0)
    conn.close()
    if isNew:
        return False
    return True


def key_block(tg_id, text):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "UPDATE user SET tg_id='"+str(tg_id)+"' WHERE key='"+text+"'"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def get_value(text):
    result = []
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM candidates WHERE type='"+text+"'"
    cursor.execute(sql)
    array = cursor.fetchall()
    for name in array:
        result.append(name[2])
    conn.close()
    return result


def admin_check(tg_id):
    isAdmin = True
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = """
        SELECT * FROM admins WHERE type=?
    """
    cursor.execute(sql, [(str(tg_id))])
    isAdmin = (not len(cursor.fetchall()) == 0)
    conn.close()
    if isAdmin:
        return True
    return False


def get_stats():
    arrayf = get_value('president')
    arrays = get_value('vice-president')
    conn = sqlite3.connect(DATABASE_PATH)
    result = {'Президент': [], 'Вице-президент': []}
    for key in arrayf:
        cursor = conn.cursor()
        sql = "SELECT * FROM user WHERE president_poll='"+key+"'"
        cursor.execute(sql)
        result['Президент'].append([(len(cursor.fetchall())), key])
    for key in arrays:
        cursor = conn.cursor()
        sql = "SELECT * FROM user WHERE vice_president_poll='"+key+"'"
        cursor.execute(sql)
        result['Вице-президент'].append([(len(cursor.fetchall())), key])
    conn.close()
    return result


def find_user(text):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM user WHERE id='"+text+"'"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    if len(result) == 0:
        return 'Пользователь не найден.'
    array = result[0]
    S = "Id: "+str(array[0])+"\nИмя: "+array[1]+"\nКласс: "+array[2]+"\nПол: "+array[3]+"\nКлюч: "+array[4]+"\nАйди Телеграмм(0 если код не был активирован): "+array[5]+"\nГолос за президента РЛ: "+array[6]+"\nГолос за вице-президента РЛ: "+array[7]
    return S


def change_user(text):
    try:
        user_id, task, value = map(str, text.split(" "))
    except ValueError:
        return False
    if task=='id' or task=='name' or task=='class' or task=='gender':
        return False
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "UPDATE user SET "+task+"='"+value+"' WHERE id='"+user_id+"'"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return True


def set_answer(text, tg_id):
    value, path = text[:-1], text[-1:]
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    if path=='p':
        sql = "UPDATE user SET president_poll='"+value+"' WHERE tg_id='"+str(tg_id)+"'"
    else:
        sql = "UPDATE user SET vice_president_poll='"+value+"' WHERE tg_id='"+str(tg_id)+"'"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def get_name(tg_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM user WHERE tg_id='"+str(tg_id)+"'"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result[0][1]


def get_max():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM user"
    cursor.execute(sql)
    result = (len(cursor.fetchall()))
    conn.close()
    return str(result)


if __name__ == "__main__":
    pass
