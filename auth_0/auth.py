'''
    REFERENCES: Identity and Access Management section of Udacity Full stack nano degree program
'''
import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


#AUTH0_DOMAIN= os.getenv('AUTH0_DOMAIN')
#ALGORITHMS= os.getenv('ALGORITHMS')
#API_AUDIENCE = os.getenv('API_AUDIENCE')

AUTH0_DOMAIN='dev-uda-course.us.auth0.com'
ALGORITHMS=['RS256']
API_AUDIENCE='capstone'
## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
'''
    get_token_auth_header() - Method to extract token from header 
    This method attempts to get the header from the request and raises an AuthError if no header is present.
    It attempts to split bearer and the token and raises an AuthError if the header is malformed. 
    It returns the token part of the header
'''
def get_token_auth_header():

    authorization = request.headers.get('Authorization', None)
    if not authorization:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Please specify authorization header'  
        },401)

    BT = authorization.split()
    if len(BT)==1:
        raise AuthError({
            'code': 'no_header',
            'description': 'Specify token'  
        },401)
    bearer, token = BT[0],BT[1]
    if len(BT)!=2 or bearer.lower()!='bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Header type must be bearer token'  
        },401)

    return token

'''
    verify_decode_jwt(token) - Method to verify the input json web token (string) and decode it
    This method verifies the token using Auth0 /.well-known/jwks.json. It verifies if the token is an Auth0 token with key id (kid).
    It decodes the payload from the token and validates the claims. It returns the decoded payload if the token is succesfully verified
    or appropriate error signature.
'''
def verify_decode_jwt(token):
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks_reference = json.loads(json_url.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'key_id_missing',
            'description': 'Key id not in header'  
        },401)

    for key in jwks_reference['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kid' : key['kid'],
                'kty' : key['kty'],
                'use' : key['use'],
                'n'   : key['n'],
                'e'   : key['e']
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms = ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://'+AUTH0_DOMAIN+'/'
            )
            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'expired_signature',
                'description': 'Signature Expired'  
            },401)
        
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Check audience and issuer'  
            },401)
        
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Bad token'  
            },400)

    raise AuthError({
            'code': 'invalid_header',
            'description': 'Can not find key'  
        },400)

'''
    check_permissions(permission, payload) - Method to verify if the token payload has the required permission to access the resource
    INPUTS: 
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    This method raises an AuthError if permissions are not included in the payload. 
    It raises an AuthError if the requested permission string is not in the payload permissions array.
    It returns True if permission is present and the resource can be accessed.
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'missing_permissions',
            'description': 'Permissions missing from payload'  
        },400)


    
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'access_denied',
            'description': 'You do not have permission to access this feature'  
        },403)

    return True


def get_user_identity(payload):
    if 'https://anusha.example.com/username' not in payload:
        raise AuthError({
                'code': 'username not available',
                'description': 'Check that you have a username'  
            },401)
  
    return payload['https://anusha.example.com/username']

'''
    @requires_auth(permission) - decorator method to authorize acess to the endpoints.
    INPUTS:
        permission: string permission
    This method uses get_token_auth_header method to extract the token from the header.
    It passes the extracted token into the verify_decode_jwt method to verify and decode the token.
    It passes the permission input and the payload decoded from verify_decode_jwt method into the
    check_permissions method to check the requested permission. If any of the aove steps fail, an 
    error is flagged right away. If the authorization is sucessful, decoded payload is returned to
    the decorated method.    
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            user_identity = get_user_identity(payload)
            return f( user_identity, *args, **kwargs, )
        return wrapper
    return requires_auth_decorator


