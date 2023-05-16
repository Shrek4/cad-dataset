import cv2
from keras.models import load_model
import numpy as np
from PIL import Image

img_width, img_height=128, 128

model = load_model('cadmnist.h5')

def make_square(img, max_size, fill_color):
    # find image dimensions
    old_img = Image.fromarray(img)
    size = (min(max_size, max(old_img.size)),) * 2

    # resize if old image is larger than max_size
    if size[0] < old_img.size[0] or size[1] < old_img.size[1]:
        old_img.thumbnail(size)

    # create new image with the given color and computed size
    new_img = Image.new(old_img.mode, size, fill_color)

    # find coordinates of upper-left corner to center the old image in the new image
    assert new_img.size[0] >= old_img.size[0]
    assert new_img.size[1] >= old_img.size[1]

    x = (new_img.size[0] - old_img.size[0]) // 2
    y = (new_img.size[1] - old_img.size[1]) // 2

    # paste image
    new_img.paste(old_img, (x, y))

    # save image
    if(max(new_img.size)<img_width):
        new_img=new_img.resize((img_width,img_height))
    return np.array(new_img)

def prepare(img):
    ret, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    padded= np.pad(th, ((5, 5), (5, 5)), "constant", constant_values=0)
    squared=make_square(padded, img_height, 0)
    ret, th = cv2.threshold(squared, 0, 255, cv2.THRESH_OTSU)
    return th

def Recognize_Part(input):

    gray = cv2.cvtColor(input.copy(), cv2.COLOR_BGR2GRAY)

    img=prepare(gray)
    img=img.reshape(1,img_width,img_height,1)
    if(np.any(img)>1): img=img/255.0

    pred = model.predict([img])[0]
    pred_class = np.argmax(pred)
    classes=["Подшипник", "Болт", "Гайка", "Сальник", "Шайба"]

    data = classes[pred_class] + ' ' + str(int(max(pred) * 100)) + '%'

    return data

