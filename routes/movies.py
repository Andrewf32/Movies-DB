import controllers
from flask import request, Response, Blueprint

movies = Blueprint('movies', __name__)

@movies.route("/movies", methods=["GET"])
def get_all_movies():
  return controllers.get_all_movies(request)

@movies.route("/movies/<movie_id>", methods=["GET"])
def get_movie_by_id(movie_id):
  return controllers.get_movies_by_id(request, movie_id)

@movies.route("/movies", methods=["POST"])
def add_movie():
  return controllers.add_movie(request)

@movies.route("/movies/<movie_id>", methods=["PUT"])
def edit_movie(movie_id):
  return controllers.edit_movie(request, movie_id)

# @movies.route("/movies/<movie_id>", methods=["PATCH"])
# def update_movie(movie_id):
#   return controllers.edit_movie(request, movie_id)

@movies.route("/movies/<movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
  return controllers.delete_movie(request, movie_id)