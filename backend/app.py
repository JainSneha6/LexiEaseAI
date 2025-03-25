from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, create_access_token
import os
import google.generativeai as genai
import re
import traceback
import requests

API_KEY = "AIzaSyC6X83C-yPa-KYJnajVxPIYvisYOcQcqmc"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:3000"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key' 
db = SQLAlchemy(app)
jwt = JWTManager(app)  

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

INFORMATICA_URL_CHATBOT = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/DyslexiaTextChatbot"
INFORMATICA_URL_RAGS = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/Query_LLM_With_Context_Using_Embeddings_Model"
INFORMATICA_FILL_PINECONE_URL = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/Fill_Empty_Pinecone_Index_Using_Gemini_AI"
INFORMATICA_URL_NOTES = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/NotesGeneration"
INFORMATICA_URL_MINDMAP = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/MindMapGeneration"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    test_score = db.Column(db.Integer, default=0)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify(message='User already exists!'), 409

    new_user = User(email=data['email'], password=generate_password_hash(data['password'], method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message='User created successfully!'), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(message='Login successful!', access_token=access_token), 200
    return jsonify(message='Invalid email or password!'), 401

@app.route('/api/ask', methods=['POST'])
def ask():
    user_prompt = request.form.get('text')
    if not user_prompt:
        return jsonify({'message': 'Missing text in request'}), 400

    payload = {'user_prompt': user_prompt}
    
    print(payload)

    try:
        response = requests.post(INFORMATICA_URL_CHATBOT, data=payload)
        
        print(response)
        
        if response.status_code != 200:
            return jsonify({'message': 'Error from Informatica endpoint', 'status': response.status_code}), 500

        answer = response.json().get('LLM_Answer', 'No response field found')
        return jsonify({'response': answer})
    except Exception as e:
        print("Error proxying request:", str(e))
        return jsonify({'message': 'Error processing your request'}), 500
    
@app.route('/api/fill-pinecone', methods=['POST'])
def fill_pinecone():
    document_text = request.form.get('document_text')
    if not document_text:
        return jsonify({'message': 'Missing document_text in request'}), 400

    payload = {
        "Input": document_text,
        "Output_Dimensionality": "768",
        "Model": "text-embedding-004",
        "Index_Host": "lexieaseai-c5gq0hp.svc.aped-4627-b74a.pinecone.io"
    }
    
    try:
        response = requests.post(INFORMATICA_FILL_PINECONE_URL, json=payload)
        
        if response.status_code != 200:
            return jsonify({
                'message': 'Error from Informatica endpoint', 
                'status': response.status_code,
                'details': response.text
            }), 500

        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({'message': 'Error processing your request', 'error': str(e)}), 500
    
@app.route('/api/query-llm', methods=['POST'])
def query_llm():
    data = request.get_json()
    if not data or 'Query' not in data:
        return jsonify({'message': 'Missing Query in request body'}), 400

    query = data.get('Query')

    payload = {
        "Query": query,
        "TopK": "2",
        "Score_Cuttoff": "0.5",
        "Index_Host": "lexieaseai-c5gq0hp.svc.aped-4627-b74a.pinecone.io"
    }

    try:
        response = requests.post(INFORMATICA_URL_RAGS, json=payload)
        
        if response.status_code != 200:
            return jsonify({
                'message': 'Error from Informatica endpoint',
                'status': response.status_code,
                'details': response.text
            }), 500
            
        return jsonify(response.json()), 200

    except Exception as e:
        return jsonify({'message': 'Error processing your request', 'error': str(e)}), 500
    
@app.route('/api/generate-notes', methods=['POST'])
def generate_notes():
    data = request.json
    extracted_content = data.get("extracted_content")
    if not extracted_content:
        return jsonify({"error": "Missing 'extracted_content' in request"}), 400

    payload = {
        "extracted_content": extracted_content
    }

    try:
        notes_response = requests.post(INFORMATICA_URL_NOTES, json=payload)
        if notes_response.status_code != 200:
            return jsonify({
                'message': 'Error from Informatica Notes endpoint',
                'status': notes_response.status_code,
                'details': notes_response.text
            }), 500
        
        notes_json = notes_response.json()
        user_prompt = notes_json.get("LLM_Response")
        if not user_prompt:
            return jsonify({"error": "Notes generation did not return 'LLM_Response'"}), 500
        
        mindmap_json = generate_mindmap(user_prompt)
        
        print(mindmap_json)
        
        combined_response = {
            "notes": notes_json,
            "mindmap": mindmap_json
        }
        
        return jsonify(combined_response), 200

    except Exception as e:
        return jsonify({'message': 'Error processing your request', 'error': str(e)}), 500

def generate_mindmap(user_prompt):
    payload = {
        "user_prompt": user_prompt
    }
    try:
        response = requests.post(INFORMATICA_URL_MINDMAP, json=payload)
        if response.status_code != 200:
            return {
                'message': 'Error from Informatica MindMap endpoint',
                'status': response.status_code,
                'details': response.text
            }
        return response.json()
    except Exception as e:
        return {'message': 'Error processing mindmap request', 'error': str(e)}

@app.route('/api/save-reading-results', methods=['POST'])
def save_reading_results():
    data = request.get_json()
    reading_speed = data.get('readingSpeed')
    time_taken = data.get('timeTaken')

    print(f"Reading Speed: {reading_speed}, Time Taken: {time_taken}")

    return jsonify(message='Reading results saved successfully!'), 200

@app.route('/api/upload-audio', methods=['POST'])
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
    
def save_file(file, prefix):
    """Save the file securely and return its path."""
    filename = secure_filename(f"{prefix}_{file.filename}")
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    return filepath

def handle_gemini_prompt(file_path=None, text_prompt=None):
    """Send the file or text to Gemini AI for processing."""
    try:
        if file_path:
            uploaded_file = genai.upload_file(path=file_path)
            response = model.generate_content([uploaded_file, text_prompt])
        else:
            response = model.generate_content([text_prompt])
        
        return response.text.replace('**', '').replace('*', '').strip()
    except Exception as e:
        print(f"Error generating content: {e}")
        return "Error generating content."
    
total_questions = 0
correct_answers = 0

def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/api/submit_results', methods=['POST'])
def submit_results():
    """Handle submission of results and calculate score."""
    global total_questions
    global correct_answers

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
    
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
