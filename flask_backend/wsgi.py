#!/usr/bin/env python3
"""Our production launchpad!
"""
from main import create_app
from config import Config


# Create and run app in production environment
app = create_app()
if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT)
