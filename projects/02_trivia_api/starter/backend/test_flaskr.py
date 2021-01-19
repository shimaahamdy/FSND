import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
QUESTIONS_PER_PAGE = 10

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','love','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "create question for test?",
            "answer": "worked", 
            "difficulty": 3,
            "category": "3"
            }

        self.new_question_missing_data = {
            "difficulty": 3,
            "category": "3"
            }

        self.search_term = {
            'searchTerm': 'team'
        }

        self.no_search_term = {
            'searchTerm': ''
        }

        self.quizz_data = {
            'previous_questions': [4, 9],
            'quiz_category': {
                'type': 'History',
                'id': 4
                }
        }

        self.quizz_data_no_question_in_category5= {
            'previous_questions': [4, 9],
            'quiz_category': {
                'type': 'History',
                'id': 5
                }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_catgories(self):
        #run test and get result in json format
        res = self.client().get('/categories')
        data = json.loads(res.data)

        #check the response data
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
    
    def test_get_questions(self):
        #run test and get result in json format
        res = self.client().get('/questions')
        data = json.loads(res.data)

        #check the response data
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['currentCategory'],None)
    
    def test_404_sent_request_questions_valid_page(self):
        res = self.client().get('/questions?page=500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delted'], 2)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(question, None)
    
    def test_422_delete_question_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'requist unprocessable')

    def test_create_question(self):
        res = self.client().post('/questions',json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])

    def test_422_create_question_missing_data(self):
        res = self.client().post('/questions',json=self.new_question_missing_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'requist unprocessable')
    
    def test_search_question(self):
        response = self.client().post('/questions', json=self.search_term)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'],None)

    def test_422_search_question_no_searchterm(self):
        res = self.client().post('/questions',json=self.no_search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'requist unprocessable')

    def test_get_catgeoty_questoin(self):
        #run test and get result in json format
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        #check the response data
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['currentCategory'], 1)

    def test_404_get_questions_catgeory_not_vaild_id(self):
        res = self.client().get('/categories/50/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_random_question(self):
        res = self.client().post('/quizzes', json=self.quizz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 4)
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()