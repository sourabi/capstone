import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from app import create_app


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_URL_TEST')
        setup_db(self.app, self.database_path)

        # auth tokens for respective roles
        self.casting_assistant = {
            "Authorization": "Bearer {}".format(os.environ.get('CASTING_ASSISTANT_TOKEN'))
        }
        self.casting_director = {
            "Authorization": "Bearer {}".format(os.environ.get('CASTING_DIRECTOR_TOKEN'))
        }
        self.executive_producer = {
            "Authorization": "Bearer {}".format(os.environ.get('EXECUTIVE_PRODUCER_TOKEN'))
        }
        self.new_actor = {
            "id": "1",
            "name": "Jennifer Aniston",
            "age": "45",
            "gender": "Female"
        }
        self.new_movie = {
            "id": "1",
            "title": "divergent",
            "release_date": "2014-04-11"
        }
        self.data_setup()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def data_setup(self):
        self.client().post('/movies', headers=self.executive_producer, json=self.new_movie)
        self.client().post('/movies', headers=self.executive_producer, json=self.new_movie)
        self.client().post('/actors', headers=self.casting_director, json=self.new_actor)
        self.client().post('/actors', headers=self.casting_director, json=self.new_actor)

    # sample endpoint test
    def test_index(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    '''
     POST /movies and /actors
    '''
    def test_post_movies(self):
        res = self.client().post('/movies', headers=self.executive_producer, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Using RBAC ROLE testing here, casting_director doesnt have permission to create a movie.
    def test_failed_post_movies_403(self):
        res = self.client().post('/movies', headers=self.casting_director, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_post_actors(self):
        res = self.client().post('/actors', headers=self.casting_director, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_failed_post_actors_422(self):
        res = self.client().post('/actors', headers=self.casting_director, json={"name":""})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    '''
     PATCH /movies and /actors
    '''
    def test_patch_movies(self):
        res = self.client().patch('/movies/2', headers=self.casting_director, json={"title": "insurgent"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_failed_patch_movies_404(self):
        res = self.client().patch('/movies/50', headers=self.executive_producer, json={"title": "insurgent"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_actors(self):
        res = self.client().patch('/actors/2', headers=self.casting_director, json={"name": "cox"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Using RBAC ROLE testing here, casting_assistant doesnt have permission to update an actor.
    def test_failed_patch_actors_403(self):
        res = self.client().patch('/actors/2', headers=self.casting_assistant, json={"name": "cox"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    '''
     GET /movies and /actors
    '''
    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_failed_get_movies_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_failed_get_actors_401(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer random characters invalid token"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')
        self.assertEqual(data['description'], 'Authorization header must be bearer token.')

    '''
     DELETE /movies and /actors
    '''
    def test_delete_movies(self):
        res = self.client().delete('/movies/1', headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])

    # Using RBAC ROLE testing here ,casting_director doesnt have permission to delete a movie.
    def test_failed_delete_movies_403(self):
        res = self.client().delete('/movies/1', headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])

    # Using RBAC ROLE testing here, casting_assistant doesnt have permission to delete a actor.
    def test_failed_delete_actors_403(self):
        res = self.client().delete('/actors/1', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
