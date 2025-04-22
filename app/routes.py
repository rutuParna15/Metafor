from flask import Blueprint, render_template
from .controllers import generate_metaphor

routes = Blueprint('main', __name__)

@routes.route('/explain', methods=['GET','POST'])
def explain():
    return generate_metaphor()

@routes.route('/', methods=['GET'])
def home():
    return render_template('home.html')
