# Casting Agency
Capstone Project for Udacity Full Stack Web Developer Nanodegree 

## About the project
[Casting Agency](https://fsnd-castingagency-2021.herokuapp.com/) is a fictional company that responsible for creating and managing movies and actors.

This project is a catalog for Casting Agency employees to manage movies and actors. Employees have different permission based on their roles.
- Casting Assistant
    - Can view actors, movies
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

This project is currently hosted at heroku and does not have a frontend.

### Background
This project is build to test and demonstrate the following skills:
- SQL and Data Modeling using SQLAlchemy
- Create web app using Flask
- Follow RESTful principles of API development
- Testing validity of API behavior and error handling
- Enable Role Based Authentication and roles-based access control (RBAC) in a Flask application
- Configure third-party authentication
- Deployment via Heroku
- Project Documentation
- All backend code follows PEP8 style guidelines


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to project directory and running:

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight the database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the app in local
Open a terminal session and activate the virtual environment.

This app need to be connected to a database.
Use the below command to create a database in local

```bash
sudo -u postgres -i
createdb <DATABASE_NAME>
```
My DATABASE_NAME is **capstone**

To set up environment variables, open 'setup.sh' and edit the following variables if you are using a different database name and if the token expires:

```
DATABASE_URL
CASTING_ASSISTANT_TOKEN
CASTING_DIRECTOR_TOKEN
EXECUTIVE_PRODUCER_TOKEN
```
To export the variables, run(GitBash):

```bash
source setup.sh
```

To initialize database, run:

```bash
flask db migrate
flask db upgrade
```

To run the flask application:

```bash
flask run --reload
```
The `--reload` flag will detect file changes and restart the server automatically.

## Unittests

Unittests are located in the `test_app.py`.

Before running tests, create the test database and make sure 'setup.sh' has proper values.

To export the variables, run(GitBash):

```bash
source setup.sh
```

To create tables in test database, uncomment line 17 in models.py

To run the tests, execute:

```bash
python test_app.py
```
### Postman
To test endpoints with [Postman](https://getpostman.com):

- Insert some records in movies and actors tables. 
- Please edit the actor_id, movie_id according to the id given by the database.
- Update the host in collection level variables to either local url or the one hosted in heroku.
- Also generate and update the tokens in collection level variables if old one expires.
- Run the capstone.postman_collection.json.

I have attached the test results in **_capstone.postman_test_run.json_**

## API Reference
### Getting Started
#### Base URL:
- The app is hosted at https://fsnd-castingagency-2021.herokuapp.com/
- When run locally, the backend app is hosted at the default http://127.0.0.1:5000/

#### API Keys /Authentication (if applicable):
  - This app use [Auth0](https://auth0.com/) for authentication.
  - Role Based Authentication and roles-based access control (RBAC) are enabled.
  - The jwt tokens are present in setup.sh and will expire on 23/08/2021 @ 10:00am (IST). 
  - If you need updated tokens use [this url](https://fsnano.us.auth0.com/authorize?audience=castingagency&response_type=token&client_id=8FPXsoo5jQrpLSiB8gVEYiAhIYVbfJqM&redirect_uri=http://localhost:5000) and below credentials to generate new tokens
    - Role|E-mail id|Password
      ---|---|---
      Casting Assistant| casting_assistant@gmail.com|@ss1stanT
      Casting Director| casting_director@gmail.com|D!recT0r
      Executive producer|executive_producer@gmail.com|proDuc3r*



### Error Handling
Errors are returned as JSON objects in one of the two following format:

**Failed request**
```
{
    "error": 404,
    "message": "resource not found",
    "success": false
}
```
**Authorization error**
```
{
    "code": "unauthorized",
    "description": "Permission not found."
}
```
A list of expected response code:

- 200: successful request
- 400: bad request
- 401: unauthorized
- 403: Forbidden
- 404: resource not found
- 405: method not found
- 422: unprocessable
- 500: Internal Server Error

### Endpoint library

#### [Movies]

#### GET /movies
- Get a list of movie entity in JSON format
- Curl sample:
    `curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/movies`
- Sample response:
```
    {
      "movies": [
        {
          "id": 1,
          "title" : "3 idiots",
          "release_date" : "2010-10-24"
        }
      ],
      "success": true
    }
```

#### POST /movies

- Add a movie entity to database
    - Movie has title and release_date
    - date must be in an expected form
        - `'%Y','%b %d, %Y','%b %d, %Y','%B %d, %Y','%B %d %Y','%m/%d/%Y','%m/%d/%y','%b %Y','%B%Y','%b %d,%Y',
          '%Y-%m-%d', '%y-%m-%d', '%m-%d-%Y', '%m-%d-$y'`
    - return new movie in JSON format
- Curl sample:
  `curl http://localhost:5000/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title" : "3 idiots", "release_date" : "2010-10-24"}`
- Sample Response:
```
    {
      "movies": {
          "id": 1,
          "title" : "3 idiots",
          "release_date" : "2010-10-24"
        }
      "success": true
    }
```

#### PATCH /movies/{movie_id}

- Edit an existing movie
    - date must be in an expected form
    - return edited movie in JSON format
- Sample curl:
  `curl http://localhost:5000/movies/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"release_date": "2010-10-18"}`
- Sample Response:
```
    {
      "movies": {
          "id": 1,
          "title" : "3 idiots",
          "release_date" : "2010-10-18"
        }
      "success": true
    }
```

#### DELETE /movies/{movie_id}

- Delete an existing actor entity from database
    - return the deleted actor info in JSON format
- Sample curl:
  `curl http://localhost:5000/movies/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"`
- Sample Response:
```
    {
      "success": true,
      "movie_id": 1
    }
```

#### [Actors]

#### GET /actors
Get a list of all actors in JSON format
- Curl sample:
  `curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/actors`
- Response sample:
```
   {
      "actors": [
        {
          "id": 1,
          "name": "theo james",
          "age": 37,
          "gender": "Male"
        }
      ],
      "success": true
   }
```

#### POST /actors
Add an actor entity to database
- actor has a name, age, gender, and a unique id assigned by database
- age must be an integer
- return the new actor entity in JSON format
- Curl sample:
  `curl http://localhost:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name": "theo james", "age": 37, "gender": "Male"}`
- Request sample:
```
    {
      "actors": {
          "id": 1,
          "name": "theo james",
          "age": 37,
          "gender": "Male"
        }
      "success": true
    }
```

#### PATCH /actors/{actor_id}
Edit an existing actor entity
- return the edited actor entity in JSON format
- Sample curl:
  `curl http://localhost:5000/actors/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"age": 40}`
- Sample response:
```
    {
      "actors": {
          "id": 1,
          "name": "theo james",
          "age": 40,
          "gender": "Male"
        }
      "success": true
    }
```

#### DELETE /actors/{actor_id}
Delete an existing actor entity from database
- return the deleted actor info in JSON format
- Sample curl:
  `curl http://localhost:5000/actors/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"`
- Example:
```
    {
      "success": true,
      "actor_id": 1
    }
```

Authors
Yours truly, Sourabi Kannan

Acknowledgements
The instructors, mentors, fellow students and entire team at Udacity.
