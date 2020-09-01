import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr.init_model import app, db
from config import token_cast_assistant, token_cast_director, token_executive_producer
from flaskr.models import Actor, Movie
from sqlalchemy import desc


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_actor_success(self):  # 1
        result = self.app.get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(token_cast_assistant)})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'] is not None)

    def test_get_actor_fail(self):  # 2
        result = self.app.get('/actors')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details']['code'] == 'Header missing')

    def test_get_movie_success(self):  # 3
        result = self.app.get(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(token_cast_assistant)})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'] is not None)

    def test_get_movie_fail(self):  # 4
        result = self.app.get('/movies')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details']['code'] == 'Header missing')

    # 5 Casting Assistant cannot access post Actor
    def test_post_actor_permission_denied(self):
        json_data = {
            "first_name": "Albon",
            "last_name": "qwqwqw",
            "age": 27,
            "gender": "Male"
        }
        result = self.app.post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(token_cast_assistant)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details']['code'] == 'Not Permitted')

    def test_post_actor_success(self):  # 6
        json_data = {
            "first_name": "Albon",
            "last_name": "qwqwqw",
            "age": 27,
            "gender": "Male"
        }
        result = self.app.post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(token_cast_director)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'] > 0)

    def test_post_actor_failure(self):  # 7
        json_data = {
            "first_name": "Albon",
            "age": 27,
            "gender": "Male"
        }
        result = self.app.post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(token_cast_director)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details'] == 'Bad Request')

    # 8 Casting Director cannot access post Movies
    def test_post_movies_permission_denied(self):
        json_data = {
            "title": "A new movie4",
            "release_date": "2020-08-20 00:51:07",
            "actors_id": [1]
        }
        result = self.app.post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(token_cast_director)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details']['code'] == 'Not Permitted')

    def test_post_movie_success(self):  # 9
        with app.app_context():
            actor = Actor.query.filter_by(
                first_name='Albon').order_by(
                desc(
                    Actor.id)).first()

        json_data = {
            "title": "A new movie4",
            "release_date": "2020-08-20 00:51:07",
            "actors_id": [actor.id]
        }
        result = self.app.post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(token_executive_producer)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'] > 0)

    def test_post_movie_failure(self):  # 10
        json_data = {
            "title": "A new movie4",
            "actors_id": [1]
        }
        result = self.app.post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(token_executive_producer)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details'] == 'Bad Request')

    def test_delete_actor_failure(self):  # 11
        result = self.app.delete(
            '/actor/2048',
            headers={
                "Authorization": "Bearer {}".format(token_executive_producer)})
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details'] == 'Bad Request')

    def test_delete_actor_permission_denied(self):  # 12
        result = self.app.delete(
            '/actor/1',
            headers={
                "Authorization": "Bearer {}".format(token_cast_assistant)})
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details']['code'] == 'Not Permitted')

    def test_delete_actor_success(self):  # 13
        with app.app_context():
            actor = Actor.query.filter_by(
                first_name='Albon').order_by(
                desc(
                    Actor.id)).first()
        result = self.app.delete('/actor/{}'.format(actor.id),
                                 headers={"Authorization": "Bearer {}".format(token_executive_producer)})
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(int(data['deleted_actor_id']) > 0)

    def test_delete_movie_failure(self):  # 14
        result = self.app.delete(
            '/movie/2048',
            headers={
                "Authorization": "Bearer {}".format(token_executive_producer)})
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details'] == 'Bad Request')

    def test_delete_movie_permission_denied(self):  # 15
        result = self.app.delete(
            '/movie/1',
            headers={
                "Authorization": "Bearer {}".format(token_cast_director)})
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details']['code'] == 'Not Permitted')

    def test_delete_movie_success(self):  # 16
        with app.app_context():
            movie = Movie.query.filter_by(
                title='A new movie4').order_by(
                desc(
                    Movie.id)).first()
        result = self.app.delete('/movie/{}'.format(movie.id),
                                 headers={"Authorization": "Bearer {}".format(token_executive_producer)})
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(int(data['deleted_movie_id']) > 0)

    def test_update_movie_success(self):  # 17
        with app.app_context():
            movie = Movie.query.filter_by(
                title='A new movie4').order_by(
                desc(
                    Movie.id)).first()
        json_data = {
            "release_date": "2020-08-21 00:51:07"
        }
        result = self.app.patch(
            '/movie/{}'.format(
                movie.id),
            headers={
                "Authorization": "Bearer {}".format(token_executive_producer)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(int(data['updated_movie_id']) > 0)

    def test_update_movie_failure(self):  # 18
        json_data = {
            "release_date": "2020-08-21 00:51:07"
        }
        result = self.app.patch(
            '/movie/999',
            headers={
                "Authorization": "Bearer {}".format(token_executive_producer)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details'] == 'Bad Request')

    def test_update_actor_success(self):  # 19
        with app.app_context():
            actor = Actor.query.filter_by(
                first_name='Albon').order_by(
                desc(
                    Actor.id)).first()
        json_data = {
            "last_name": "Alex"
        }
        result = self.app.patch(
            '/actor/{}'.format(
                actor.id),
            headers={
                "Authorization": "Bearer {}".format(token_executive_producer)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(int(data['updated_actor_id']) > 0)

    def test_update_actor_failure(self):  # 20
        json_data = {
            "last_name": "Alex"
        }
        result = self.app.patch(
            '/actor/999',
            headers={
                "Authorization": "Bearer {}".format(token_executive_producer)},
            json=json_data)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['details'] == 'Bad Request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
