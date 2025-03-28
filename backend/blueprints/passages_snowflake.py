from flask import Blueprint, request, jsonify
from flask_cors import CORS
import snowflake.connector
import os
from dotenv import load_dotenv
import random

passages_snowflake_bp = Blueprint('passages_snowflake', __name__)

load_dotenv()

def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

@passages_snowflake_bp.route('/passages', methods=['GET'])
def get_passages():
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM PASSAGES;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    print(rows)

    columns = [desc[0] for desc in cursor.description]

    passages = [dict(zip(columns, row)) for row in rows]
    
    cursor.close()
    conn.close()

    easy = [p for p in passages if p["EASY"]]
    medium = [p for p in passages if p["MEDIUM"]]
    hard = [p for p in passages if p["HARD"]]

    selected_passages = {
        "easy": random.sample(easy, 2) if len(easy) >= 2 else easy,
        "medium": random.sample(medium, 2) if len(medium) >= 2 else medium,
        "hard": random.sample(hard, 2) if len(hard) >= 2 else hard,
    }

    return jsonify(selected_passages)

