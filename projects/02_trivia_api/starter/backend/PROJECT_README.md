# Trivia - Backend API 

The Full Stack Trivia API project serves as the backend for the Udacity Trivia application which was developed to increase bonding experiences for its employees and students.

The Full Stack Trivia API backend will allow the employees and students that use the Trivia application to perform the following:

- View all Categories and corresponding questions that are currently in the Trivia Database.
- Play Trivia based on Category
- Add new Questions and Answers to the Trivia Database based on Category
- Delete Questions and Answers from the Trivia Database
- Search for questions based on substrings that may be contained within.

## Getting Started

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

To run the application, navigate to the ./backend/flaskr directory and run the following commands::

```bash
export FLASK_APP=flaskr
flask run
```

## API Usage

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/

- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:

- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

### API Data Payload

All data payloads that are sent will be in JSON format.

```
{
    "sample_key": "sample_value"
}
```

### API Endpoint Library

The following API endpoints are outlined with sample request/response payloads.

#### GET /questions

- General:
    - Returns a JSON object containing the question categories, current category, questions, and number of total questions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: 
    - Default request which retrieves the first page of results: curl http://127.0.0.1:5000/questions
    - Optional request to retrive an additional page. In this case, page 2: curl http://127:0.0.1:5000/questions?page=2
        - Request Payload: None

        - Response Payload:
            ```
            {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "current_category": 4, 
            "questions": [
                {
                "answer": "Maya Angelou", 
                "category": 4, 
                "difficulty": 2, 
                "id": 5, 
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                } ], 
            "total_questions": 1
                
            ```

#### POST /questions

- General:
    - Endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
        - Create New Question: 
            - Request Payload
            ```
            {
                'question': 'Sample Question', 
                'answer': 'Sample Answer', 
                'difficulty': '3', 
                'category': '2'
            }
            ```
            - Response Payload - Returns the ID of the newly created question, paginated list of questions, success boolean, and
                                 the total number of questions in the database.
            ```
            {
                "created": 29,
                "questions": [
                    {
                        "answer": "Apollo 13",
                        "category": 5,
                        "difficulty": 4,
                        "id": 2,
                        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                    }

                    ... 

                    {
                        "answer": "Agra",
                        "category": 3,
                        "difficulty": 2,
                        "id": 15,
                        "question": "The Taj Mahal is located in which Indian city?"
                    }
                ],
                "success": true,
                "total_questions": 23
            }
            ```


        - Search for an existing question:
            - Request Payload - The substring on which to search.

            ```
            {
                'searchTerm': 'samp'
            }
            ```
            - Response Payload - Returns a list of questions containing the requested substring, case-insensitive
            ```
            [
                {
                    'id': 27, 
                    'question': 'Sample Question', 
                    'answer': 'Sample Answer', 
                    'category': 2, 
                    'difficulty': 3
                }
            ]
            ```

#### GET /categories/\<int:category_id\>/questions

- General:
    - Endpoint to get a paginated list of all questions from a given category by id.
        - Request Payload: None

        - Response Payload: To retrieve from the Sports category, which has an ID of 6
        ```
        {
            "current_category": 6, 
            "questions": [
                    {
                        "answer": "Brazil", 
                        "category": 6, 
                        "difficulty": 3, 
                        "id": 10, 
                        "question": "Which is the only team to play in every soccer World Cup tournament?"
                    }, 
                    {
                        "answer": "Uruguay", 
                        "category": 6, 
                        "difficulty": 4, 
                        "id": 11, 
                        "question": "Which country won the first ever soccer World Cup in 1930?"
                    }, 
                    {
                        "answer": "Muhammad Ali", 
                        "category": 6, 
                        "difficulty": 1, 
                        "id": 24, 
                        "question": "What did the famous boxer Cassius Clay change his name to?"
                    }
                ], 
                "success": true, 
                "total_questions": 3
        }

#### POST /quizzes

- General:
    - A POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters 
      and return a random questions within the given category, if provided, and that is not one of the previous questions. 
        - POST to get a new quiz question: 
            - Request Payload:
            ```
            {
                'previous_questions': [], 
                'quiz_category': 
                    {
                        'type': 'Sports', 
                        'id': '6'
                    }
            }
            ```
            - Response Payload:
            ```
            {
              'question': "What did the famous boxer Cassius Clay change his name to?"
            }