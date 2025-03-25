from flask import Flask
from flask_cors import CORS
import os

from extensions import db, jwt

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    
    db.init_app(app)
    jwt.init_app(app)
    
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    from blueprints.auth import auth_bp
    from blueprints.chatbot import chatbot_bp
    from blueprints.fill_pinecone import fill_pinecone_bp
    from blueprints.query_llm import query_llm_bp
    from blueprints.generate_notes import generate_notes_bp
    from blueprints.misc import misc_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(chatbot_bp, url_prefix="/api")
    app.register_blueprint(fill_pinecone_bp, url_prefix="/api")
    app.register_blueprint(query_llm_bp, url_prefix="/api")
    app.register_blueprint(generate_notes_bp, url_prefix="/api")
    app.register_blueprint(misc_bp, url_prefix="/api")
    
    return app

if __name__ == '__main__':
    app = create_app()
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
