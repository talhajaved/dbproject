from declarative import Base, Place, Continent, Country, City
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import csv

engine = create_engine('sqlite:///example.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_place = Place(id=100)
session.add(new_place)
session.commit()

session.close()
