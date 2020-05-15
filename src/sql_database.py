import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        # Для выполнения операторов SQLite3 сначала устанавливается соединение c базой
        # Cоздаeм базу данных в оперативной памяти
        # con = sqlite3.connect(':memory:')
        con = sqlite3.connect('mydatabase.db')
        print("Connection is established: Database is created")
        return con

    except Error:
        print(Error)


def sql_create_table(connect):
    #  Cоздается объект курсора с использованием объекта соединения
    cursor_obj = connect.cursor()
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS employees("
                       "id integer PRIMARY KEY,"
                       "name text,"
                       "salary real,"
                       "department text,"
                       "position text,"
                       "hireDate text)")
    # Метод commit() сохраняет все сделанные изменения
    connect.commit()


def sql_insert(connect, entities):
    cursor_obj = connect.cursor()
    cursor_obj.execute('INSERT OR IGNORE INTO employees('
                       'id,'
                       'name,'
                       'salary,'
                       'department,'
                       'position,'
                       'hireDate) VALUES(?, ?, ?, ?, ?, ?)', entities)
    connect.commit()


def sql_update(connect):
    # Для обновления будем использовать инструкцию UPDATE.
    # Также воспользуемся предикатом WHERE в качестве условия для выбора нужного сотрудника.
    cursor_obj = connect.cursor()
    cursor_obj.execute('UPDATE employees SET name = "Rogers" where id = 2')
    connect.commit()


def sql_select(connect):
    cursor_obj = connect.cursor()
    #  извлекаем данные из БД
    cursor_obj.execute('SELECT * FROM employees')
    # сохраняем данные в переменную
    table = cursor_obj.fetchall()
    return table

if __name__ == "__main__":
    con = sql_connection()
    sql_create_table(con)

    # Вставляем значения
    entities1 = (1, 'John', 700, 'HR', 'Manager', '2017-01-04')
    entities2 = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')
    entities3 = (3, 'Alise', 900, 'IT', 'Tech', '2019-03-07')
    sql_insert(con, entities1)
    sql_insert(con, entities2)
    sql_insert(con, entities3)
    # Изменяем имя Эндрю на Роджерс.
    sql_update(con)
    # Извлекаем данные
    rows = sql_select(con)
    for row in rows:
        print(row)

    # Закрываем соединение с базой
    con.close()
