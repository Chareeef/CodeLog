#!/usr/bin/env python3
"""Module that creates and configures the Flask application
"""
from flask import Flask
from config import Config
from routes import auth_bp, home_bp, profile_bp


def create_app(config=Config):
    """Create the flask application
    """
    app = Flask(__name__)

    # Set configuration
    app.config.from_object(Config)

    # Disable strict slashes
    app.url_map.strict_slashes = False

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(profile_bp, url_prefix='/user')

    return app


# Create and run app for developement purpose
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host=Config.HOST, port=Config.PORT)
