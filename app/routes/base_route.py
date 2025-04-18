from flask import Blueprint, render_template
import app


base = Blueprint('base', __name__, template_folder='templates')

@base.route('/', methods=['GET'])
def index():
    return render_template('index.html')