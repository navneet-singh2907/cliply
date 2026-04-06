import os
from flask import Flask

def create_app():
    # This 'os.path.dirname' trick tells Flask exactly where to find the templates 
    # relative to THIS file (__init__.py)
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    app.config['SECRET_KEY'] = 'dev-key-123'
    app.config['UPLOAD_FOLDER'] = os.path.join(static_dir, 'uploads')
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app