from flask import Blueprint, render_template, session, redirect, url_for

home_bp = Blueprint('home', __name__)

# Rota inicial 
@home_bp.route('/')
def index():
    return render_template('index.html')