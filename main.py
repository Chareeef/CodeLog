#!/usr/bin/env python3
"""Module that creates and configures the Flask application
"""
from flask import Flask
from config import Config


def create_app(config=Config):
    """Create the flask application
    """
    app = Flask(__name__)

    # Set configuration
    app.config.from_object(Config)

    return app


# Create and run app for developement purpose
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
