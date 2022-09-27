import threading
import requests
import argparse
from flask import Flask
import csv
import json

app = Flask(__name__)

parts = []


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


@app.route('/parts')
def get_parts():
    try:
     return getParts()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run()
