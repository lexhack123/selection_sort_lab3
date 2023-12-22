import mysql.connector, random, time, sys, os

# Получаем текущую директорию main.py
current_dir = os.path.dirname(__file__)

# Получаем путь к директории lab2 (родительская директория)
lab2_path = os.path.abspath(os.path.join(current_dir, '..', 'lab2'))
sys.path.append(lab2_path)

from modules.selection_sort import selection_sort


def connect_to_db():
    """
    Функция для установления соединения с базой данных.

    Returns:
        connection: Объект подключения к базе данных.
    """
    return mysql.connector.connect(
        host='localhost',
        user='user',
        password='password',
        database='array_storage'
    )


def add_arrays(num_arrays):
    """
    Функция для добавления массивов в базу данных.

    Args:
        num_arrays (int): Количество массивов, которые нужно добавить в базу данных.
    """
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        start_time = time.time()

        for _ in range(num_arrays):
            # Генерация случайного массива
            array = [random.randint(1, 100)
                     for _ in range(random.randint(5, 15))]
            # Вставка массива в базу данных
            cursor.execute(
                'INSERT INTO unsorted_arrays (array_data) VALUES (%s)', (str(array),))

        conn.commit()
        conn.close()

        execution_time = time.time() - start_time
        print(f'Добавлено {num_arrays} массивов за {execution_time} секунд.')

    except mysql.connector.Error as error:
        print(f'Ошибка при добавлении массивов: {error}')


def fetch_and_sort_arrays(num_arrays):
    """
    Функция для выгрузки и сортировки массивов из базы данных.

    Args:
        num_arrays (int): Количество массивов, которые нужно выгрузить и отсортировать.
    
    Обратите внимание, что может переупорядочивать строки, как показано ниже:
    SELECT * FROM unsorted_arrays;
    | 33300 | [3, 10, 35, 12, 100, 26, 63, 7]                                | 2023-12-10 14:55:47 |
    SELECT * FROM sorted_arrays;
    |33300 | [1, 4, 18, 23, 24, 26, 35, 43, 79, 84, 85, 86, 90, 93, 94]     | 2023-12-10 14:55:49 |
    """
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Получение данных из таблицы unsorted_arrays
        cursor.execute(
            f'SELECT array_data FROM unsorted_arrays ORDER BY RAND() LIMIT {num_arrays}')
        arrays = cursor.fetchall()

        start_time = time.time()

        sorted_arrays = []  # Создаем пустой список для отсортированных массивов

        for array in arrays:
            # Сортировка каждого массива и добавление его в список отсортированных массивов
            sorted_array = selection_sort(eval(array[0]))
            sorted_arrays.append(sorted_array)

        # Запись отсортированных данных в таблицу sorted_arrays
        for sorted_array in sorted_arrays:
            cursor.execute(
                'INSERT INTO sorted_arrays (array_data) VALUES (%s)', (str(sorted_array),))

        conn.commit()

        execution_time = time.time() - start_time
        avg_sorting_time = execution_time / len(arrays)

        print(
            f'Выгружено {num_arrays} массивов из unsorted_arrays, отсортировано и записано в sorted_arrays за {execution_time} секунд.')
        print(
            f'Среднее время сортировки 1 массива: {avg_sorting_time} секунд.')

    except mysql.connector.Error as error:
        print(f'Ошибка при выгрузке и сортировке массивов: {error}')


def clear_database():
    """
    Функция для очистки базы данных от записей.
    """
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        start_time = time.time()
        cursor.execute('DELETE FROM unsorted_arrays')
        cursor.execute('DELETE FROM sorted_arrays')
        conn.commit()
        conn.close()

        execution_time = time.time() - start_time
        print(f'База данных очищена за {execution_time} секунд.')

    except mysql.connector.Error as error:
        print(f'Ошибка при очистке базы данных: {error}')


# Запуск тестов
add_arrays(100)  # Добавление 100 массивов в базу данных
add_arrays(1000)  # Добавление 1000 массивов в базу данных
add_arrays(10000)  # Добавление 10000 массивов в базу данных

# Выгрузка и сортировка 100, 1000 и 10000 случайных массивов из базы данных
fetch_and_sort_arrays(100)
fetch_and_sort_arrays(1000)
fetch_and_sort_arrays(10000)

# Очистка базы данных
clear_database()
