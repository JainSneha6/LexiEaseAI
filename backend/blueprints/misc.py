from flask import Blueprint, request, jsonify
import os, traceback
from werkzeug.utils import secure_filename
import google.generativeai as genai
import requests

misc_bp = Blueprint('misc', __name__)

API_KEY = "AIzaSyC6X83C-yPa-KYJnajVxPIYvisYOcQcqmc"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@misc_bp.route('/save-reading-results', methods=['POST'])
def save_reading_results():
    data = request.get_json()
    reading_speed = data.get('readingSpeed')
    time_taken = data.get('timeTaken')

    print(f"Reading Speed: {reading_speed}, Time Taken: {time_taken}")
    return jsonify(message='Reading results saved successfully!'), 200

@misc_bp.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify(message='No audio file provided!'), 400

    audio_file = request.files['audio']
    audio_path = os.path.join('uploads', f'reading_test.wav')
    audio_file.save(audio_path)

    fluency_rating = assess_fluency(audio_path)
    print(fluency_rating)
    return jsonify(message='Audio uploaded successfully!', fluency_rating=fluency_rating), 200

def assess_fluency(audio_path):
    prompt = "Rate the fluency of the audio from 100. Just give me the number."
    user_audio_file = genai.upload_file(path=audio_path)
    response = model.generate_content([user_audio_file, prompt])
    fluency_rating = extract_fluency_rating(response.text)
    return fluency_rating

def extract_fluency_rating(response_text):
    try:
        fluency_rating = int(response_text.strip())
        return fluency_rating
    except ValueError:
        print("Error extracting fluency rating:", response_text)
        return 0

@misc_bp.route('/submit_results', methods=['POST'])
def submit_results():
    global total_questions, correct_answers
    try:
        if total_questions == 0:
            return jsonify({'score': 0, 'total_questions': 0, 'correct_answers': 0})

        score_percentage = (correct_answers / total_questions) * 100
        total_questions = 0
        correct_answers = 0

        return jsonify({
            'score': score_percentage,
            'total_questions': total_questions,
            'correct_answers': correct_answers
        })
    except Exception as e:
        print(f"An error occurred while calculating the score: {e}")
        traceback.print_exc()  
        return jsonify({'error': 'An error occurred while calculating the score'}), 500
