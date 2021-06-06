import datetime
import logging
from bson.codec_options import _parse_codec_options
from flask import Blueprint, request, make_response, jsonify,Response

from server.controllers.auth_model import AuthModel
from markupsafe import escape
auth_routes = Blueprint('auth', __name__)
 
@auth_routes.route('/auth/sign_up', methods=['POST'])
def sign_up():
    try:
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
            return response,201
        else:
            return Response("Bad Request",status=400)
    except Exception as error:
        logging.error(error)
        return Response("Server Error",status=400)

@auth_routes.route('/auth/log_in', methods=['POST'])
def log_in():
    try:
        # if request.args['user_name'] and request.args['user_password']:
        #     user_name = str(escape(request.args['user_name']))
        #     user_password = str(escape(request.args['user_password']))
        #     outputdata = AuthModel.user_auth_signup(user_name,user_password)
        #     if outputdata['auth_token']:
        #         token = outputdata['auth_token']
        #         del outputdata['auth_token']
        #     response =  make_response(jsonify(outputdata))
        #     if outputdata['status'] == 'Success':
        #         response.set_cookie('auth_cookie',value=token, httponly=True)
        #         return response,201
        # else:
        #     return Response("Bad Request",status=400)
        return Response("",status=201)
    except:
        return Response("Server Error",status=400)


# class RegisterAPI(MethodView):
#     """
#     AuthModel Registration Resource
#     """

#     def post(self):
#         # get the post data
#         post_data = request.get_json()
#         # check if AuthModel already exists
#         AuthModel = AuthModel.query.filter_by(email=post_data.get('email')).first()
#         if not AuthModel:
#             try:
#                 AuthModel = AuthModel(
#                     email=post_data.get('email'),
#                     password=post_data.get('password')
#                 )
#                 # insert the AuthModel
#                 db.session.add(AuthModel)
#                 db.session.commit()
#                 # generate the auth token
#                 auth_token = AuthModel.encode_auth_token(AuthModel.id)
#                 responseObject = {
#                     'status': 'success',
#                     'message': 'Successfully registered.',
#                     'auth_token': auth_token.decode()
#                 }
#                 return make_response(jsonify(responseObject)), 201
#             except Exception as e:
#                 responseObject = {
#                     'status': 'fail',
#                     'message': 'Some error occurred. Please try again.'
#                 }
#                 return make_response(jsonify(responseObject)), 401
#         else:
#             responseObject = {
#                 'status': 'fail',
#                 'message': 'AuthModel already exists. Please Log in.',
#             }
#             return make_response(jsonify(responseObject)), 202


# class LoginAPI(MethodView):
#     """
#     AuthModel Login Resource
#     """
#     def post(self):
#         # get the post data
#         post_data = request.get_json()
#         try:
#             # fetch the AuthModel data
#             AuthModel = AuthModel.query.filter_by(
#                 email=post_data.get('email')
#             ).first()
#             if AuthModel and bcrypt.check_password_hash(
#                 AuthModel.password, post_data.get('password')
#             ):
#                 auth_token = AuthModel.encode_auth_token(AuthModel.id)
#                 if auth_token:
#                     responseObject = {
#                         'status': 'success',
#                         'message': 'Successfully logged in.',
#                         'auth_token': auth_token.decode()
#                     }
#                     return make_response(jsonify(responseObject)), 200
#             else:
#                 responseObject = {
#                     'status': 'fail',
#                     'message': 'AuthModel does not exist.'
#                 }
#                 return make_response(jsonify(responseObject)), 404
#         except Exception as e:
#             print(e)
#             responseObject = {
#                 'status': 'fail',
#                 'message': 'Try again'
#             }
#             return make_response(jsonify(responseObject)), 500


# class AuthModelAPI(MethodView):
#     """
#     AuthModel Resource
#     """
#     def get(self):
#         # get the auth token
#         auth_header = request.headers.get('Authorization')
#         if auth_header:
#             try:
#                 auth_token = auth_header.split(" ")[1]
#             except IndexError:
#                 responseObject = {
#                     'status': 'fail',
#                     'message': 'Bearer token malformed.'
#                 }
#                 return make_response(jsonify(responseObject)), 401
#         else:
#             auth_token = ''
#         if auth_token:
#             resp = AuthModel.decode_auth_token(auth_token)
#             if not isinstance(resp, str):
#                 AuthModel = AuthModel.query.filter_by(id=resp).first()
#                 responseObject = {
#                     'status': 'success',
#                     'data': {
#                         'AuthModel_id': AuthModel.id,
#                         'email': AuthModel.email,
#                         'admin': AuthModel.admin,
#                         'registered_on': AuthModel.registered_on
#                     }
#                 }
#                 return make_response(jsonify(responseObject)), 200
#             responseObject = {
#                 'status': 'fail',
#                 'message': resp
#             }
#             return make_response(jsonify(responseObject)), 401
#         else:
#             responseObject = {
#                 'status': 'fail',
#                 'message': 'Provide a valid auth token.'
#             }
#             return make_response(jsonify(responseObject)), 401


# class LogoutAPI(MethodView):
#     """
#     Logout Resource
#     """
#     def post(self):
#         # get auth token
#         auth_header = request.headers.get('Authorization')
#         if auth_header:
#             auth_token = auth_header.split(" ")[1]
#         else:
#             auth_token = ''
#         if auth_token:
#             resp = AuthModel.decode_auth_token(auth_token)
#             if not isinstance(resp, str):
#                 # mark the token as blacklisted
#                 blacklist_token = BlacklistToken(token=auth_token)
#                 try:
#                     # insert the token
#                     db.session.add(blacklist_token)
#                     db.session.commit()
#                     responseObject = {
#                         'status': 'success',
#                         'message': 'Successfully logged out.'
#                     }
#                     return make_response(jsonify(responseObject)), 200
#                 except Exception as e:
#                     responseObject = {
#                         'status': 'fail',
#                         'message': e
#                     }
#                     return make_response(jsonify(responseObject)), 200
#             else:
#                 responseObject = {
#                     'status': 'fail',
#                     'message': resp
#                 }
#                 return make_response(jsonify(responseObject)), 401
#         else:
#             responseObject = {
#                 'status': 'fail',
#                 'message': 'Provide a valid auth token.'
#             }
#             return make_response(jsonify(responseObject)), 403

# # define the API resources
# registration_view = RegisterAPI.as_view('register_api')
# login_view = LoginAPI.as_view('login_api')
# AuthModel_view = AuthModelAPI.as_view('AuthModel_api')
# logout_view = LogoutAPI.as_view('logout_api')

