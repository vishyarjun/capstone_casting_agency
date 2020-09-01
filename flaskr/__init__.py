from config import SQLALCHEMY_DATABASE_URI
from flask import Flask, render_template, request, Response, redirect, jsonify
from flask_migrate import Migrate
import logging
from flask_sqlalchemy import SQLAlchemy
import datetime
from .movies import movie_bp
from .actors import actor_bp
from .init_model import app, db
from .errors import error_bp


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'success': True,
                    'message': 'Welcome to Casting Agency!'
                    })

app.register_blueprint(movie_bp)
app.register_blueprint(actor_bp)
app.register_blueprint(error_bp)

if __name__ == '__main__':
    app.run()
