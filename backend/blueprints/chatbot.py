from flask import Blueprint, request, jsonify
import requests

chatbot_bp = Blueprint('chatbot', __name__)

INFORMATICA_URL_CHATBOT = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/DyslexiaTextChatbot"

@chatbot_bp.route('/ask', methods=['POST'])
def ask():
    user_prompt = request.form.get('text')
    if not user_prompt:
        return jsonify({'message': 'Missing text in request'}), 400

    payload = {'user_prompt': user_prompt}
    
    try:
        response = requests.post(INFORMATICA_URL_CHATBOT, data=payload)
        if response.status_code != 200:
            return jsonify({'message': 'Error from Informatica endpoint', 'status': response.status_code}), 500
        answer = response.json().get('LLM_Answer', 'No response field found')
        return jsonify({'response': answer})
    except Exception as e:
        return jsonify({'message': 'Error processing your request'}), 500
