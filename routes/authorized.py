from flask import request, Response, jsonify, Blueprint, redirect, abort
from flasgger import swag_from
from flask_cors import cross_origin, CORS
from modules.authorized import AUTHORIZED
from modules.config import setup_config
from functools import wraps
from modules.logging import setup_logging
import json, os

config = setup_config()
logging = setup_logging()

ADMIN = config["ADMIN"]["PASSWORD"]

FULL_UUID = ''
IP_STATUS = ''
JSON_FILE = ''

authorized_bp = Blueprint('authorized_bp', __name__)
authorized = AUTHORIZED()
CORS(authorized_bp)


# ==================================================================================================================================================== #

def admin_password():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the admin password from the headers
            admin_password = request.headers.get('L33T-MY')
            if admin_password == ADMIN:
                return f(*args, **kwargs)
            else:
                return jsonify({"responseData": "Gonna manipulate? Hihi"}), 401
        return decorated_function
    return decorator

# ==================================================================================================================================================== #

@authorized_bp.errorhandler(500)
def internal_server_error(e):
    return jsonify({'responseData': 'Internal server error'}), 500

@authorized_bp.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'responseData': 'Method not allowed'}), 405

# ==================================================================================================================================================== #

@authorized_bp.route('/<short_code>', methods=['GET', 'POST'])
@cross_origin()
@swag_from('../swagger/authorized/shorten.yml')
def handle_url(short_code=None):
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'responseData': 'Missing JSON data'}), 401
        
        data = request.get_json()
        original_url = data.get('url', None)
        
        if not original_url:
            return jsonify({"message": "URL is required"}), 400
        
        authorized.original_url = original_url
        return authorized.shorten_url_logic()
    
    elif request.method == 'GET':
        if not short_code:
            return jsonify({'responseData': 'Missing required field'}), 400
        
        original_url = authorized.get_original_url(short_code)
        
        if original_url:
            return redirect(original_url)
        else:
            return abort(404, description="Shortened URL not found")

# ==================================================================================================================================================== #

@authorized_bp.route('/iptv', methods=['GET'])
@cross_origin()
def get_iptv():
    username = request.args.get('username')
    uuid = request.args.get('uuid')
    
    if not username or not uuid:
        return jsonify({"responseData": "missing required field!"}), 400
    
    authorized = AUTHORIZED()
    authorized.username = username
    authorized.uuid = uuid
    return authorized.get_iptvs()


# ==================================================================================================================================================== #

