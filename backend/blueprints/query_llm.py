from flask import Blueprint, request, jsonify
import requests

query_llm_bp = Blueprint('query_llm', __name__)

INFORMATICA_URL_RAGS = "https://usw5-cai.dm-us.informaticacloud.com/active-bpel/public/rt/9VCedj3QY7Lc198InmXVkW/Query_LLM_With_Context_Using_Embeddings_Model"

@query_llm_bp.route('/query-llm', methods=['POST'])
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
