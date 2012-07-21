# aux.py

import os

from google.appengine.ext import db
from google.appengine.datastore import entity_pb


is_development = os.environ['SERVER_SOFTWARE'].startswith('Development')

def serialize(models):
  if models is None:
    return None
  elif isinstance(models, db.Model):
    # Just one instance
    return db.model_to_protobuf(models).Encode()
  else:
    # A list
    return [db.model_to_protobuf(x).Encode() for x in models]

def deserialize(data):
  if data is None:
    return None
  elif isinstance(data, str):
    # Just one instance
    return db.model_from_protobuf(entity_pb.EntityProto(data))
  else:
    return [db.model_from_protobuf(entity_pb.EntityProto(x)) for x in data]


