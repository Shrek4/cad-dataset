import cv2
import os
from PIL import Image
import numpy as np
import csv


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
    return np.array(new_img)

def prepare(img):
    # neg=cv2.bitwise_not(img)
    # norm=cv2.normalize(neg, None, -50, 400, norm_type=cv2.NORM_MINMAX)

    gray = img
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cnt=cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][0]
    x, y, w, h = cv2.boundingRect(cnt)
    digit = th[y:y + h, x:x + w]
    # resized_digit = cv2.resize(digit, (90, 90))
    padded= np.pad(digit, ((5, 5), (5, 5)), "constant", constant_values=0)
    # digit = padded_digit.reshape(1, 100, 100, 1)
    # digit = digit / 255.0
    squared=make_square(padded, 100, 0)

    ret, th = cv2.threshold(squared, 0, 255, cv2.THRESH_OTSU)
    return th

def makedataset():
    filelist = []

    for root, dirs, files in os.walk("Images"):
        for file in files:
            filelist.append(os.path.join(root,file))

    for file in filelist:
        im=cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(os.path.join("Images2",file), prepare(im))
        

def getData():
    jsonArray = []
    #read csv file
    with open("Data.csv", encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf, delimiter=";") 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    return jsonArray

def makedataset2():
    data=getData()
    
    for item in data:
        class_ass=None
        if(item[1]=="Болт/Винт"):
            class_ass="bolts"
        elif(item[1]=="Гайка"):
            class_ass="nuts"
        elif(item[1]=="Шайба"):
            class_ass="washers"
        elif(item[1]=="Подшипник"):
            class_ass="bearings"
        cv2.imwrite(os.path.join("cadmnist",class_ass), prepare(im))

makedataset2()