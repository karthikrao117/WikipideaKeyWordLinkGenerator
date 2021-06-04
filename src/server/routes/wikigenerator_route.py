from flask import Blueprint,Response,request,jsonify
from server.controllers.web_scrapper import WebScrapper
import logging
wikigenerator = Blueprint('wikigenerator', __name__,)

@wikigenerator.route('/addURL', methods=['GET'])
def add_url_request():
    try:
        if request.args['search_url']:
            search_url = str(request.args['search_url'])
            WebScrapper.updateKeywordLinkMap(search_url)
            return Response("Success",status=201)
        else:
            return Response("Enter valid search url",status=404)
    except:
        return Response("Invalid search url passed")
    
