from flask import Blueprint,Response,request,jsonify
from server.controllers.web_scrapper import WebScrapper

import json
wikigenerator = Blueprint('wikigenerator', __name__,)

@wikigenerator.route('/addURL', methods=['GET'])
def add_url_request():
    try:
        if request.args['search_url']:
            search_url = str(request.args['search_url'])
            return_status = WebScrapper.get_html_content(search_url)
            if return_status == True:
                return Response("Success",status=201)
            else:
                return Response("Bad Request",status=400)
        else:
            return Response("Bad Request",status=400)
    except:
        return Response("Server Error",status=400)
    
@wikigenerator.route('/getrelativepages', methods=['POST'])
def get_relative_page_data():
    try:
        if request.args['search_keyword']:
            search_key = str(request.args['search_keyword'])
            wiki_data = WebScrapper.get_keyword_wikilinks(search_key)
            if wiki_data:
                return Response(json.dumps(wiki_data),status=201)
            else:
                return Response("Bad Request",status=400)
        else:
            return Response("Bad Request",status=400)
    except:
        return Response("Server Error",status=400)