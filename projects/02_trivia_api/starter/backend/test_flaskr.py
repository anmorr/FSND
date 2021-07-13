import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from pprint import pprint


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # print("creating the tables...")
            # create all tables
            self.db.create_all()
        
        # Question.query.delete() 
        Question.query.delete()
        Category.query.delete()
        self.category1 = Category(type="Sports")
        self.category1.insert()
        # print("TYPE OF CAT1: ", type(self.category1.id))
        self.question1 = Question(question='Who is the Brown Bomber',answer='Joe Lewis',difficulty=3, category=self.category1.id)
        self.question1.insert()
    
    def tearDown(self):
        """Executed after reach test"""
        Question.query.delete()
        # self.question1.delete()
        
       

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        """Test that gets all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)


    def test_get_all_questions(self):
        """Test that gets all questions"""
        # self.question1 = Question(question='Who is the Brown Bomber',answer='Joe Lewis',difficulty=3, category=5)
        # self.question1.insert()
        res = self.client().get('/questions')
        data = json.loads(res.get_data(as_text=True))
        # print("data ===> ", data)
        self.assertEqual(res.status_code, 200)


    def test_delete_question(self):
        """Test delete a question"""
        res = self.client().delete('/questions/' + str(self.question1.id))
        data = json.loads(res.get_data(as_text=True))
        # print("delete data ===> ", data)
        # print("questions ===> ", Question.query.all())
        # # print(res)
        self.assertEqual(len(Question.query.all()), 0)
        self.assertEqual(data.get('success'), True)
        self.assertEqual(res.status_code, 200)
    
    def test_create_question(self):
        """Test that creates a question"""
        self.question1.delete()
        new_question = {
            "question": 'Sample Question', 
            'answer': 'Sample Answer', 
            'difficulty': '3', 
            'category': '2'
        }
        json_data = json.dumps(new_question)
        res = self.client().post('/questions', data=json_data, content_type="application/json")
        data = json.loads(res.get_data(as_text=True))
        # print("Create data ===> ", data)
        # print("Create Question ===> ", Question.query.all())
        new_question_id = Question.query.filter_by(question='Sample Question').first().id
        self.assertEqual(data.get('created'), new_question_id)
        self.assertEqual(res.status_code, 201)

    
    def test_search_question(self):
        """Test that creates a question"""
        self.question1.delete()
        new_question = {
            "question": 'Sample Question', 
            'answer': 'Sample Answer', 
            'difficulty': '3', 
            'category': '2'
        }
        json_data1 = json.dumps(new_question)
        self.client().post('/questions', data=json_data1, content_type="application/json")
        search_term = {
            "searchTerm": "samp"
        }
        json_data2 = json.dumps(search_term)
        res = self.client().post('/questions', data=json_data2, content_type="application/json")
        data = json.loads(res.get_data(as_text=True))
        # print("Search data ===> ", data)
        self.client().delete('/questions/' + str(data.get('questions')[0].get("id")))
        # print("Create Question ===> ", Question.query.all())
        self.assertEqual(data.get('questions')[0].get("question"), "Sample Question")
        self.assertEqual(res.status_code, 200)


    def test_get_question_by_category(self):
        """Test that creates a question"""
        current_category = str(self.category1.id)
        category_url = '/categories/' + current_category + '/questions'
        # print("question1 category========> " + str(self.question1.category))
        # print(category_url)
        # print("self.question1.id: ", self.question1.id, self.question1.category)
        # print("=======> ", Question.query.filter_by(category=str(current_category)).all())
        res = self.client().get(category_url)
        data = json.loads(res.get_data(as_text=True))
        # print("get_by_category_data ====>", data)
        self.assertEqual(data.get('questions')[0].get('category'), current_category)
        self.assertEqual(res.status_code, 200)

    def test_get_quiz_questions(self):
        current_category = str(self.question1.category)
        payload_data = {'previous_questions': [], 
                        'quiz_category': 
                            {
                                'type': 'Sports', 
                                'id': current_category
                            }
                        }
        json_data = json.dumps(payload_data)
        res = self.client().post('/quizzes', data=json_data, content_type="application/json")
        # print("Question ID: ", Question.query.first().id) 
        data = json.loads(res.get_data(as_text=True))
        # pprint(data)
        self.assertEqual(data.get('question').get('category'), current_category)
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()