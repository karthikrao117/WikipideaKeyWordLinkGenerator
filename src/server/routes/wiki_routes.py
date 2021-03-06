import json
import logging

from flask import Blueprint,Response,request
from markupsafe import escape

from server.controllers.web_scrapper_model import WebScrapper
from server.controllers.auth_model import  AuthModel

wiki_routes = Blueprint('wiki_routes', __name__)

@wiki_routes.route('/addwikilinks', methods=['GET'])
def add_url_request():
    try:
        logging.info("Begin View Module add_url_request::")
        token = request.cookies.get('auth_cookie')
        if token:
            if AuthModel.verify_user_validity(token):
                if request.args['search_url']:
                    search_url = str(escape(request.args['search_url']))
                    return_status = WebScrapper.get_html_content(search_url)
                    if return_status == True:
                        return Response("Success",status=201)
                    else:
                        return Response("Bad Request",status=400)
                else:
                    return Response("Bad Request",status=400)
        return Response("UnAuthorized",status=401) 
    except Exception as error:
        logging.error("Error occured in View Moduleof add_url_request::"+str(error))
        return Response("Server Error",status=400)
    
@wiki_routes.route('/getrelativepages', methods=['POST'])
def get_relative_page_data():
    try:
        logging.info("Begin View Module get_relative_page_data::")
        token = request.cookies.get('auth_cookie')
        if token:
            if AuthModel.verify_user_validity(token):
                if request.args['search_keyword']:
                    search_key = str(request.args['search_keyword'])
                    wiki_data = WebScrapper.get_keyword_wikilinks(search_key)
                    if wiki_data:
                        return Response(json.dumps(wiki_data),status=201)
                    else:
                        return Response("Bad Request",status=400)
                else:
                    return Response("Bad Request",status=400)
        return Response("UnAuthorized",status=401)
    except Exception as error:
        logging.error("Error occured in View Moduleof get_relative_page_data::"+str(error))
        return Response("Server Error",status=400)