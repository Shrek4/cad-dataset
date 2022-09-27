import tensorflow as tf
tf.compat.v1.disable_v2_behavior()

import tensorflow_datasets as tfds
# Construct a tf.data.Dataset
# mnist = tfds.load(name="mnist", split=tfds.Split.TRAIN)

# Сохраните библиотеки, необходимые для модели
from tensorflow.python.framework.graph_util import convert_variables_to_constants
from tensorflow.python.framework import graph_util
# Импорт других библиотек
import cv2
import numpy as np

# Получить данные MINIST
mnist = tf.keras.datasets.mnist.load_data()[0]

# Создать разговор
sess = tf.compat.v1.InteractiveSession()
# Заполнитель
x = tf.compat.v1.placeholder("float", shape=[None, 784], name="Mul")
y_ = tf.compat.v1.placeholder("float", shape=[None, 10], name="y_")
# Переменная
W = tf.Variable(tf.zeros([784, 10]), name='x')
b = tf.Variable(tf.zeros([10]), 'y_')

# Веса
def weight_variable(shape):
    initial = tf.compat.v1.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

# Отклонение
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# Свертка
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

# Максимальный пул
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# Создание связанных переменных
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
x_image = tf.reshape(x, [-1, 28, 28, 1])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
# Функция активации
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
keep_prob = tf.compat.v1.placeholder("float", name='rob')
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
# Softmax функция для обучения
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2, name='res')
# Используется для тестирования функции softmax после тренировки
y_conv2 = tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2, name="final_result")
# Расчет перекрестной энтропии возвращает Тензор, содержащий значение потерь.
cross_entropy = -tf.reduce_sum(y_ * tf.compat.v1.log(y_conv))
# Оптимизатор, отвечающий за минимизацию кросс-энтропии
train_step = tf.compat.v1.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
# Расчет точности
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
# Инициализировать все переменные
sess.run(tf.compat.v1.global_variables_initializer())
# Сохранить ввод и вывод, можно использовать позже
tf.compat.v1.add_to_collection('res', y_conv)
tf.compat.v1.add_to_collection('output', y_conv2)
tf.compat.v1.add_to_collection('x', x)
# Начало обучения
for i in range(10000):
    batch = mnist.train.next_batch(100)
    if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accuracy %g" % (i, train_accuracy))
        # run () можно рассматривать как заполнитель для ввода соответствующего значения в функцию, а затем для вычисления результата, здесь batch [0], xbatch [1] - y_
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
# Установить текущее изображение как изображение по умолчанию
graph_def = tf.get_default_graph().as_graph_def()
# Преобразуйте указанную выше переменную в константу, необходимо сохранить модель как модель pb. Обратите внимание, что здесь final_result имеет то же имя, что и предыдущий y_con2, и только тогда он будет сохранен, в противном случае будет сообщено об ошибке,
# Если вам нужно сохранить другой тензор, просто сохраните его имя и оставьте здесь
output_graph_def = tf.graph_util.convert_variables_to_constants(sess, graph_def, ['final_result'])
# Сохранить модель с заставкой
saver = tf.train.Saver()
saver.save(sess, "model/model")