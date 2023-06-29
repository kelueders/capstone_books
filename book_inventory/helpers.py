from flask import request, jsonify    # jsonify makes it so any language can be read
from functools import wraps
import secrets
import decimal
import requests
import json

from book_inventory.models import User

# decorator function that we will use elsewhere
def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        """
        This function takes in any number of args & kwargs and verifies that the token
        passed into the headers is associated with a user in the database. 
        """
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401    # Client error
        
        try:
            our_user = User.query.filter_by(token = token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
            
        except:
            our_user = User.query.filter_by(token = token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        return our_flask_function(our_user, *args, **kwargs)
    return decorated       # since it is decorater function you have to return decorated

class JSONEncoder(json.JSONEncoder):       # inheriting the default JSON encoder and then extending it for additional functions
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):     # default json encoder does not handle decimals so we have to add this feature
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)