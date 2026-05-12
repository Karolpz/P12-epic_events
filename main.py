from models.base import Base, engine
from models import Collaborator, Client, Contract, Event

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


