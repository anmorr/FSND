import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from werkzeug.exceptions import HTTPException

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
# CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  #################################################################################
  #                                                                               #
  #                              Helper Methods                                   #
  #                                                                               #
  #################################################################################

  def paginate_questions(request, selection):
    page = request.args.get("page", default=1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.all()
    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]
    return current_questions


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_all_categories():
    try:
      categories = Category.query.all()
      category_dict = {}
      for category in categories:
        category_dict[category.id] = category.type
      return jsonify({
          'categories': category_dict,
      }), 200
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_all_questions():
    try:
      categories = Category.query.all()
      # categories = [category.format() for category in categories]
      category_dict = {}
      for category in categories:
        # print(category)
        category_dict[category.id] = category.type
      # print(categories)
      print(category_dict)
      questions = Question.query.all()
      current_questions = paginate_questions(request, questions)
      # print(current_questions)
      if len(current_questions) == 0:
        abort(404)
      
      print("category_dict ======> ", current_questions)

      return jsonify({
          'categories': category_dict,
          'questions': current_questions,
          'total_questions': len(questions),
          'current_category': current_questions[0]['category'],
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      current_question = Question.query.filter_by(id=question_id).first()
      if current_question:
        current_question.delete()
      else:
        abort(404)
      return jsonify({
          'success': True,
      }), 200
    except Exception as e:
      if isinstance(e, HTTPException):
        abort(e.code)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():

    print("====>", request.json)

    question = request.json.get('question')
    answer = request.json.get('answer')
    difficulty = request.json.get('difficulty')
    category = request.json.get('category')
    search = request.json.get('searchTerm')
    print("search ========> ", search)
   

    if search:
        search_string = "%" + search + "%"
        print(search_string)
        question_search_results = Question.query.filter(Question.question.ilike(search_string)).all()
        print(question_search_results)
        if question_search_results:
          paginated_question_results = paginate_questions(request, question_search_results)
          print("paginated_question_results===> ", paginated_question_results)
          print("paginated_question_results category ===> ", paginated_question_results[0]['category'])
          return jsonify({
              'questions': paginated_question_results,
              'total_questions': len(question_search_results),
              'current_category': paginated_question_results[0]["category"],
          }), 200
        else:
          return jsonify({
              'success': False,
              'books': 0,
              'total_books': 0
          }), 200

    # print(question + " " + answer + " " + str(difficulty))
    # if question == None or answer == None or difficulty == None:
    #   abort(422)
    

    try:
      print("In the try block...")
      new_question = Question(question=question, answer=answer, 
                              difficulty=difficulty, category=category)
      print(new_question)
      new_question.insert()
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
    
      return jsonify({
          'success': True,
          'created': new_question.id,
          'questions': current_questions,
          'total_questions': len(questions),
      }), 201
    except:
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  ####### In the method above ########

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_question_by_category(category_id):
    print(request.json)
    try:
      current_questions = Question.query.filter_by(category=category_id).all()
      paginated_questions = paginate_questions(request, current_questions)
      if paginated_questions:
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(current_questions),
            'current_category': category_id
        }), 200
    except Exception as e:
      if isinstance(e, HTTPException):
        abort(e.code)



  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    print("reqest.json=> ", request.json)
    previous_questions = request.json.get('previous_questions')
    quiz_category = request.json.get('quiz_category')
    print("previous_questions=> ", previous_questions)
    print("quiz_category=> ", quiz_category)
    if previous_questions:
      if quiz_category['id'] is 0:
        available_questions = Question.query.filter(~Question.id.in_(previous_questions)).all()
      else:
        available_questions = Question.query.filter_by(category=quiz_category['id']).filter(~Question.id.in_(previous_questions)).all()
    else:
      if quiz_category['id'] is 0:
        available_questions = Question.query.filter(~Question.id.in_(previous_questions)).all()
      else:
        available_questions = Question.query.filter_by(category=quiz_category['id']).all()
    print(available_questions)
    if available_questions:
      # end_index = (len(available_questions) - 1)
      final_question = available_questions[random.randint(0,(len(available_questions) - 1))].format()
      return jsonify({
              'question': final_question
          }), 200
    else:
      return jsonify({
              'question': False,
          }), 200

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "Not found"
          }), 404
 
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False, 
          "error": 422,
          "message": "unprocessable"
          }), 422


  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          "success": False, 
          "error": 405,
          "message": "Method Not Allowed"
          }), 405
  
  return app

    