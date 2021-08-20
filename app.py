from werkzeug.exceptions import HTTPException

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from auth import requires_auth, AuthError
from models import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    return app


app = create_app()


@app.route('/')
def index():
    return "Welcome to capstone casting agency!"


@app.route('/movies')
@requires_auth('get:movies')
def view_movies(payload):
    try:
        movies = Movies.query.order_by(Movies.id).all()
        if len(movies) == 0:
            abort(404)
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })
    except Exception as e:
        handle_exception(e)


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_new_movie(payload):
    try:
        body = request.get_json()
        req_title = body.get('title', None)
        req_release_date = body.get('release_date', None)
        if req_title is None or req_title == '':
            abort(422)
        else:
            movie = Movies(title=req_title, release_date=req_release_date)
            movie.insert()
            return jsonify({
                "success": True,
                "movies": movie.format()
            })
    except Exception as e:
        handle_exception(e)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, movie_id):
    try:
        body = request.get_json()
        req_title = body.get('title', None)
        req_release_date = body.get('release_date', None)
        movie = Movies.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            if req_title is not None:
                movie.title = req_title
            if req_release_date is not None:
                movie.release_date = req_release_date
            movie.update()
            return jsonify({
                "success": True,
                "movies": movie.format()
            })
    except Exception as e:
        handle_exception(e)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    try:
        movie = Movies.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            movie.delete()
            return jsonify({
                "success": True,
                "movies": movie_id
            })
    except Exception as e:
        handle_exception(e)


@app.route('/actors')
@requires_auth('get:actors')
def view_actors(payload):
    try:
        actors = Actors.query.order_by(Actors.id).all()
        if len(actors) == 0:
            abort(404)
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })
    except Exception as e:
        handle_exception(e)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_new_actor(payload):
    try:
        body = request.get_json()
        req_name = body.get('name', None)
        req_age = body.get('age', None)
        req_gender = body.get('gender', None)
        if req_name is None or req_gender is None or req_name == '' or req_gender == '':
            abort(422)
        else:
            actor = Actors(name=req_name, age=req_age, gender=req_gender)
            actor.insert()
            return jsonify({
                "success": True,
                "movies": actor.format()
            })
    except Exception as e:
        handle_exception(e)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, actor_id):
    try:
        body = request.get_json()
        req_name = body.get('name', None)
        req_age = body.get('age', None)
        req_gender = body.get('gender', None)
        actor = Actors.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)
        else:
            if req_name is not None:
                actor.name = req_name
            if req_age is not None:
                actor.age = req_age
            if req_gender is not None:
                actor.gender = req_gender
            actor.update()
            return jsonify({
                "success": True,
                "movies": actor.format()
            })
    except Exception as e:
        handle_exception(e)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    try:
        actor = Actors.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)
        else:
            actor.delete()
            return jsonify({
                "success": True,
                "movies": actor_id
            })
    except Exception as e:
        handle_exception(e)


'''Handles the received exception which is If a HTTPException occurs will throw the same if 
some other exception is received 500 will be thrown. '''


def handle_exception(e):
    if isinstance(e, AuthError):
        raise e
    elif isinstance(e, HTTPException):
        abort(e.code)
    else:
        abort(500)


'''Error handler methods '''


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
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


@app.errorhandler(403)
def authentication_error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(403)
def authorization_error(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


''' error handler for AuthError '''


@app.errorhandler(AuthError)
def auth_error_handler(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
