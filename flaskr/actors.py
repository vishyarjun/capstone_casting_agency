from flask import Blueprint
from flask import (
    Flask,
    render_template,
    request, Response,
    redirect,
    jsonify,
    abort
)
from .models import Actor, Movie
from .init_model import db
from .auth import AuthError, requires_auth

actor_bp = Blueprint('actor_bp', __name__, template_folder='templates')


@actor_bp.route('/actors', methods=['POST'])
@requires_auth('add: actors')
def post_actors(jwt):
    if request.method == 'POST':
        body = request.get_json()
        response = {}
        if (not body or not body.get('first_name') or
            not body.get('last_name') or not body.get('age') or
                not body.get('gender')):
            abort(400)
        actor = Actor(
            first_name=body.get('first_name'),
            last_name=body.get('last_name'),
            age=body.get('age'),
            gender=body.get('gender')
        )
        if body.get('movies_id'):
            movies = Movie.query.filter(
                Movie.id.in_(body.get('movies_id'))).all()
            actor.movies = movies
        try:
            actor.insert()
            response = jsonify({
                'success': True,
                'id': actor.id
            })
        except BaseException:
            db.session.rollback()
            abort(500)
        db.session.close()
        return response


@actor_bp.route('/actors', methods=['GET'])
@requires_auth('get:actors-movies')
def get_actors(jwt):
    try:
        actors = Actor.query.all()
        response_body = []
        for actor in actors:
            response_body.append(actor.format())
    except BaseException:
        abort(500)
    return jsonify({
        'success': True,
        'actors': response_body
    })


@actor_bp.route('/actor/<id>', methods=['DELETE'])
@requires_auth('delete: actors')
def delete_actors(jwt, id):
    if request.method == 'DELETE':
        actor = Actor.query.get(int(id))
        if actor is None:
            abort(400)
        else:
            actor.delete()
            return jsonify({
                'success': True,
                'deleted_actor_id': id
            })


@actor_bp.route('/actor/<id>', methods=['PATCH'])
@requires_auth('modify: actors')
def modify_actors(jwt, id):
    changed = False
    actor = Actor.query.get(int(id))
    if actor is None:
        abort(400)
    body = request.get_json()
    if body.get('first_name'):
        changed = True
        actor.first_name = body.get('first_name')
    if body.get('last_name'):
        changed = True
        actor.last_name = body.get('last_name')
    if body.get('age'):
        changed = True
        actor.age = body.get('age')
    if body.get('gender'):
        changed = True
        actor.gender = body.get('gender')
    if changed is False:
        abort(400)
    actor.update()
    return jsonify({
        'success': True,
        'updated_actor_id': id
    })
