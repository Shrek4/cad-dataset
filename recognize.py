import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils
import matplotlib.patches as mpatches
from skimage import data, segmentation, measure, morphology, color
import tensorflow as tf


class Number_recognition():
    "" "Инициализация восстановления модели" ""

    def __init__(self, img):
        self.sess = tf.InteractiveSession()
        saver = tf.train.import_meta_graph('model/model.meta')
        saver.restore(self.sess, 'model / model')  # восстановление модели
        # graph = tf.get_default_graph()
        # Получить входной тензор и получить выходной тензор
        self.input_x = self.sess.graph.get_tensor_by_name("Mul:0")
        self.y_conv2 = self.sess.graph.get_tensor_by_name("final_result:0")
        self.Preprocessing(img)  # предварительная обработка изображений
    
    def recognition(self, im):
        im = cv2.resize(im, (28, 28), interpolation=cv2.INTER_CUBIC)
        x_img = np.reshape(im, [-1, 784])
        output = self.sess.run(self.y_conv2, feed_dict={self.input_x: x_img})
        print ('Введенное число:% d'% (np.argmax (output)))
        return np.argmax (output) # вернуть результат распознавания
    
    def Preprocessing(self, image):
        if image.shape[0] > 1000:
            image = imutils.resize (image, height = 800) # Если изображение слишком большое, локальная пороговая скорость сегментации будет немного медленнее, поэтому понижающая дискретизация будет, когда изображение слишком большое
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to gray picture
        m1, n1 = img.shape
        k = int(m1 / 19) + 1
        l = int(n1 / 19) + 1
        #img = cv2.GaussianBlur (img, (3, 3), 0) # фильтр Гаусса
        imm = img.copy()
        # Метод локальной пороговой сегментации на основе Niblack лучше для извлечения сегментации текстового изображения
        for x in range(k):
            for y in range(l):
                s = imm[19 * x:19 * (x + 1), 19 * y:19 * (y + 1)]
                me = s.mean () # среднее
                var = np.std (s) # дисперсия
                t = me * (1 - 0.2 * ((125 - var) / 125))
                ret, imm[19 * x:19 * (x + 1), 19 * y:19 * (y + 1)] = cv2.threshold(imm[19 * x:19 * (x + 1), 19 * y:19 * (y + 1)], t, 255, cv2.THRESH_BINARY_INV)
                label_image = measure.label (imm) # метка подключенной области
                for region in measure.regionprops (label_image): # цикл, чтобы получить набор атрибутов каждой подключенной области
                    # Игнорировать небольшие участки
                    if region.area < 100:
                        continue
                    minr, minc, maxr, maxc = region.bbox # получить параметры прямоугольника аутсорсинга
                    cv2.rectangle (image, (minc, minr), (maxc, maxr), (0, 255, 0), 2) # нарисовать связанные области
        im2 = imm [minr-15: maxr + 15, minc-15: maxc + 15] # Получить интересующую область, то есть площадь каждого числа
        number = self.recognition (im2) # Распознать
        cv2.putText (image, str (number), (minc, minr-10), 0, 2, (0, 0, 255), 2) # Записать результат распознавания на исходном изображении
        cv2.imshow("threshold", imm)
        cv2.imshow("recgonize result", image)
        cv2.waitKey(0)
        
        
if __name__ == '__main__':
    img = cv2.imread("./imgs/1.png")
    x = Number_recognition(img)