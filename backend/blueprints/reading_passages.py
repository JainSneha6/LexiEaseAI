import os
import json
import re
import joblib
import pandas as pd
import google.generativeai as genai
from flask import Blueprint, request, jsonify
import requests

reading_passages_bp = Blueprint('misc', __name__)

INFORMATICA_URL_MODEL_SERVE = "https://usw5-dsml.dm-us.informaticacloud.com/ml-predict/api/v1/deployment/dXpgn2QaD2PhHnhROcBQqr"

API_KEY = "AIzaSyC6X83C-yPa-KYJnajVxPIYvisYOcQcqmc"
genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

@reading_passages_bp.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify(message='No audio file provided!'), 400

    audio_file = request.files['audio']
    audio_path = os.path.join('uploads', 'reading_test.wav')
    audio_file.save(audio_path)

    fluency_rating = assess_fluency(audio_path)
    print(fluency_rating)
    return jsonify(message='Audio uploaded successfully!', fluency_rating=fluency_rating), 200

def assess_fluency_model_serve(audio_path):
    prompt = (
        "Analyze the provided audio and return a JSON object with the following keys with only numbers. No text: "
        "'ReadingSpeedWPM', 'PronunciationErrors', 'Omissions', 'Insertions', "
        "'Substitutions', 'Repetitions', 'Hesitations'. Provide numeric values for each key."
    )
    user_audio_file = genai.upload_file(path=audio_path)
    response = gemini_model.generate_content([user_audio_file, prompt])
    
    response_text = response.text.strip()
    response_text = re.sub(r'^```(?:json)?\n', '', response_text)
    response_text = re.sub(r'\n```$', '', response_text)
    
    try:
        fluency_metrics = json.loads(response_text)
    except Exception as e:
        print("Error parsing fluency JSON:", response.text, e)
        return {}

    try:
        fluency = requests.post(INFORMATICA_URL_MODEL_SERVE, json=fluency_metrics)
        if fluency.status_code != 200:
            return jsonify({
                'message': 'Error from Informatica Notes endpoint',
                'status': fluency.status_code,
                'details': fluency.text
            }), 500
        
        fluency_json = fluency.json()
        
        return jsonify(fluency_json), 200

    except Exception as e:
        return jsonify({'message': 'Error processing your request', 'error': str(e)}), 500

def assess_fluency(audio_path):
    prompt = (
        "Analyze the provided audio and return a JSON object with the following keys with only numbers. No text: "
        "'ReadingSpeedWPM', 'PronunciationErrors', 'Omissions', 'Insertions', "
        "'Substitutions', 'Repetitions', 'Hesitations'. Provide numeric values for each key."
    )
    user_audio_file = genai.upload_file(path=audio_path)
    response = gemini_model.generate_content([user_audio_file, prompt])
    
    response_text = response.text.strip()
    response_text = re.sub(r'^```(?:json)?\n', '', response_text)
    response_text = re.sub(r'\n```$', '', response_text)
    
    try:
        fluency_metrics = json.loads(response_text)
    except Exception as e:
        print("Error parsing fluency JSON:", response.text, e)
        return {}
    
    prediction_model = joblib.load('D:/LexiEaseAI/backend/models/fluency_model.pkl')
    input_data = pd.DataFrame([fluency_metrics])
    prediction = prediction_model.predict(input_data)
    model_prediction = {'Fluency': prediction[0]}
    return model_prediction



