from functools import wraps
from flask import (
        Flask,
        request,
        render_template,
        jsonify,
        redirect,
        url_for,
        session)

app = Flask(__name__)
app.secret_key = "password"

def StartWebServer():
    app.run(debug=True)

