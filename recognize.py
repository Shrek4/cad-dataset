import cv2
from keras.models import load_model
import numpy as np
from PIL import Image


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
    if(max(new_img.size)<150):
        new_img=new_img.resize((150,150))
    return np.array(new_img)

def prepare(img):
    padded= np.pad(img, ((5, 5), (5, 5)), "constant", constant_values=0)
    squared=make_square(padded, 150, 0)
    ret, th = cv2.threshold(squared, 0, 255, cv2.THRESH_OTSU)
    return th

def Recognize_Part(input):

    # image = cv2.imread(FILENAME, cv2.IMREAD_COLOR)
    image=input
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # make a rectangle box around each curve
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)
        
        digit=prepare(th[y:y + h, x:x + w])
        digit=digit.reshape(1,150,150,1)
        digit = digit / 255.0

        pred = model.predict([digit])[0]
        final_pred = np.argmax(pred)
        classes=["bearing", "bolt", "nut", "seal", "washer"]

        data = classes[final_pred] + ' ' + str(int(max(pred) * 100)) + '%'

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        color = (255, 0, 0)
        thickness = 1
        cv2.putText(image, data, (x, y - 5), font, fontScale, color, thickness)


    # cv2.imwrite("output.png", image)
    return image

