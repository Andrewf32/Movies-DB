from flask import jsonify
import flask
from db import db

from models.characters import Characters, characters_schema, character_schema
from util.reflection import populate_object


def get_all_characters(req:flask.Request):
  records = db.session.query(Characters).all()

  return jsonify({"message": "success", "results": characters_schema.dump(records)}), 200


def get_character_by_id(req:flask.Request, char_id):
  record = db.session.query(Characters).filter(Characters.char_id == char_id).first()

  if record:
    return jsonify({"message": "character found", "results": character_schema.dump(record)}), 200

  return jsonify({"message": "character not found", "results": character_schema.dump(record)}), 404


def add_character(req:flask.Request):
  post_data = req.get_json()
  if not post_data:
    post_data = request.form

  record = Characters.get_new_character()
  populate_object(record, post_data)

  db.session.add(record)
  db.session.commit()
  
  return jsonify({"message": "character added", "results": character_schema.dump(record)}), 201


def edit_character(req:flask.Request, char_id):
  post_data = req.get_json()
  if not post_data:
    post_data = request.form

  record = db.session.query(Characters).filter(Characters.char_id == char_id).first()

  if record:
    db.session.commit()
    return jsonify({"message": "character updated", "results": character_schema.dump(record)}), 201

  return jsonify({"message": "character not found", "results": character_schema.dump(record)}), 404
  

def delete_character(req:flask.Request, char_id):
  record = db.session.query(Characters).filter(Characters.char_id == char_id).first()

  if not record:
    return jsonify("character not found"), 404
    
  if record:
    db.session.delete(record)
    db.session.commit()

    return jsonify("record deleted"), 202