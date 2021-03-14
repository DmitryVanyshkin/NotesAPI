from flask import Flask 
from app.api import api
import logging

app = Flask(__name__)
api.init_app(app)
app.run(debug=False, host="0.0.0.0", port=5000)
