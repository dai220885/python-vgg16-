import sys
from PyQt5.QtWidgets import QApplication
from myDiplomaApp import MyDiplomaApp


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MyDiplomaApp()  # Создаём экземпляр класса MyDiplomaApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
