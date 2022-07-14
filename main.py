from flask import request, Flask, jsonify
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID

from models.actors import Actors, actors_schema, actor_schema
from models.characters import Characters, characters_schema, character_schema
from models.movies import Movies, movies_schema, movie_schema

from db import db, init_db

app = Flask(__name__)

database_host = "127.0.0.1:5432"
database_name = "moviesdb"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{database_host}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
ma = Marshmallow(app)

def create_all():
  with app.app_context():
    db.create_all()

    print("Querying for Movie...")
    movie_data = db.session.query(Movies).filter(Movies.title == "Endgame").first()

    if movie_data == None:
      print("Endgame movie not found. Creating Endgame Movie Record in database...")

      endgame_description = 'After half of all life is snapped away by Thanos, the Avengers are left scattered and divided. Now with a way to reverse the damage, the Avengers and their allies must assemble once more and learn to put differences aside in order to work together and set things right.'
      
      movie_data = Movies('Endgame', endgame_description, 'April 26th 2019', 'Russo Brothers')

      db.session.add(movie_data)
      db.session.commit()
    else:
      print("Movies found!")

    print("Querying for Actors...")
    actor_data = db.session.query(Actors).filter(Actors.first_name == 'Robert').first()

    if actor_data == None:
      print("Actor not found. Creating record for Robert Downy Jr")
      
      actor_data = Actors('Robert', 'Downy Jr')

      db.session.add(actor_data)
      db.session.commit()
    else:
      print("Robert Downy Jr found!")

    
    print("Querying for Mr. Stark...")
    character_data = db.session.query(Characters).filter(Characters.char_name == 'Tony Stark').first()

    if character_data == None:
      actor_id = actor_data.actor_id
      movie_id = movie_data.movie_id

      print("Mr. Stark not found. Creating record for Mr. Stark")

      character_data = Characters('Tony Stark', "Ironman", "Hero", actor_id, movie_id)

      db.session.add(character_data)
      db.session.commit()
    else:
      print("Welcome back Mr. Stark...")


## MOVIES ##
@app.route('/movie/add', methods=['POST'])
def add_movie():
  form = request.form

  fields = ["title", "description", "date_released", "director"]
  req_fields = ["title", "director"]
  values = []
  
  for field in fields:
    form_value = form.get(field)

    if form_value in req_fields and form_value == " ":
      return jsonify (f'{field} is required field'), 400

    values.append(form_value)
  
  title = form.get('title')
  description = form.get('description')
  date_released = form.get('date_released')
  director = form.get('director')
  
  new_movie = Movies(title, description, date_released, director)

  db.session.add(new_movie)
  db.session.commit()
  
  return jsonify('Movie Added'), 200


@app.route('/movies/list', methods=['GET'])
def get_all_movies():
  movie_records = db.session.query(Movies).all()

  return jsonify(movies_schema.dump(movie_records)), 200


@app.route('/movie/get/<movie_id>', methods=['GET'])
def get_single_movie(movie_id):
  movie_record = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()

  return jsonify(movie_schema.dump(movie_record)), 200


@app.route('/movie/edit/<movie_id>', methods=['PUT'])
def edit_movie(movie_id, title=None, description=None, date_released=None, director=None):
  movie_record = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()

  if not movie_record:
    return ('Movie not found'), 404

  if request:
    form = request.form
    title = form.get('title')
    description = form.get('description')
    date_released = form.get('date_released')
    director = form.get('director')
  
  if title:
    movie_record.title = title
  if description:
    movie_record.description = description
  if date_released:
    movie_record.date_released = date_released
  if director:
    movie_record.director = director
  
  db.session.commit()

  return jsonify('Movie Updated'), 201


@app.route('/movie/delete/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
  movie_record = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()

  if not movie_record:
    return ('Movie not found'), 404
    
  if movie_record:
    db.session.delete(movie_record)
    db.session.commit()

    return ("Record Deleted"), 202
  

## ACTORS ##
@app.route('/actor/add', methods=['POST'])
def add_actor():
  form = request.form

  fields = ["first_name", "last_name"]
  req_fields = ["first_name"]
  values = []
  
  for field in fields:
    form_value = form.get(field)

    if form_value in req_fields and form_value == " ":
      return jsonify (f'{field} is required field'), 400

    values.append(form_value)
  
  first_name = form.get('first_name')
  last_name = form.get('last_name')
  
  new_actor = Actors(first_name, last_name)

  db.session.add(new_actor)
  db.session.commit()
  
  return jsonify('Actor Added'), 200


@app.route('/actors/list', methods=['GET'])
def get_all_actors():
  actor_records = db.session.query(Actors).all()

  return jsonify(actors_schema.dump(actor_records)), 200


@app.route('/actor/get/<actor_id>', methods=['GET'])
def get_single_actor(actor_id):
  actor_record = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()

  return jsonify(actor_schema.dump(actor_record)), 200


@app.route('/actor/edit/<actor_id>', methods=['PUT'])
def edit_actor(actor_id, first_name=None, last_name=None):
  actor_record = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()

  if not actor_record:
    return ('Actor not found'), 404

  if request:
    form = request.form
    first_name = form.get('first_name')
    last_name = form.get('last_name')
  
  if first_name:
    actor_record.first_name = first_name
  if last_name:
    actor_record.last_name = last_name
  
  db.session.commit()

  return jsonify('Actor Updated'), 201


@app.route('/actor/delete/<actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
  actor_record = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()

  if not actor_record:
    return ('Actor not found'), 404
    
  if actor_record:
    db.session.delete(actor_record)
    db.session.commit()

    return ("Record Deleted"), 202


## CHARACTERS ##
@app.route('/character/add', methods=['POST'])
def add_character():
  form = request.form

  fields = ["char_name", "char_alter_name", "char_role", "actor_id", "movie_id"]
  req_fields = ["char_name", "char_role", "actor_id", "movie_id"]
  values = []
  
  for field in fields:
    form_value = form.get(field)

    if form_value in req_fields and form_value == " ":
      return jsonify (f'{field} is required field'), 400

    values.append(form_value)
  
  char_name = form.get('char_name')
  char_alter_name = form.get('char_alter_name')
  char_role = form.get('char_role')
  actor_id = form.get('actor_id')
  movie_id = form.get('movie_id')

  new_character = Characters(char_name, char_alter_name, char_role, actor_id, movie_id)

  db.session.add(new_character)
  db.session.commit()
  
  return jsonify('Character Added'), 200


@app.route('/characters/list', methods=['GET'])
def get_all_characters():
  character_records = db.session.query(Characters).all()

  return jsonify(characters_schema.dump(character_records)), 200


@app.route('/character/get/<char_id>', methods=['GET'])
def get_single_character(char_id):
  character_record = db.session.query(Characters).filter(Characters.char_id == char_id).first()

  return jsonify(character_schema.dump(character_record)), 200


@app.route('/character/edit/<char_id>', methods=['PUT'])
def edit_character(char_id, char_name=None, char_alter_name=None, char_role=None, actor_id=None, movie_id=None):
  character_record = db.session.query(Characters).filter(Characters.char_id == char_id).first()

  if not character_record:
    return ('Character not found'), 404

  if request:
    form = request.form
    char_name = form.get('char_name')
    char_alter_name = form.get('char_alter_name')
    char_role = form.get('char_role')
    actor_id = form.get('actor_id')
    movie_id = form.get('movie_id')
  
  if char_name:
    character_record.char_name = char_name
  if char_alter_name:
    character_record.char_alter_name = char_alter_name
  if char_role:
    character_record.char_role = char_role
  if actor_id:
    character_record.actor_id = actor_id
  if movie_id:
    character_record.movie_id = movie_id
    
  db.session.commit()

  return jsonify('Character Updated'), 201


@app.route('/character/delete/<char_id>', methods=['DELETE'])
def delete_character(char_id):
  character_record = db.session.query(Characters).filter(Characters.char_id == char_id).first()

  if not character_record:
    return ('Character not found'), 404
    
  if character_record:
    db.session.delete(character_record)
    db.session.commit()

    return ("Record Deleted"), 202


## SEARCHING ##
@app.route('/movies/search/<search_term>', methods=['GET'])
def movies_search(search_term, internal_call=False):
  search_term = search_term.lower()

  movie_data = {}

  movie_data = db.session.query(Movies).filter(db.or_(db.func.lower(Movies.title).contains(search_term))).all()

  if internal_call:
    return movies_schema.dump(movie_data)
  
  return jsonify(movies_schema.dump(movie_data))


@app.route('/actors/search/<search_term>', methods=['GET'])
def actors_search(search_term, internal_call=False):
  search_term = search_term.lower()

  actor_data = {}

  actor_data = db.session.query(Actors).filter(db.or_( \
    db.func.lower(Actors.first_name).contains(search_term), \
    db.func.lower(Actors.last_name).contains(search_term)))

  if internal_call:
    return actors_schema.dump(actor_data)
  
  return jsonify(actors_schema.dump(actor_data))


@app.route('/characters/search/<search_term>', methods=['GET'])
def character_search(search_term, internal_call=False):
  search_term = search_term.lower()

  character_data = {}

  character_data = db.session.query(Characters).filter(db.or_( \
    db.func.lower(Characters.char_name).contains(search_term), \
    db.func.lower(Characters.char_alter_name).contains(search_term), \
    db.func.lower(Characters.char_role).contains(search_term)
    ))

  if internal_call:
    return characters_schema.dump(character_data)
  
  return jsonify(characters_schema.dump(character_data))

@app.route('/search/<search_term>', methods=['GET'])
def search_all(search_term):
  search_term = search_term.lower()

  search_results = {}
  search_results['actors'] = actors_search(search_term, True)
  search_results['actors'] = actors_search(search_term, True)
  search_results['actors'] = character_search(search_term, True)

  return jsonify(search_results)

if __name__ == '__main__':
  create_all()
  app.run()
