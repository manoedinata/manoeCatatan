from flask import Flask
from deta import Deta
from dotenv import load_dotenv
import os

load_dotenv()

deta = Deta(os.getenv("DETA_PROJECT_KEY"))
catatanDb = deta.Base("catatan")

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY").encode()

    # Main routes
    from manoeCatatan.main_routes import main as main_routes
    app.register_blueprint(main_routes)

    return app
