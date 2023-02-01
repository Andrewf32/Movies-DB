import controllers
from flask import request, Response, Blueprint

characters = Blueprint('characters', __name__)

@characters.route("/characters", methods=["GET"])
def get_all_characters():
  return controllers.get_all_characters(request)

@characters.route("/characters/<char_id>", methods=["GET"])
def get_character_by_id(char_id):
  return controllers.get_characters_by_id(request, char_id)

@characters.route("/characters", methods=["POST"])
def add_character():
  return controllers.add_character(request)

@characters.route("/characters/<char_id>", methods=["PUT"])
def edit_character(char_id):
  return controllers.edit_character(request, char_id)

@characters.route("/characters/<char_id>", methods=["DELETE"])
def delete_character(char_id):
  return controllers.delete_character(request, char_id)