import os
from PyQt5 import QtGui
import design
import shutil
from imgResizer import ImageResizer
from imgRecognizer import ImageRecognizer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QFileDialog, QMessageBox

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

imageresize = ImageResizer()  #экземпляр класса ImageResizer() для последующего изменения размера изображения
imagerecogn = ImageRecognizer()  #экземпляр класса ImageRecognizer() для распознавания изображения

#пишем класс, который наследуется от QMainWindow и от Ui_MainWindow(из нашего design.py)
class MyDiplomaApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # для инициализации нашего дизайна
        self.btn_copy_image_in_corresponding_folder.clicked.connect(self.fnc_move_recognized_image_to_folder)  # обработчик нажатия на кнопку "copy image ..."
        self.btn_recognize_image.clicked.connect(self.fnc_recognize_image)  # обработчик нажатия на кнопку "recognize image"
        self.action_open_image.triggered.connect(self.fnc_open_image)  # обработчик нажатия на пункт меню "open image"
        self.action_save_image_as.triggered.connect(self.fnc_save_image_as)  # обработчик нажатия на пункт меню "save image as"

    # метод для открытия изображения
    def fnc_open_image(self):
        #переменная, в которую запишется путь к изображению (которое потом будем распознавать)
        full_image_path = QFileDialog.getOpenFileName(self, "Open Image", 'd:/',
                                                                'Images (*.png *.xpm *.jpg *.jpeg)')[0]
        if full_image_path:
            # передаем путь к открытому изображению в экземпляр класса ImageResizer()
            imageresize.set_full_image_path(full_image_path)
            #if imageresize.get_full_image_path() != '':
            if os.path.isfile(imageresize.get_full_image_path()):  # проверяем наличие файла
                imageresize.resize_image_for_recognizing()
                imageresize.resize_image_for_showing()
                self.textBrowser.clear()  # очищаем текст-браузер
                #отобразим в textBrowzer изображение, которое будем распознавать:
                document = self.textBrowser.document()
                cursor = QTextCursor(document)
                cursor.insertImage(imageresize.get_resized_image_for_showing_path())
            else:
                QMessageBox.critical(self, "Ошибка ", "ошибка открытия изображения\n"
                                                      "попробуйте повторить", QMessageBox.Ok)

    # метод для кнопки recognize image
    def fnc_recognize_image(self):
        if imageresize.get_full_image_path() != '':
            if os.path.isfile(imageresize.get_resized_image_path()):
                imagerecogn.set_incoming_image_path(imageresize.get_resized_image_path())
                imagerecogn.recognize()
                # выведем название того, что распознала нейросеть
                self.textBrowser.setFont(QtGui.QFont("Times", 14))
                self.textBrowser.append(
                    'recognized image: {}'.format(imagerecogn.get_recognized_image_name()))

            else:
                imagerecogn.set_recognized_image_name('unrecognized image')
                QMessageBox.critical(self, "Ошибка ", "не найдено изображение для распознавания\n"
                                                      " попробуйте открыть изображение еще раз" , QMessageBox.Ok)
        else:
            imagerecogn.set_recognized_image_name('unrecognized image')
            QMessageBox.warning(self, "Внимание", "сначала выберите изображение для распознавания", QMessageBox.Ok)

    # метод для сохранения изображения
    def fnc_save_image_as(self):
        if os.path.isfile(imageresize.get_full_image_path()):  # проверяем наличие файла
            save_as_name = QFileDialog.getSaveFileName(self, 'Save as', r"d:/")
            if save_as_name[0] != '':
                shutil.copy(imageresize.get_full_image_path(), save_as_name[0])
                if os.path.isfile(save_as_name[0]):
                    QMessageBox.information(self, 'сохранение', "изображение успешно сохранено", QMessageBox.Ok)
                else:
                    QMessageBox.critical(self, "Ошибка ", "не удалось сохранить изображение", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Внимание", "выберите изображение для сохранения\n"
                                                  "через menu - open image", QMessageBox.Ok)

    # функция для копирования изображения в папку с именем,
    # соответствующим тому, что изображено на распознанном изображении
    def fnc_move_recognized_image_to_folder(self):
        if imageresize.get_full_image_path() != '':
            file_source = r"d:/"
            folder_to_move_pass = file_source + imagerecogn.get_recognized_image_name()
            file_name = os.path.basename(imageresize.get_full_image_path())  # получаем имя файла из полного пути к нему

            if not os.path.isdir(folder_to_move_pass): # если папки еще не существует, то:
                os.mkdir(folder_to_move_pass)  # создаем папку с именем того, что распознала нейросеть на картинке
            if os.path.isfile(imageresize.get_full_image_path()):  # проверяем наличие файла

                # копирование исходного изображения в папку
                shutil.copy(imageresize.get_full_image_path(), folder_to_move_pass)
                if os.path.isfile(folder_to_move_pass+r"/"+file_name):  # проверяем наличие скопированного файла
                    QMessageBox.information(self, 'копирование', "изображение успешно скопировано", QMessageBox.Ok)
                else:
                    QMessageBox.critical(self, "Ошибка ", "не удалось скопировать изображение", QMessageBox.Ok)

        else:
            QMessageBox.warning(self, "Внимание", "выберите изображение для копирования", QMessageBox.Ok)

