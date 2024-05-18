#!/usr/bin/env python3
"""The Home page routes
"""
from flask import Blueprint, render_template


# Create home Blueprint
home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/')
def home():
    """Display the home page
    """
    return render_template('home.html')
