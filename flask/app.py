import sys
sys.path.append('../')

import os
import base64
import json
import cv2
import uuid
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
from time import gmtime, strftime

from engine.header import *

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
root_path = os.path.dirname(dir_path)

MATCH_THRESHOLD = 0.82

app = Flask(__name__)
CORS(app)

print('\t Face SDK Lite version')

def activate_sdk():
    ret = init_sdk()

    if ret == 0:
        print("Successfully init SDK!")
    else:
        print(f"Falied to init SDK, Error code {ret}")

    return ret

@app.route('/api/analyze_face', methods=['POST'])
def analyze_face_api():
    status = "ok"
    data = {
        "status": status, 
        "data": {}
    }

    try:
        file = request.files['image']
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    except:
        data["data"]["result"] = "Failed to open image"   
        response = jsonify(data)
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    ret, face_result = detect_face(image, 1, ENGINE_MODE.M_IDENTIFY.value)
    if ret <= 0:
        if ret == ENGINE_CODE.E_NO_FILE.value:
            result = "NO FILE"
        elif ret == ENGINE_CODE.E_NO_FACE.value:
            result = "NO FACE"
        else:
            result = "ENGINE ERROR"
        
        data["data"]["result"] = result   
        response = jsonify(data)
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    
    data["data"]["result"] = "FACE DETECTED"
    attribute = face_result[0]
    data["data"]["face_rect"] = {
        "x": attribute.x1, 
        "y": attribute.y1, 
        "w": attribute.x2 - attribute.x1 + 1, 
        "h": attribute.y2 - attribute.y1 + 1
    }
    
    
    attr = {}
    if attribute.liveness == LIVENESS_CODE.L_SPOOF.value:
        liveness = "SPOOF"
    elif attribute.liveness == LIVENESS_CODE.L_REAL.value:
        liveness = "REAL"
    elif attribute.liveness == LIVENESS_CODE.L_TOO_SMALL_FACE.value:    
        liveness = "TOO SMALL FACE"
    elif attribute.liveness == LIVENESS_CODE.L_TOO_LARGE_FACE.value:
        liveness = "TOO LARGE FACE"
    elif attribute.liveness == LIVENESS_CODE.L_NO_FACE.value:
        liveness = "NO FACE"
    elif attribute.liveness == LIVENESS_CODE.L_LIVENESS_CHECK_FAILED.value:
        liveness = "Liveness Check Failed"
    else:    
        liveness = "ERROR"

    attr["liveness"] = liveness
    attr["gender"] = "MALE" if attribute.gender == 0 else "FEMALE"
    attr["age"] = str(attribute.age)
    
    attr["wear_glass"] = "NO" if attribute.glass == 0 else "YES"
    attr["mask"] = "YES" if attribute.mask == 1 else "NO"
    data["data"]["attribute"] = attr

    response = jsonify(data)
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

@app.route('/api/compare_face', methods=['POST'])
def compare_face_api():
    status = "ok"
    data = {
        "status": status, 
        "data": {}
    }

    try:
        file1 = request.files['image1']
        image1 = cv2.imdecode(np.frombuffer(file1.read(), np.uint8), cv2.IMREAD_COLOR)
    except:
        data["data"]["result"] = "Failed to open image1"   
        response = jsonify(data)
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    try:
        file2 = request.files['image2']
        image2 = cv2.imdecode(np.frombuffer(file2.read(), np.uint8), cv2.IMREAD_COLOR)
    except:
        data["data"]["result"] = "Failed to open image2"   
        response = jsonify(data)
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    ret, face_result1 = detect_face(image1, 1, ENGINE_MODE.M_ENROLL.value)
    if ret <= 0:
        if ret == ENGINE_CODE.E_NO_FILE.value:
            result = "NO FILE1"
        elif ret == ENGINE_CODE.E_NO_FACE.value:
            result = "NO FACE in image1"
        else:
            result = "ENGINE ERROR"

        data["data"]["result"] = result   
        response = jsonify(data)
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    ret, face_result2 = detect_face(image2, 1, ENGINE_MODE.M_IDENTIFY.value)
    if ret <= 0:
        if ret == ENGINE_CODE.E_NO_FILE.value:
            result = "NO FILE2"
        elif ret == ENGINE_CODE.E_NO_FACE.value:
            result = "NO FACE in image2"
        else:
            result = "ENGINE ERROR"

        data["data"]["result"] = result   
        response = jsonify(data)
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    detection = {}
    detection["face1"] = {
        "x" : face_result1[0].x1,
        "y" : face_result1[0].y1,
        "width" : face_result1[0].x2 - face_result1[0].x1 + 1,
        "height" : face_result1[0].y2 - face_result1[0].y1 + 1
    }

    detection["face2"] = {
        "x" : face_result2[0].x1,
        "y" : face_result2[0].y1,
        "width" : face_result2[0].x2 - face_result2[0].x1 + 1,
        "height" : face_result2[0].y2 - face_result2[0].y1 + 1
    }
    data["data"]["detection"] = detection   

    similarity = get_similarity(face_result1[0].feature, face_result2[0].feature)
    if similarity > MATCH_THRESHOLD:
        result = "SAME PERSON"
    else:
        result = "DIFFERENT PERSON"
    
    data["data"]["result"] = result   
    data["data"]["similarity"] = float(similarity)
    response = jsonify(data)
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

if __name__ == '__main__':
    ret = activate_sdk()
    if ret != 0:
        exit(-1)

    serve(app, host='0.0.0.0', port=8000)