import controllers
from flask import request, Response, Blueprint

actors = Blueprint('actors', __name__)

@actors.route("/actors", methods=["GET"])
def get_all_actors():
  return controllers.get_all_actors(request)

@actors.route("/actors/<actor_id>", methods=["GET"])
def get_actor_by_id(actor_id):
  return controllers.get_actors_by_id(request, actor_id)

@actors.route("/actors", methods=["POST"])
def add_actor():
  return controllers.add_actor(request)

@actors.route("/actors/<actor_id>", methods=["PUT"])
def edit_actor(actor_id):
  return controllers.edit_actor(request, actor_id)

@actors.route("/actors/<actor_id>", methods=["DELETE"])
def delete_actor(actor_id):
  return controllers.delete_actor(request, actor_id)