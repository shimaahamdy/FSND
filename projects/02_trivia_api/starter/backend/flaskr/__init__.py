import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # cors which allow any origin (*) 
  CORS(app,resources={r"/api/*": {"origins":"*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    #list of methods applied
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  #defalut --> get method
  @app.route('/categories')
  def get_catgories():
    #select all catgories from database
    selection = Category.query.all()

    #loop over each catgory and add to dictonary
    #catgories_list has to ba a dictonary not list as fron-end recive as dict
    catgories_list = {category.id: category.type for category in selection}
    
    #check if there is no catogories arise 404 error (source not found)
    if len(catgories_list)==0:
      abort(404)
    

    #return json object
    return jsonify({
      'success':True,
      'categories':catgories_list,
      'total_categories':len(catgories_list)
    })



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
  #paginat function used to page qustions for specific number in one page
  def paginate(request,selection):
    #get page number send with request and set default to one if it doesn't exist
    page = request.args.get('page',1,type=int)
    start = (page-1)*QUESTIONS_PER_PAGE 
    end = start+QUESTIONS_PER_PAGE
    questions= [question.format() for question in selection]
    return questions[start:end]

  #default get method
  @app.route('/questions')
  def get_questions():
    #select all questions from database and page it 
    selection = Question.query.all()
    #selct catgories
    catgories_selection = Category.query.all()
    #format catgories
    catgories_list = {category.id: category.type for category in catgories_selection}
    questons = paginate(request,selection)  #list of questions

    #check if there is no questions arise 404 error (source not found)
    if len(selection)==0:
      abort(404)
      
    
    
    #return json object
    return jsonify({
      'success':True,
      'questions':questons,
      'totalQuestions':len(selection),
      'categories':catgories_list,
      'currentCategory':'no current catgory'
      
    })



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    