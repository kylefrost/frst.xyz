from flask import Blueprint

# Set up api Blueprint
api = Blueprint('api', __name__)

# API Post Route
@api.route('/create', methods=['GET', 'POST'])
def api_create():
    return "Create JSON Blueprint!"
