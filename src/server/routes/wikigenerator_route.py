from flask import Blueprint

simple_page = Blueprint('simple_page', __name__,)

@simple_page.route('/', methods=['GET'])
def get_url_request():
    return ""
