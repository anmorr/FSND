import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from flask.helpers import make_response
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
setup_db(app)
CORS(app)



# '''
# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# !! Running this funciton will add one
# '''
db_drop_and_create_all()




# ROUTES
# '''
# # @TODO implement endpoint
# #     GET /drinks
# #         it should be a public endpoint
# #         it should contain only the drink.short() data representation
# #     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
# #         or appropriate status code indicating reason for failure
# # '''

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drink_list = Drink.query.all()
    final_drink_list = []
    for drink in drink_list:
        final_drink_list.append(drink.short())
        # print("drink title => ", drink.title, "drink recipe => ", drink.short()) 
    return jsonify({
        "success" : True,
        "drinks" : final_drink_list,
        })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
    drink_list = Drink.query.all()
    final_drink_list = []
    for drink in drink_list:
        final_drink_list.append(drink.long())
        # print("drink title => ", drink.title, "drink recipe => ", drink.short()) 
    return jsonify({
        "success" : True,
        "drinks" : final_drink_list,
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
@app.route('/drinks', methods=['POST'])
@requires_auth("post:drinks")
def post_drinks(payload):
    try:
        # drink_list = Drink.query.all()
        drink_data_json = request.get_json()
        print(drink_data_json)
        drink_title = drink_data_json.get("title")
        drink_recipe = drink_data_json.get("recipe")
        print("Drink Title: ", drink_title)
        # drink_recipe_list = []
        # drink_recipe_list.append(drink_recipe)
        print("Drink Recipe: ", drink_recipe)
        new_drink = Drink(title=drink_title,
                        recipe=json.dumps(drink_recipe))
        new_drink.insert()
        print("After new drink")
        # new_drink2 = Drink.query.filter_by(title="Water8").first()
        final_drink_list = []
        final_drink_list.append(new_drink.long())
        return jsonify({
            "success" : True,
            "drink": [final_drink_list]
            }), 200
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
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def patch_drinks(payload=None, drink_id=None):
    try:
        current_drink = Drink.query.filter_by(id=drink_id).first()
        json_data = request.get_json()
        if json_data.get("title"):
            current_drink.title = json_data.get("title")
        if json_data.get("recipe"):
            drink_recipe_list = [json_data.get("recipe")]
            current_drink.recipe = json.dumps(drink_recipe_list)
        current_drink.update()
        updated_drink = Drink.query.filter_by(id=drink_id).first()
        updated_drink_list = [updated_drink.long()]
        print("Updated Drink: ", updated_drink_list)
        return jsonify({
            "success" : True,
            "drink": updated_drink_list
            }), 200
    except:
        abort(404)



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
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth("delete:drinks")
def delete_drinks(payload=None, drink_id=None):
    try:
        current_drink = Drink.query.filter_by(id=drink_id).first()
        print("current_drink - 1: ", current_drink)
        if current_drink:
            current_drink.delete()
            return jsonify({
                "success": True,
                "delete": drink_id
            })
        else:
            abort(404)
    except Exception as e:
      if isinstance(e, HTTPException):
        abort(e.code)




# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
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
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404

@app.errorhandler(401)
def unauthenticated(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthenticated"
    }), 401

@app.errorhandler(403)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error,
    }), 403
