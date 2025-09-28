from flask import Flask
import os
from dotenv import load_dotenv, dotenv_values 

app = Flask(__name__)


# Load variables from .env file
load_dotenv()

@app.route("/")
def hello_world():
    return os.getenv("APLOS_KEY")
