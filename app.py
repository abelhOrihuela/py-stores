import os
from flask import Flask, jsonify
from ma import ma
from instance.config import app_config
from manager import create_app
from dotenv import load_dotenv

load_dotenv()
app = create_app(os.getenv("ENVIRONMENT"))

if __name__ == "__main__":
    ma.init_app(app)
    app.run(port=5000)
