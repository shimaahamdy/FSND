import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
#no call for auth as it is public endpoint
def get_drinks():

    #select all drinks from database
    selection = Drink.query.all()
    
    #return json object with short format for drinks
    return jsonify({
      'success': True,
      'drinks': [drink.short() for drink in selection]
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
#premission allowed
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    #select all drinks from database
    selection = Drink.query.all()

    #return json object with long format for drinks
    return jsonify({
      'success': True,
      'drinks': [drink.long() for drink in selection]
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks' , methods = ['POST'])
#premission allowed
@requires_auth('post:drinks')
def create_drink(payload):

    #get requet body and content data of request
    body = request.get_json()
    drink_title = body.get('title')
    #convert the object to string
    drink_recipe = json.dumps(body.get('recipe'))
    try:
        if not drink_recipe or not  drink_title:
            abort(400)
        
        #create a new row in the drinks table
        drink = Drink(title=drink_title,recipe=drink_recipe)
        drink.insert()

        #return json object with long format for drink
        return jsonify({
            'success': True,
            'drinks': drink.long()
            })
    except:
        abort(422)

        
        

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>' , methods = ['PATCH'])
#premission allowed
@requires_auth('patch:drinks')
def update_drink(payload,drink_id):

    #get drink with id
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    #respond with a 404 error if <id> is not found
    if not drink:
        abort(404)
    
    #get requet body and content data of request
    body = request.get_json()
    drink_title = body.get('title')
    #convert the object to string
    drink_recipe = json.dumps(body.get('recipe'))
    
    try:
        #update the corresponding row for <id>
        if drink_recipe:
            drink.recipe = drink_recipe
        
        if drink_title:
            drink.title = drink_recipe
        
        drink.update()

        #return json object with long format for drinks
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
            })
    except:
        abort(422)

    

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>' , methods = ['DELETE'])
#premission allowed
@requires_auth('delete:drinks')
def delete_drink(payload,drink_id):
    #get drink with id
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    #respond with a 404 error if <id> is not found
    if not drink:
        abort(404)
    
    try:
        #delete the corresponding row for <id>
        drink.delete()
        #return json object with long format for drinks
        return jsonify({
            'success': True,
            'delete': drink_id
            })
    except:
        abort(422)  
    
    


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request structure"
      }), 400

@app.errorhandler(403)
def forbidden_request(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "forbidden requiest:Permission Not found"
      }), 403
'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(error):
    #print the error that arise in auth functions
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "code": error.error['code'],
        "message": error.error['description']
    }), error.status_code
