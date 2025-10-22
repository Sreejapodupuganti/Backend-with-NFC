from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for your frontend origin
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    from .your_blueprint_file import main_bp  
    app.register_blueprint(main_bp)

    return app
