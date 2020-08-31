from flask import jsonify, Blueprint
from .auth import AuthError

error_bp = Blueprint('error_bp', __name__)


@error_bp.app_errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'details': 'Resource not found'
    }), 404

@error_bp.app_errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'details': 'Bad Request'
    }), 400

@error_bp.app_errorhandler(AuthError)
def unauthorized(e):
    return jsonify({
        'success': False,
        'details': e.error

    }), 401

@error_bp.app_errorhandler(500)
def int_server_error(error):
    return jsonify({
        'success': False,
        'details': 'Internal Server Error'
    }), 500