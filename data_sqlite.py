# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import sqlite3


def create_table():
    conn = sqlite3.connect('./http_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE HTTP_DATA
               (DATA TEXT   NOT NULL,
               RESPONSE TEXT    NOT NULL);''')
    print('HTTP_DATA created!!!!')
    conn.commit()
    conn.close()


def instet_table(data, reponse):
    conn = sqlite3.connect('./http_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO HTTP_DATA (DATA,RESPONSE) VALUES (?,?)", (str(data), str(reponse)))
    # print('instet_table!!!!')
    conn.commit()
    conn.close()


def reader_table():
    conn = sqlite3.connect('./http_data.db', check_same_thread=False)
    all_data_respone = []
    cursor = conn.execute("SELECT data,response from HTTP_DATA")
    for row in cursor:
        data = row[0]
        response = row[1]
        all_data_respone.append({'data': data, 'response': response})
    conn.commit()
    conn.close()
    return all_data_respone


def delete_table():
    conn = sqlite3.connect('./http_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("DROP TABLE HTTP_DATA")
    print('HTTP_DATA delete!!!!')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # create_table()
    # instet_table('asdadadadasdasd', 'dadadasdasdadadadasdassssssssssssssssssssssss')
    # delete_table()
    print(reader_table())
