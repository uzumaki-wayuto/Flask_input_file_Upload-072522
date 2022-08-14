from flask import Flask
from config import Config

def init_app():
    
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')
    app.config.from_object(Config)
    
    with app.app_context():
        from .upload import send_file_bp
        app.register_blueprint(send_file_bp, url_prefix= '/')
        return app
    
