from flask import Blueprint
from flask import Flask, render_template, request, Response, redirect, jsonify, abort
from .models import Actor, Movie
from .init_model import db
from .auth import AuthError, requires_auth

movie_bp = Blueprint('movie_bp', __name__,
                        template_folder='templates')

@movie_bp.route('/movies', methods=['POST'])
@requires_auth('add: movies')
def post_movies(jwt):
    if request.method=='POST':
        body = request.get_json()
        if not body or not body.get('title') or not body.get('release_date'):
            abort(400)

        movie = Movie(
            title=body.get('title'),
            release_date=body.get('release_date')
        )
        if body.get('actors_id'):
            actor = Actor.query.filter(Actor.id.in_(body.get('actors_id'))).all()
            if not actor:
                abort(400)
            movie.actors=actor
        
        try:
            db.session.add(movie)
            db.session.commit()
            response = jsonify({
                'success':True,
                'id': movie.id
            })
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
            return response
            

@movie_bp.route('/movies', methods=['GET'])
@requires_auth('get:actors-movies')
def get_movies(jwt):
    try:
        movies = Movie.query.all()
        response_body = []
        for movie in movies:
            actors = movie.actors
            actors_json = []
            for actor in actors:
                actors_json.append({
                'id': actor.id,
                'first_name': actor.first_name,
                'last_name': actor.last_name,
                'age': actor.age,
                'gender': actor.gender
            })
            response_body.append({
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date,
                'actors': actors_json
            })
    except:
        abort(500)
    return jsonify({
        'success': True,
        'movies': response_body
    })

@movie_bp.route('/movie/<id>', methods=['DELETE'])
@requires_auth('delete: movies')
def delete_movies(jwt,id):
    if request.method=='DELETE':
        movie = Movie.query.get(int(id))
        if not movie:
            abort(400)
        db.session.delete(movie)
        db.session.commit()
        return jsonify({
            'success': True,
            'deleted_movie_id': id
        })
@movie_bp.route('/movie/<id>', methods=['PATCH'])
@requires_auth('modify: movies')
def modify_movies(jwt,id):
        changed=False
        movie = Movie.query.get(int(id))
        body = request.get_json()
        if not movie or not body:
            abort(400)
        if body.get('title'):
            movie.title=body.get('title')
            changed=True
        if body.get('release_date'):
            movie.release_date=body.get('release_date')
            changed=True
        if changed==False:
            abort(400)
        db.session.commit()
        return jsonify({
            'success': True,
            'updated_movie_id': id
        })      