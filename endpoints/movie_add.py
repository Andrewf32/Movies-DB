# from flask import jsonify, request
# import flask
# from db import db

# from models.movies import Movies

# def add_movie(req:flask.Request):
#   form = request.form

#   fields = ["title", "description", "date_released", "director"]
#   req_fields = ["title", "director"]
#   values = []
  
#   for field in fields:
#     form_value = form.get(field)

#     if form_value in req_fields and form_value == " ":
#       return jsonify (f'{field} is required field'), 400

#     values.append(form_value)
  
#   title = form.get('title')
#   description = form.get('description')
#   date_released = form.get('date_released')
#   director = form.get('director')
  
#   new_movie = Movies(title, description, date_released, director)

#   db.session.add(new_movie)
#   db.session.commit()
  
#   return jsonify('Movie Added'), 200