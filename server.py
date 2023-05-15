from codecs import unicode_escape_decode, unicode_escape_encode
import threading
import argparse
from flask import Flask, send_from_directory, request
import csv
import json
from flask_cors import CORS
import os
import cv2
from werkzeug.utils import secure_filename

from recognize import Recognize_Part
PORT=3001

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

def getParts():
    jsonArray = []
    #read csv file
    with open("Parts.csv", encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf, delimiter=";") 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    return jsonArray

def getStandarts():
    jsonArray = []
    #read csv file
    with open("Standarts.csv", encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf, delimiter=";") 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    return jsonArray


def getClasses():
    jsonArray = []
    #read csv file
    with open("Classes.csv", encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf, delimiter=";") 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    return jsonArray

def getImCat():
    jsonArray = []
    #read csv file
    with open("Images_categories.csv", encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf, delimiter=";") 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    return jsonArray

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

parts_data=getData()
# parts=getParts()
# classes=getClasses()
# standarts=getStandarts()
# im_categories=getImCat()

# def getClass(class_id):
#     return [x for x in classes if x['id'] == class_id][0]['name']

# def getStandart(standart_id):
#     return [x for x in standarts if x['id'] == standart_id][0]['name']

# def getImages(part_id):
#     cat_id=[x for x in parts if x['id'] == part_id][0]['image_category']
#     cat_name=[x for x in im_categories if x['id'] == cat_id][0]['folder']
#     return [cat_name+'/'+x for x in os.listdir(cat_name)]

@app.route('/parts')
def get_parts():
    # try:
    #     data=[]
    #     for i in range(len(parts)):
    #         data.append({"id": parts[i]['id'], "class": getClass(parts[i]['class_id']), "standart": getStandart(parts[i]['standart_id']), "size": parts[i]['size'], "images": getImages(parts[i]['id'])})
    #     return data
    # except Exception as e:
    #     print(e)
    try:
        data=[]
        for i in range(len(parts_data)):
            cat_name=parts_data[i]['image_dir']
            data.append({"id": parts_data[i]['id'], "class": parts_data[i]['class'], "standart": parts_data[i]['standart'], "size": parts_data[i]['size'], "images": [cat_name+'/'+x for x in os.listdir(cat_name)]})
        return data
    except Exception as e:
        print(e)

@app.route('/Images/<path:path>')
def get_files(path):
    try:
        return send_from_directory("Images", path)
    except Exception as e:
        print(e)

@app.route('/recognize_img/<path:path>')
def get_recognized_img(path):
    try:
        return send_from_directory("recognize_img", path)
    except Exception as e:
        print(e)

@app.route('/upload', methods=['POST'])
def fileUpload():
    file_dir="recognize_img/"
    f = request.files['file']
    f.save(file_dir+"input.png")
    recognized=Recognize_Part(cv2.imread(file_dir+"input.png", cv2.IMREAD_COLOR))
    cv2.imwrite(file_dir+"output.png", recognized)
    return {"url": file_dir+"output.png"}

if __name__ == "__main__":
    app.run(host="localhost", port=PORT)
