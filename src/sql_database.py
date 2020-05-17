import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        # Для выполнения операторов SQLite3 сначала устанавливается соединение c базой
        # Cоздаeм базу данных в оперативной памяти
        #  By default, check_same_thread is True and only the creating thread may use the connection.
        #  If set False, the returned connection may be shared across multiple threads.
        #  When using multiple threads with the same connection writing operations should be serialized
        #  by the user to avoid data corruption
        con = sqlite3.connect('mydatabase.db', check_same_thread=False)
        print("Connection is established: Database is created")
        return con

    except Error:
        print(Error)


def sql_create_table(connect):
    #  Cоздается объект курсора с использованием объекта соединения
    cursor_obj = connect.cursor()
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS weather("
                       "id integer PRIMARY KEY,"
                       "weather_flag integer)")
    # Метод commit() сохраняет все сделанные изменения
    connect.commit()


def sql_insert(connect, entities):
    cursor_obj = connect.cursor()
    cursor_obj.execute('INSERT OR IGNORE INTO weather('
                       'id,'
                       'weather_flag) VALUES(?, ?)', entities)
    connect.commit()


def sql_update(connect, val, id_for_upd):
    # Для обновления будем использовать инструкцию UPDATE.
    # Также воспользуемся предикатом WHERE в качестве условия для выбора нужного сотрудника.
    cursor_obj = connect.cursor()
    string_for_update = 'UPDATE weather SET weather_flag = ' + str(val) + ' where id = ' + str(id_for_upd)
    print(string_for_update)
    cursor_obj.execute('UPDATE weather SET weather_flag = ' + str(val) + ' where id = ' + str(id_for_upd))
    connect.commit()


def sql_select(connect):
    cursor_obj = connect.cursor()
    #  извлекаем данные из БД
    cursor_obj.execute('SELECT * FROM weather')
    # сохраняем данные в переменную
    table = cursor_obj.fetchall()
    return table


def sql_select_flag(connect, id_for_flag):
    cursor_obj = connect.cursor()
    #  извлекаем данные из БД
    cursor_obj.execute('SELECT weather_flag FROM weather where id = ' + str(id_for_flag))
    # сохраняем данные в переменную
    flag = cursor_obj.fetchall()
    if len(flag) > 0:
        return flag[0][0]
    else:
        return None


if __name__ == "__main__":
    con = sql_connection()
    sql_create_table(con)

    # Вставляем значения
    entities1 = (1, 0)
    entities2 = (2, 0)
    entities3 = (3, 0)
    sql_insert(con, entities1)
    sql_insert(con, entities2)
    sql_insert(con, entities3)
    # Изменяем данные.
    sql_update(con, 1, 2)
    # Извлекаем данные
    rows = sql_select(con)
    for row in rows:
        print(row)

    #
    flag = sql_select_flag(con, 2)
    print(flag)

    # Закрываем соединение с базой
    con.close()
