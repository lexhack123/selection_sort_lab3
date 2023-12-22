import sys
import os
import random
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox

# Получаем текущую директорию main.py
current_dir = os.path.dirname(__file__)

# Получаем путь к директории lab2 (родительская директория)
lab2_path = os.path.abspath(os.path.join(current_dir, '..', 'lab2'))
sys.path.append(lab2_path)

# Импорт функции selection_sort из модуля lab2
from modules.selection_sort import selection_sort


# Функция для соединения с базой данных
def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='user',
        password='password',
        database='array_storage'
    )


# Функция для добавления массива в базу данных
def add_array_to_db(array):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO unsorted_arrays (array_data) VALUES (%s)', (str(array),))
        conn.commit()
        conn.close()
    except mysql.connector.Error as error:
        print(f'Ошибка при добавлении массива: {error}')


# Функция для получения всех массивов из базы данных
def get_arrays_from_db():
    arrays = []
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute('SELECT array_data FROM unsorted_arrays')
        arrays = cursor.fetchall()
        conn.close()
    except mysql.connector.Error as error:
        print(f'Ошибка при получении массивов: {error}')
    return arrays


# Основной класс для приложения
class SortingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Создание основного интерфейса приложения
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Создание элементов управления интерфейса
        self.label = QLabel(
            "Введите/редактируйте массив для сортировки (через запятую):")
        self.array_input = QLineEdit()
        self.save_button = QPushButton("Сохранить в базе данных")
        self.show_arrays_button = QPushButton("Показать массивы из базы")
        self.array_list = QListWidget()
        self.sort_array_button = QPushButton("Сортировать массив")
        self.generate_array_button = QPushButton("Сгенерировать массив")      

        # Добавление элементов управления на основной интерфейс
        layout.addWidget(self.label)
        layout.addWidget(self.array_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.show_arrays_button)
        layout.addWidget(self.array_list)
        layout.addWidget(self.sort_array_button)
        layout.addWidget(self.generate_array_button)

        # Подключение функций к кнопкам
        self.save_button.clicked.connect(self.save_array)
        self.show_arrays_button.clicked.connect(self.show_arrays)
        self.sort_array_button.clicked.connect(self.sort_array)
        self.generate_array_button.clicked.connect(self.generate_array)

        self.setWindowTitle("Sorting App")
        self.setGeometry(100, 100, 400, 400)

    def save_array(self):
        # Получение массива из текстового поля и добавление его в базу данных
        array = self.array_input.text().split(',')
        add_array_to_db(array)
        self.array_input.clear()

    def show_arrays(self):
        # Получение всех массивов из базы данных и отображение их в QListWidget
        arrays = get_arrays_from_db()
        self.array_list.clear()
        for array in arrays:
            self.array_list.addItem(str(array[0]))

    def sort_array(self):
        # Сортировка выбранного массива из QListWidget
        selected_item = self.array_list.currentItem()
        if selected_item:
            # Преобразование строки в массив
            array = eval(selected_item.text())
            sorted_array = selection_sort(array)

            # Создание сообщения с вопросом о сохранении отсортированного массива
            reply = QMessageBox.question(
                self, 'Сохранение в базу данных',
                'Хотите ли Вы сохранить отсортированный массив в базу данных?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            # Обработка выбора пользователя
            if reply == QMessageBox.Yes:
                add_array_to_db(sorted_array)

            # Показ сообщения с отсортированным массивом
            QMessageBox.information(
                self, 'Отсортированный массив', str(sorted_array))
        else:
            QMessageBox.warning(self, 'Предупреждение',
                                'Выберите массив для сортировки')
    
    def generate_array(self):
        # Генерация массива с 10 случайными целочисленными значениями от 1 до 100
        random_array = [random.randint(1, 100) for _ in range(10)]

        # Преобразование сгенерированного массива в строку и отображение его в поле ввода
        self.array_input.setText(','.join(map(str, random_array)))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    sorting_app = SortingApp()
    sorting_app.show()
    sys.exit(app.exec_())
