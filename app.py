from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, jsonify, request
import requests, os
from pymongo import MongoClient
from bs4 import BeautifulSoup
from datetime import datetime

client = MongoClient(os.environ.get('MONGODB_URI'))
db = getattr(client, os.environ.get('DB_NAME'))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=["GET"])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    
    return jsonify({'articles': articles})

@app.route('/diary', methods=["POST"])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    
    today = datetime.now()
    myTime = today.strftime("%Y-%m-%d-%H-%M-%S")
    
    file = request.files["file_give"]
    extention = file.filename.split('.')[-1]
    fileName = f'file-{myTime}.{extention}'
    saveTo = f'static/{fileName}'
    file.save(saveTo)
    
    profile_file = request.files["profile_give"]
    extention = profile_file.filename.split('.')[-1]
    profileName = f'profile-{myTime}.{extention}'
    saveProfile = f'static/{profileName}'
    profile_file.save(saveProfile)
    
    timeDate = today.strftime("%Y-%m-%d")
    
    doc = {
        'file': fileName,
        'profile': profileName,
        'title': title_receive,
        'content': content_receive,
        'time': timeDate,
    }
    db.diary.insert_one(doc)
    
    return jsonify({'msg': 'Upload completed!'})

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)