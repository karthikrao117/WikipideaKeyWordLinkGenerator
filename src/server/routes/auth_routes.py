import logging

from flask import Blueprint, request, make_response, jsonify,Response
from markupsafe import escape

from server.controllers.auth_model import AuthModel

auth_routes = Blueprint('auth', __name__)
 
@auth_routes.route('/auth/sign_up', methods=['POST'])
def sign_up():
    try:
        logging.info("Begin View Module sign_up::")
        if request.args['user_name'] and request.args['user_password']:
            user_name = str(escape(request.args['user_name']))
            user_password = str(escape(request.args['user_password']))
            outputdata = AuthModel.user_auth_signup(user_name,user_password)
            if  outputdata['status'] == 'Success' and outputdata['auth_token']:
                token = outputdata['auth_token']
            del outputdata['auth_token']
            response =  make_response(jsonify(outputdata))
            if outputdata['status'] == 'Success':
                response.set_cookie('auth_cookie',value=token, httponly=True)
                # update secure flag expire etc 
            return response,201
        else:
            return Response("Bad Request",status=400)
    except Exception as error:
        logging.error("Error occured in View Module sign_up::"+str(error))
        return Response("Server Error",status=400)

@auth_routes.route('/auth/log_in', methods=['POST'])
def log_in():
    try:
        logging.info("Begin View Module log_in::")
        if request.args['user_name'] and request.args['user_password']:
            user_name = str(escape(request.args['user_name']))
            user_password = str(escape(request.args['user_password']))
            outputdata = AuthModel.user_auth_login(user_name,user_password)
            if  outputdata['status'] == 'Success' and outputdata['auth_token']:
                token = outputdata['auth_token']
            del outputdata['auth_token']
            response =  make_response(jsonify(outputdata))
            if outputdata['status'] == 'Success':
                response.set_cookie('auth_cookie',value=token, httponly=True)
                # update secure flag expire etc 
            return response,201
        else:
            return Response("Bad Request",status=400)
    except Exception as error:
        logging.error("Error occured in View Module sign_up::"+str(error))
        return Response("Server Error",status=400)