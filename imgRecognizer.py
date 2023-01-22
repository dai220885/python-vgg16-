import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from dictForNeuralNetwork import mydict
from tensorflow import keras
from PIL import Image


class ImageRecognizer:
    def __init__(self, incoming_image_path=str(r"d:\small_224_224.jpg"), recognized_image_name='unrecognized image'):
        self.__incoming_image_path = incoming_image_path
        self.__recognized_image_name = recognized_image_name

    def set_incoming_image_path(self, incoming_image_path):
        self.__incoming_image_path = incoming_image_path

    def get_incoming_image_path(self):
        return self.__incoming_image_path

    def set_recognized_image_name(self, recognized_image_name):
        self.__recognized_image_name = recognized_image_name

    def get_recognized_image_name(self):
        return self.__recognized_image_name

    def recognize(self):
        if os.path.isfile(self.__incoming_image_path):
            img = Image.open(self.__incoming_image_path)
            networkmodel = keras.applications.VGG16()
            # приводим к входному формату VGG-сети
            # преобразование изображения в массив numpy:
            img = np.array(img)
            # print(img.shape)

            # далее передаем массив в функцию для преобразования из RGB в BGR формат
            # (со смещениями цветовых компонентов: (B) 103.939 , (G) 116.779, (R) 123.68),
            # для распознавания нейросетью
            tobgr = keras.applications.vgg16.preprocess_input(
                img)  # на выходе получили массив в нужном цветовом формате
            # print(tobgr.shape)  # (224, 224, 3)

            # добавим массиву еще одну пространственную ось, чтобы формат входных данный для модели соответствовал:
            # (размер батча, кол-во строк, кол-во столбцов, кол-во каналов)
            tobgr = np.expand_dims(tobgr, axis=0)
            # print(tobgr.shape)  # (1, 224, 224, 3)

            # пропускаем через сеть
            result = networkmodel.predict(tobgr)
            # print("......:", result.size)  # 1000
            # print(result)
            # print(result.shape)
            # print(np.argmax(result))
            # print(result[0][np.argmax(result)])

            self.__recognized_image_name = mydict[np.argmax(result)]

        else:
            self.__recognized_image_name = 'unrecognized image'
