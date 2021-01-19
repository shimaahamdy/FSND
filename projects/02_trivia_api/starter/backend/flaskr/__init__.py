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
  '''
  #paginat function used to page qustions for specific number in one page
  def paginate(request,selection):
    #get page number send with request and set default to one if it doesn't exist
    page = request.args.get('page',1,type=int)
    #get start and end index of each page 
    start = (page-1)*QUESTIONS_PER_PAGE 
    end = start+QUESTIONS_PER_PAGE
    questions= [question.format() for question in selection]
    return questions[start:end]

  #default get method
  @app.route('/questions')
  def get_questions():
    
    #select all questions from database 
    selection = Question.query.all()
    #selct catgories
    catgories_selection = Category.query.all()
    #format catgories in dictoanry form
    catgories_list = {category.id: category.type for category in catgories_selection}
    questons = paginate(request,selection)  #list of questions paginate
    
    if len(questons)==0:
      abort(404)
    #check if there is no questions arise 404 error (source not found)
  
    #return json object
    return jsonify({
      'success':True,
      'questions':questons,
      'totalQuestions':len(selection),
      'currentCategory':None,
      'categories':catgories_list
      })



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID.  
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
    try:
      #get question from database
      question = Question.query.filter(Question.id == question_id).one_or_none()
      
      #delte question
      question.delete()
      
      #return number of questions left and question itself
      selection = Question.query.all()  

      return jsonify({
        'success':True,
        'delted': question_id,
        'totalQuestions':len(selection)
        })
    except:
      abort(422)
  
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  ''' 
  @app.route('/questions', methods=['POST'])
  def create_question():
    #get requet body and content data of request
    body = request.get_json()

    question_text = body.get('question')
    answer_text = body.get('answer')
    #set default of catgory is science with difficulty = 1 as it the default in front
    category_type = body.get('category')
    difficulty_score = body.get('difficulty')
    
    try:
      #check if method was "search" with searchterm in the request
      if body.get('searchTerm'):
        return search(request)
      
      else:
        #check if question and answer exit to not create a question with empty cell
        if question_text and answer_text and category_type and difficulty_score:
          #create a new question
          question = Question(question=question_text,answer=answer_text,category=category_type,difficulty=difficulty_score)
          question.insert()
          
          return jsonify({
            'success': True,
            'created': question.id,
            'question': question.format(),
            'total_questions': len(Question.query.all())
            })

        else:
          abort(400)

    except:
        abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question.  
  '''
  def search(request):
    #get searchterm send in request 
    body = request.get_json()
    search_term = body.get('searchTerm')
    #searh in data base with any string contain the searchterm and get all question realted to it
    selected = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
    #check if there is results send it and if not send there is nothing gound but process success
    # page the result
    questions = paginate(request,selected)
    return jsonify({
      'success':True,
      'questions':questions,
      'totalQuestions':len(selected),
      'currentCategory': None
      })
    

    

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  '''
  #default get method
  @app.route('/categories/<int:catgory_id>/questions')
  def get_catgory_questions(catgory_id):
    
    #get catgory type with id
    catgory = Category.query.filter(Category.id == catgory_id).one_or_none()

    if catgory:
      #select catgory question from database and paginate it
      selection = Question.query.filter(Question.category == catgory_id).all()
      questions = paginate(request,selection)
      
      #return json object
      return jsonify({
        'success':True,
        'questions':questions,
        'totalQuestions':len(selection),
        'currentCategory':catgory_id
        })
    else:
      abort(404)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions.  
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_random_quiz():
    #get data from requist
    data = request.get_json()
    previous_questions = data.get('previous_questions')
    quiz_category = data.get('quiz_category')

    # check if request completed with needed data
    if quiz_category is None or previous_questions is None:
      abort(400)
      #check if "All" was chosen select all question available including in the preivous
      #if not select questions with specific catgory
      #fix bug ---> if it was all we return a question without check if in previous
    if quiz_category['id'] == 0:
      selection = Question.query.all()
    else:
      selection = Question.query.filter(Question.category == quiz_category['id']).all()
        
    #choose a question from selection in random
    choosen_question = selection[random.randint(0, len(selection)-1)]

    #loop on questions till find a question that not in previous questions
    infinit_loop = True       #if we found question break loop
    while infinit_loop:
      if choosen_question.id in previous_questions:
        choosen_question = selection[random.randint(0, len(selection)-1)]
      else:
        break

    return jsonify({
      'success': True,
      'question': choosen_question.format()
      })
    


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
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "requist unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request structure"
      }), 400

  return app

    