import json
import os
from shapely.geometry import Polygon
import cv2
import csv


def loadCSV(path):
    readData = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            readData.append(row)
    return readData

def csvGetDates(csvData, toSearch):
    toReturn = [None, None, None]
    for row in csvData:
        for term in row:
            if term == toSearch:
                if row[1] != '':
                    toReturn[0] = row[1]
                if row[2] != '':
                    toReturn[1] = row[2]
                if row[4] != '':
                    toReturn[2] = row[4]
    return toReturn

def writeJson(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def readJson(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def rescale(val, oldMin, oldMax, a, b):
    return a + (((val - oldMin) * (b - a)) / (oldMax - oldMin))

def getCentroid(pointList):
    P = Polygon(pointList)
    cent = P.centroid.coords
    return [cent[0][0], cent[0][1]]

def collectFiles(path, acceptedFormats):

    finalList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            extension = os.path.splitext(file)[1][1:]
            if extension in acceptedFormats:
                finalList.append(os.path.join(root, file))
    return finalList

def save_frame(video_path, frame_num, result_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

    ret, frame = cap.read()

    if ret:
        cv2.imwrite(result_path, frame)