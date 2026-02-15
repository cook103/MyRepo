import queue
import threading

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

database_dcf_run_queue = queue.Queue()

class DCFRun(db.Model):
    __tablename__ = "dcf_runs"
    id = db.Column(db.Integer, primary_key=True)
    dcf_details = db.Column(db.JSON, nullable=False)
    model_version = db.Column(db.String(20), default="v1")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dcf.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

app = create_app()

def process_runs_into_database():
    def fn():
        with app.app_context():
            while True:
                # get analyzed data off queue and create database entry.
                reply_message = database_dcf_run_queue.get()
                run = DCFRun(dcf_details=reply_message)
                db.session.add(run)
                db.session.commit()

    queue_publish_thread = threading.Thread(target=fn, args=(), daemon=True)
    queue_publish_thread.start()
