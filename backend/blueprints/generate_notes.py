from flask import Blueprint, request, jsonify
import requests

generate_notes_bp = Blueprint('generate_notes', __name__)

INFORMATICA_URL_NOTES = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/NotesGeneration"
INFORMATICA_URL_MINDMAP = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/MindMapGeneration"

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
        user_prompt = notes_json.get("LLM_Response")
        if not user_prompt:
            return jsonify({"error": "Notes generation did not return 'LLM_Response'"}), 500
        
        mindmap_json = generate_mindmap(user_prompt)
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
