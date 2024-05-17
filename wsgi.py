#!/usr/bin/env python3
"""Our production launchpad!
"""
from main import create_app


# Create and run app in production environment
if __name__ == '__main__':
    app = create_app()
    app.run()
