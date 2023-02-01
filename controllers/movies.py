from flask import jsonify
import flask
from db import db

from models.movies import Movies, movies_schema, movie_schema
from util.reflection import populate_object


def get_all_movies(req:flask.Request):
  records = db.session.query(Movies).all()

  return jsonify({"message": "received records", "results": movies_schema.dump(records)}), 200


def get_movie_by_id(req:flask.Request, movie_id):
  record = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()

  if record:
    return jsonify({"message": "movie found", "results": movie_schema.dump(record)}), 200

  return jsonify({"message": "movie not found", "results": movie_schema.dump(record)}), 404


def add_movie(req:flask.Request):
  post_data = req.get_json()
  if not post_data:
    post_data = request.form

  record = Movies.get_new_movie()
  populate_object(record, post_data)

  db.session.add(record)
  db.session.commit()
  
  return jsonify({"message": "movie added", "results": movie_schema.dump(record)}), 201


def edit_movie(req:flask.Request, movie_id):
  post_data = req.get_json()
  if not post_data:
    post_data = request.form

  record = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()

  if record:
    db.session.commit()
    return jsonify({"message": "movie updated", "results": movie_schema.dump(record)}), 201

  return jsonify({"message": "movie not found", "results": movie_schema.dump(record)}), 404
  

def delete_movie(req:flask.Request, movie_id):
  record = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()

  if not record:
    return jsonify("movie not found"), 404
    
  if record:
    db.session.delete(record)
    db.session.commit()

    return jsonify("record deleted"), 202