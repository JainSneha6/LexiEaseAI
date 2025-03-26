from flask import Blueprint, request, jsonify
import requests

generate_notes_bp = Blueprint('generate_notes', __name__)

INFORMATICA_URL_NOTES = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/NotesGeneration"

@generate_notes_bp.route('/generate-notes', methods=['POST'])
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
        
        return jsonify(notes_json), 200

    except Exception as e:
        return jsonify({'message': 'Error processing your request', 'error': str(e)}), 500
