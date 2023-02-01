from flask import jsonify
import flask
from db import db

from models.actors import Actors, actors_schema, actor_schema
from util.reflection import populate_object


def get_all_actors(req:flask.Request):
  records = db.session.query(Actors).all()

  return jsonify({"message": "success", "results": actors_schema.dump(records)}), 200


def get_actor_by_id(req:flask.Request, actor_id):
  record = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()

  if record:
    return jsonify({"message": "actor found", "results": actor_schema.dump(record)}), 200

  return jsonify({"message": "actor not found", "results": actor_schema.dump(record)}), 404


def add_actor(req:flask.Request):
  post_data = req.get_json()
  if not post_data:
    post_data = request.form

  record = Actors.get_new_actor()
  populate_object(record, post_data)

  db.session.add(record)
  db.session.commit()
  
  return jsonify({"message": "actor added", "results": actor_schema.dump(record)}), 201


def edit_actor(req:flask.Request, actor_id):
  post_data = req.get_json()
  if not post_data:
    post_data = request.form

  record = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()

  if record:
    db.session.commit()
    return jsonify({"message": "actor updated", "results": actor_schema.dump(record)}), 201

  return jsonify({"message": "actor not found", "results": actor_schema.dump(record)}), 404
  

def delete_actor(req:flask.Request, actor_id):
  record = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()

  if not record:
    return jsonify("actor not found"), 404
    
  if record:
    db.session.delete(record)
    db.session.commit()

    return jsonify("record deleted"), 202