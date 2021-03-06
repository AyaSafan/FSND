# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT

This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

## Error Handeling
Errors are returned as JSON oblects in the following format:
```
{
	"success": False, 
	"error": 400,
	"message": "Bad request"
}
```

The API will return four error types when te request fails:
* 400: Bad Request
* 404: Not Fount
* 422: unprocessable
* 500: Internal Server Error


## Endpoints
### GET /categories
* General

	- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
	- Request Arguments: None
	- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

* Example
```
curl --location --request GET 'http://127.0.0.1:5000/categories'
```
* Response

```
{
	'1' : "Science",
	'2' : "Art",
	'3' : "Geography",
	'4' : "History",
	'5' : "Entertainment",
	'6' : "Sports"
}

```

### GET /questions?page=<int:number>
* General

	- Fetches a paginated dictionary of questions from all categories
	- Request Arguments: None
	- Returns: An object containing a list of questions, number of total questions, current category, categories. 

* Example
```
curl --location --request GET 'http://127.0.0.1:5000/questions?page=2'
```
* Response

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
  "current_category": null, 
  "questions": [
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
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}

```
### DELETE /questions/<int:question_id>
* General

	- Deletes an existing question 
	- Request Arguments: int:question_id
	- Returns: An object containing success boolean value and deleted question id.

* Example
```
curl --location --request DELETE 'http://127.0.0.1:5000/questions/2'
```
* Response


```
{
	'success': True,
	'deleted': 2 
}

```

### POST /questions
* General

	- Creates a new question 
	- Request Arguments: {"question":string, "answer":string, "difficulty":int, "category":string}
	- Returns: An object containing success boolean value and created question id.

* Example

```
curl --location --request POST 'http://127.0.0.1:5000/questions' \
--header 'Content-Type: application/json' \
--data-raw '{  "question": "new question",  "answer": "answer", "difficulty": 1, "category": 1  }'
```
* Response

```
{
	'success': True,
	'created': 24 
}

```

### POST /questions/search
* General

	- Fetchs questions based on a search term. It returns any questions for whom the search term is a substring of the question. 
	- Request Arguments: {"searchTerm":string}
	- Returns: An object containing success boolean value, a list of questions, number of total questions, and current category. 


* Example

```
curl --location --request POST 'http://127.0.0.1:5000/questions/search' \
--header 'Content-Type: application/json' \
--data-raw '{"searchTerm":"tom"}'
```
* Response

```
{
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true,
    "total_questions": 1
}

```

### GET /categories/<int:category_id>/questions
* General

	- Fetchs questions based on category. 
	- Request Arguments: int:category_id
	- Returns: An object containing success boolean value, a list of questions, number of total questions, and current category. 
	
* Example
```
curl --location --request GET 'http://127.0.0.1:5000/categories/2/questions'
```
*Response

```
{
  "current_category": {
    "id": 2, 
    "type": "Art"
  }, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}

```

### POST /quizzes
* General

	- Fetchs uestions to play the quiz. It takes category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.  
	- Request Arguments: {"previous_questions": [], "quiz_category": {"id":int, "type":string}}
	- Returns: An object containing success boolean value, and question object.

* Example

```
curl --location --request POST 'http://127.0.0.1:5000/quizzes' \
--header 'Content-Type: application/json' \
--data-raw '{"quiz_category": {"id": 1, "type":"Science"}, "previous_questions":[]}'
```

* Response

```
{
    "question": {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    "success": true
}


```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
