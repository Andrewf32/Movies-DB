from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db

from models.movies import MoviesSchema
from models.actors import ActorsSchema

class Characters(db.Model):
  __tablename__ = 'characters'
  char_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  char_name = db.Column(db.String(), nullable=False)
  char_alter_name = db.Column(db.String())
  char_role = db.Column(db.String(), nullable=False)
  actor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('actors.actor_id'), nullable=False)
  movie_id = db.Column(UUID(as_uuid=True), db.ForeignKey('movies.movie_id'), nullable=False)

  def __init__(self, char_name, char_alter_name, char_role, actor_id, movie_id):
    self.char_name = char_name
    self.char_alter_name = char_alter_name
    self.char_role = char_role
    self.actor_id = actor_id
    self.movie_id = movie_id

class CharactersSchema(ma.Schema):
  class Meta:
    fields = ['char_id', 'char_name', 'char_alter_name', 'char_role', 'actor', 'movie']

  actor = ma.fields.Nested(ActorsSchema(only=('actor_id', 'first_name', 'last_name')))
  movie = ma.fields.Nested(MoviesSchema(only=('movie_id', 'title', 'director')))

character_schema = CharactersSchema()
characters_schema = CharactersSchema(many=True)