from PIL import Image


# класс для изменения размера изображения
class ImageResizer:
    def __init__(self,
                 full_image_path=str(r""),
                 resize_image_path=str(r"d:\small_224_224.jpg"),
                 resized_image_size=(224, 224),  #размер, необходимый для нейросети
                 resized_image_for_showing_path=str(r"d:\small_for_showing.jpg"),
                 resized_image_for_showing_size=(700, 490)  #размер для показа в окне приложения
                 ):
        self.__full_image_path = full_image_path  #путь к исходному изображению для распознавания
        self.__resized_image_path = resize_image_path  #путь к уменьшенному изображению (для нейросети)
        self.__resized_image_size = resized_image_size  #размер, необходимый для нейросети
        self.__resized_image_for_showing_path = resized_image_for_showing_path  #путь к уменьшенному изображению (для показа в окне приложения)
        self.__resized_image_for_showing_size = resized_image_for_showing_size  #размер уменьшенного изображения (для показа в окне приложения)


    def set_full_image_path(self, full_image_path):
        self.__full_image_path = full_image_path

    def get_full_image_path(self):
        return self.__full_image_path

    def set_resized_image_path(self, resized_image_path):
        self.__resized_image_path = resized_image_path

    def get_resized_image_path(self):
        return self.__resized_image_path

    def set_resized_image_size(self, resized_image_size):
        self.__resized_image_size = resized_image_size

    def get_resized_image_size(self):
        return self.__resized_image_size

    def set_resized_image_for_showing_size(self, resized_image_for_showing_size):
        self.__resized_image_for_showing_size = resized_image_for_showing_size

    def get_resized_image_for_showing_size(self):
        return self.__resized_image_for_showing_size

    def set_resized_image_for_showing_path(self, resized_image_for_showing_path):
        self.__resized_image_for_showing_path = resized_image_for_showing_path

    def get_resized_image_for_showing_path(self):
        return self.__resized_image_for_showing_path

    def resize_image_for_recognizing(self):
        original_image = Image.open(self.__full_image_path)
        resized_image = original_image.resize(self.__resized_image_size)
        resized_image.save(self.__resized_image_path)

    def resize_image_for_showing(self):
        original_image = Image.open(self.__full_image_path)
        #'''
        #maxwigth = 500
        maxwigth = self.__resized_image_for_showing_size[0]
        wigth = original_image.size[0]
        height = original_image.size[1]

        #если в оригинале изображения его сторона больше 500 пикселов, то меняем размер:
        if original_image.size[0] > maxwigth:
            wigth = maxwigth
            proportion = float(original_image.size[1] / original_image.size[0])
            height = int(wigth * proportion)
        resized_image = original_image.resize((wigth, height))
        #'''
        #resized_image = original_image.resize()
        #resized_image = original_image.resize(self.__resized_image_size_for_showing)
        resized_image.save(self.__resized_image_for_showing_path)

# if __name__ == '__main__':
#  resize_image(full_image_path='caterpillar.jpg',
#      small_image_path='caterpillar_small.jpg',
#     size=(800, 400))

# resize_image (r"d:\1.jpg", r"d:\222.jpg", (224, 224))
