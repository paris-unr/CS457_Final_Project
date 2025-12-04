#import kagglehub

# Download latest version
#path = kagglehub.dataset_download("ahsen1330/us-police-shootings")

from flask import Flask
from dotenv import load_dotenv
import os
from models import db
from views import main

# Load environment variables
load_dotenv()

def create_app():

# Initialize Flask app
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    
