from .init_model import db

movie_actor = db.Table('movie_actor',
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('movie_id', db.Integer,
                                 db.ForeignKey('movie.id',
                                               ondelete='CASCADE')),
                       db.Column('actor_id', db.Integer,
                                 db.ForeignKey('actor.id',
                                               ondelete='CASCADE'))
                )


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    release_date = db.Column(db.DateTime)
    actors = db.relationship('Actor', secondary=movie_actor,
                             backref=db.backref('movies',
                             passive_deletes=True))
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.format() for actor in self.actors]
        }



class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender
        }

