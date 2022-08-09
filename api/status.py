import json

from flask import Blueprint, render_template
status = Blueprint('status', __name__)

@status.route('/status')
def process():
    """ 死活チェック """
    return json.dumps({"status": "ok"})
