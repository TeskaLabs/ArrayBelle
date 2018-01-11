#!/usr/bin/env python2
from app import app
from flask_cors import CORS
CORS(app)
app.run(debug=True)
