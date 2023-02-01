from flask import request, Flask, jsonify
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from models.actors import Actors, actors_schema, actor_schema
from models.characters import Characters, characters_schema, character_schema
from models.movies import Movies, movies_schema, movie_schema
import routes

from db import db, init_db
from os.path import abspath, dirname, isfile, join

def create_all():
  with app.app_context():

    print("Querying for Movie...")
    movie_data = db.session.query(Movies).filter(Movies.title == "Endgame").first()

    if movie_data == None:
      print("Broken in movies")
      print("Endgame movie not found. Creating Endgame Movie Record in database...")

      endgame_description = 'After half of all life is snapped away by Thanos, the Avengers are left scattered and divided. Now with a way to reverse the damage, the Avengers and their allies must assemble once more and learn to put differences aside in order to work together and set things right.'
      
      movie_data = Movies('Endgame', endgame_description, 'Russo Brothers')

      db.session.add(movie_data)
      db.session.commit()
    else:
      print("Movies found!")

    print("Querying for Actors...")
    actor_data = db.session.query(Actors).filter(Actors.first_name == 'Robert').first()

    if actor_data == None:
      print("Broken in actor Data")

      print("Actor not found. Creating record for Robert Downy Jr")
      
      actor_data = Actors('Robert', 'Downy Jr')

      db.session.add(actor_data)
      db.session.commit()
    else:
      print("Robert Downy Jr found!")

    
    print("Querying for Mr. Stark...")
    character_data = db.session.query(Characters).filter(Characters.char_name == 'Tony Stark').first()

    if character_data == None:
      print("Broken in character Data")
      actor_id = actor_data.actor_id
      print(actor_id)
      movie_id = movie_data.movie_id
      print(movie_id)

      print("Mr. Stark not found. Creating record for Mr. Stark")

      character_data = Characters('Tony Stark', "Ironman", "Hero", actor_id, movie_id)

      db.session.add(character_data)
      db.session.commit()
    else:
      print("Welcome back Mr. Stark...")


def create_app(config_file=None):
   app = Flask(__name__)
   database_host = "127.0.0.1:5432"
   database_name = "moviesdb"
   app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres://{database_host}/{database_name}'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
   init_db(app, db)

   current_dir = dirname(abspath(__file__))
   if config_file is None:
      config_file = abspath(join(current_dir, '../config/config.yml'))
   else:
      config_file = abspath(config_file)

   cfg = app.config
   app.env = cfg.get('ENVIRONMENT', 'development')
   if app.debug:
      app.live = False
      if app.env == 'test':
         app.testing = True
      elif app.env == 'development':
         app.dev = True
      else:
         raise EnvironmentError('Invalid environment for app state. (Look inside __init__.py for help)')
   else:
      if app.env == 'production':
         app.live = True
      elif app.env == 'development':
         app.live = False
         app.testing = False
      else:
         raise EnvironmentError('Invalid environment for app state. (Look inside __init__.py for help)')
   return app


app = create_app()
bcrypt = Bcrypt(app)
CORS(app)
ma  = Marshmallow(app)

app.register_blueprint(routes.actors)
app.register_blueprint(routes.movies)
app.register_blueprint(routes.characters)


if __name__ == "__main__":
    create_all()
    app.run(debug=True)