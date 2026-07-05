import os

from flask import Flask
from dotenv import load_dotenv

from config import DevelopmentConfig, Config, TestConfig
from app.models import db, migrate
from app.routers import questions_bp, responses_bp, categories_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    flask_mode = (
        os.environ.get('FLASK_MODE')
        or os.environ.get('FLASK_ENV', 'development')
    )
    config_class = {
        'development': DevelopmentConfig,
        'production': Config,
        'testing': TestConfig,
    }.get(flask_mode, DevelopmentConfig)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(questions_bp, url_prefix='/questions')
    app.register_blueprint(responses_bp, url_prefix='/responses')
    app.register_blueprint(categories_bp, url_prefix='/categories')

    return app
