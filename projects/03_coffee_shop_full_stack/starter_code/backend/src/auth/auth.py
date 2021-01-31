import json
from flask import request, _request_ctx_stack, jsonify, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'idandauth.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000'

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
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    
    #get header from request
    auth_header = request.headers.get('Authorization',None)

    #raise an AuthError if no header is present
    if not auth_header:
        raise header_missing

    #split bearer and the token
    header_parts = auth_header.split()
    barrer = header_parts[0]
    token = header_parts[1]

    #raise an AuthError if the header is malformed
    
    #check if header in barrer_token form
    if len(header_parts)>2 or not barrer:
        raise malformed_auth
    #check first term is bearer
    if barrer.lower() != 'bearer':
        raise barrer_not_found
    #check if token is send
    if not token:
        raise token_not_found

    #return token
    return token


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    #raise an AuthError if permissions are not included in the payload
    if 'permissions' not in payload:
        abort(400)
    #raise an AuthError if the requested permission string is not in the payload permissions array
    if permission not in payload['permissions']:
        raise premission_not_found
    return True
'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    #get jwks from Auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    #an Auth0 token with key id (kid)
    if 'kid' not in unverified_header:
        raise malformed_auth

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    #verify the token using Auth0 /.well-known/jwks.json
    if rsa_key:
        #decode the payload from the token
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        #validate the claims
        except jwt.ExpiredSignatureError:
            raise token_expired

        except jwt.JWTClaimsError:
            raise incorrect_clamis
        
        except Exception:
            raise not_pars_auth
    
    raise not_found_key

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


# some implmentation of errors:
header_missing = AuthError({
    'code': 'missing_authorization_header',
    'description': 'an authorization header is expected to be send in request.'
    }, 401)

barrer_not_found = AuthError({
    'code': 'invalid_header',
    'description': 'Authorization header must start with "Bearer".'
    }, 401)

malformed_auth = AuthError({
    'code': 'invalid_header',
    'description': 'Authorization malformed.'
    }, 401)

token_not_found = AuthError({
    'code': 'invalid_header',
    'description': 'Token not found.'
    }, 401)

token_expired = AuthError({
    'code': 'token_expired',
    'description': 'Token expired.'
    }, 401)

incorrect_clamis = AuthError({
    'code': 'invalid_claims',
    'description': 'Incorrect claims. check the audience and issuer.'
    }, 401)

not_pars_auth = AuthError({
    'code': 'invalid_header',
    'description': 'Unable to parse authentication token.'
    }, 400)

not_found_key = AuthError({
    'code': 'invalid_header',
    'description': 'Can not find the appropriate key.'
    }, 400)

premission_not_found = AuthError({
    'code': 'unauthorized',
    'description': 'Permission Not found',
    }, 401)
