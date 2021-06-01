from flask import Flask,request
from flask_cors import CORS,cross_origin
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import os 
import librosa
import librosa.display
import time
import json
app=Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'therandomstring'
CORS(app, expose_headers='Authorization')
model = keras.models.load_model("/home/siddhu/Desktop/IBM INSTRUMENT DETECTION/models/music.h5")
instruments=["Cello","Clarinet","Flute","Acoustic guitar","Electric guitar","Organ","Piano","Saxophone","Trumpet","Violin","Human singing"]

def feature_extraction(file_name):
    audio_data,sample_rate = librosa.load(file_name,res_type="kaiser_fast")
    mfcc_features = librosa.feature.mfcc(y=audio_data,sr=sample_rate,n_mfcc=60)
    mfcc_scaled_features = np.mean(mfcc_features.T,axis=0)
    
    return mfcc_scaled_features

@app.route('/data',methods=['POST'])
def get_data():
    print(os.getcwd())
    target=os.path.join(UPLOAD_FOLDER)
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    
    destination="/".join([target, filename])
   
    file.save(destination)
    prediction_feature=feature_extraction(destination)
    prediction_feature=prediction_feature.reshape(1,-1)
    data=np.argmax(model.predict(prediction_feature), axis=-1).tolist()
    json_dump=json.dumps(data)
    print(json_dump[1:2])
    index=int(json_dump[1:2])
    return {"data":instruments[index]}
   