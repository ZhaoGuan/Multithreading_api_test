# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import sqlite3


def create_table():
    conn = sqlite3.connect('./tag_list.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE tag_list
               (DATA TEXT   NOT NULL,
               CHECKVALUE TEXT    NOT NULL);''')
    print('HTTP_DATA created!!!!')
    conn.commit()
    conn.close()


def instet_table(data, check_value):
    conn = sqlite3.connect('./tag_list.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO tag_list (DATA,CHECKVALUE) VALUES (?,?)", (str(data), str(check_value)))
    # print('instet_table!!!!')
    conn.commit()
    conn.close()


def reader_table():
    conn = sqlite3.connect('./tag_list.db', check_same_thread=False)
    all_data_respone = []
    cursor = conn.execute("SELECT DATA,CHECKVALUE from tag_list")
    for row in cursor:
        data = row[0]
        check_value = row[1]
        all_data_respone.append({'data': data, 'check_value': check_value})
    conn.commit()
    conn.close()
    return all_data_respone


def delete_table():
    conn = sqlite3.connect('./tag_list.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("DROP TABLE tag_list")
    print('HTTP_DATA delete!!!!')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    print(reader_table())
