from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db

class Actors(db.Model):
  __tablename__ = 'actors'
  actor_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  first_name = db.Column(db.String(), nullable=False)
  last_name = db.Column(db.String())
  character = db.relationship('Characters', cascade='all,delete', backref='actor', lazy=True)

  def __init__(self, first_name, last_name):
    self.first_name = first_name
    self.last_name = last_name


class ActorsSchema(ma.Schema):
  class Meta:
    fields = ['actor_id', 'first_name', 'last_name']

actor_schema = ActorsSchema()
actors_schema = ActorsSchema(many=True)