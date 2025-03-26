from flask import Blueprint, request, jsonify
import requests

generate_mindmap_bp = Blueprint('generate_mindmap', __name__)

INFORMATICA_URL_MINDMAP = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/MindMapGeneration"

@generate_mindmap_bp.route('/generate-mindmap', methods=['POST'])
def generate_notes():
    data = request.json
    extracted_content = data.get("extracted_content")
    if not extracted_content:
        return jsonify({"error": "Missing 'extracted_content' in request"}), 400

    payload = {
        "user_prompt": extracted_content
    }

    try:
        mindmap_response = requests.post(INFORMATICA_URL_MINDMAP, json=payload)
        if mindmap_response.status_code != 200:
            return jsonify({
                'message': 'Error from Informatica Notes endpoint',
                'status': mindmap_response.status_code,
                'details': mindmap_response.text
            }), 500
        
        mindmap_json = mindmap_response.json()
        
        return jsonify(mindmap_json), 200

    except Exception as e:
        return jsonify({'message': 'Error processing your request', 'error': str(e)}), 500
