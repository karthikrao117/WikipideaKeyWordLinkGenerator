from flask import Blueprint,Response,request,jsonify
from server.controllers.web_scrapper import WebScrapper
import logging
wikigenerator = Blueprint('wikigenerator', __name__,)

@wikigenerator.route('/addURL', methods=['GET'])
def add_url_request():
    if request.args['search_url']:
        search_url = str(request.args['search_url'])
        WebScrapper.get_html_content(search_url)
        logging.warning("sup")
    return Response({},status=201)
