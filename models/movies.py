from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db


class Movies(db.Model):
  __tablename__ = 'Movies'
  movie_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  title = db.Column(db.String(), nullable=False, unique=True)
  description = db.Column(db.String())
  director = db.Column(db.String(), nullable=False)

  def __init__(self, title, description, director):
    self.title = title
    self.description = description
    self.director = director

  def get_new_movie():
    return Movies("", "", "")

class MoviesSchema(ma.Schema):
  class Meta:
    fields = ['movie_id', 'title', 'description', 'director', 'character']

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)