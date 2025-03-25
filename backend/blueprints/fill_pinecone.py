from flask import Blueprint, request, jsonify
import requests

fill_pinecone_bp = Blueprint('fill_pinecone', __name__)

INFORMATICA_FILL_PINECONE_URL = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/Fill_Empty_Pinecone_Index_Using_Gemini_AI"

@fill_pinecone_bp.route('/fill-pinecone', methods=['POST'])
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
