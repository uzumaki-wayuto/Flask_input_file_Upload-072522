from flask import Blueprint

send_file_bp = Blueprint('send_file', __name__)

from . import upload_file