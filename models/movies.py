from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db

class Movies(db.Model):
  __tablename__ = 'movies'
  movie_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  title = db.Column(db.String(), nullable=False, unique=True)
  description = db.Column(db.String())
  date_released = db.Column(db.String())
  director = db.Column(db.String(), nullable=False)
  character = db.relationship('Characters', cascade='all,delete', backref='movie', lazy=True)

  def __init__(self, title, description, date_released, director):
    self.title = title
    self.description = description
    self.date_released = date_released
    self.director = director

class MoviesSchema(ma.Schema):
  class Meta:
    fields = ['movie_id', 'title', 'description', 'date_released', 'director']
  

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)