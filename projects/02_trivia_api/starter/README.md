# Trivia API

Trivia is a web application (hold trivia on a regular basis) to ask questions and play funny qizzes
 
The application features:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

![Untitled](https://user-images.githubusercontent.com/53627971/104937086-0ce22800-59b6-11eb-8d81-510a7f5c7201.png)

## Getting Started

### Prerequisites & Installation

#### Python 3.7
install python 3.7 version is a need (other versions cause problems) for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP installations

navigate to the `/backend` directory and run:

```bash
pip install -r requirements.txt
```

This will install all of the required packages in the `requirements.txt` file.
##### the basic dependencies

- Flask
- SQLAlchemy
- Flask-CORS

#### Database Setup

-make sure Postgres server is runing
Restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
### Running the server

From the `backend` directory, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

#### Frontend Dependencies

This project uses NPM to manage software dependencies. from the `frontend` directory run:

```bash
npm install
```

#### Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```
### Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## API Reference
### Getting Started

Base URL: trivia app can only run locally (not hosted)
* Backend Base URL: `http://127.0.0.1:5000/`
* Frontend Base URL: `http://127.0.0.1:3000/`

### Error Handling

Errors returned as object (json format):

```json
      {
        "success": "False",
        "error": 400,
        "message": "bad request structure",
      }
```

The error that will return when request fail:

* 400 – bad request structure
* 404 – resource not found
* 422 – requist unprocessable

### Endpoints

#### GET /categories
- General:
    -  return all available catgories exist in application
- sample: `curl http://127.0.0.1:5000/categories`

```json
    {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```
#### GET /questions
- General:
    - return a list of questions, number of total questions, current category, categories.
    - list of questions is paged in 10/page. Include argument choose page number starting from 1
- Sample: `curl http://127.0.0.1:5000/questions`

```json
    {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
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
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "totalQuestions": 33
}
```
#### DELETE /questions/<int:id\>
- General:
    - delte question using questinon id
- Sample: `curl http://127.0.0.1:5000/questions/5 -X DELETE`

```json
{
  "delted": 5,
  "success": true,
  "totalQuestions": 31
}
```
#### POST /questions
- General:
  - POST a new question,which will require the question and answer text,category, and difficulty score. 
  - can be used also in search depend on request content we send, if it was searchterm:"" it is search
  - for creation, return question we creat and its id
  - for search, return list of questions was found and if no questions, return empty list 
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{    "question": "where is your thoughts came?", "answer": "brain", "difficulty": 3, "category": "1" }'`

```json
{
    "created": 41,
    "question": {
        "answer": "brain",
        "category": 1,
        "difficulty": 3,
        "id": 41,
        "question": "where is your thoughts came?"
    },
    "success": true,
    "total_questions": 32
}
```
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "end"}'`

```json
{
    "currentCategory": null,
    "questions": [
        {
            "answer": "there is no end",
            "category": 4,
            "difficulty": 3,
            "id": 24,
            "question": "when we reach to the end?"
        }
    ],
    "success": true,
    "totalQuestions": 1
}
```

#### GET /categories/<int:id\>/questions

- General:
  - get questions based on category.
- Sample: `curl http://127.0.0.1:5000/categories/3/questions`

```json
{
  "currentCategory": 3,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Egypt",
      "category": 3,
      "difficulty": 1,
      "id": 40,
      "question": "where is nile?"
    }
  ],
  "success": true,
  "totalQuestions": 4
}
```
#### POST /quizzes
- General
  - get questions to play the quiz.
  - take category and previous question parameters 
  - return a random questions within the given category,if provided and not in previous questions.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9], "quiz_category": {"type": "History", "id": "4"}}'`

```json
{
    "question": {
        "answer": "Scarab",
        "category": 4,
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    "success": true
}
```
## Authors
- udacity nono-degree for full stack developers provide starter project (full front-end), basic backend and also how to setup and start project
- shimaa hamdy implment API for the project and also write documantion
