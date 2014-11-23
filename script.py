from sqlalchemy import *
import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
 

 
class Place(Base):
    __tablename__ = 'place'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(50), nullable=False)

 class Comment(Base):
    __tablename__ = 'comment'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    locationIP = Column(String(20), nullable=False)
    browserUsed = Column(String(20), nullable=False)
    creationDate = Column(DateTime, nullable=False)
    content = Column(String(250), nullable=False)
    length = Column(Integer, nullable=False)
    creator_id = Column(BigInteger, ForeignKey('person.id'))
    person = relationship(Person)
    location_id = Column(BigInteger, ForeignKey('place.id'))
    place = relationship(Place)
    

 class Forum(Base):
    __tablename__ = 'forum'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    title = Column(String(50), nullable=False)
    creationDate = Column(DateTime, nullable=False)

 class Organisation(Base):
    __tablename__ = 'organisation'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(250), nullable=False)
    type = Column(String(10), nullable=False)
    
class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    locationIP = Column(String(20), nullable=False)
    browserUsed = Column(String(20), nullable=False)
    creationDate = Column(DateTime, nullable=False)
    birthday = Column(Date, nullable=False)

class Place(Base):
    __tablename__ = 'place'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    url = Column(String(250), nullable=False)
    type = Column(String(10), nullable=False)

class TagClass(Base):
    __tablename__ = 'tagclass'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    url = Column(String(250), nullable=False)

class Tag(Base):
    __tablename__ = 'tag'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    url = Column(String(250), nullable=False)

class PersonSpeaksLanguage(Base):
    __tablename__ = 'person_speaks_language'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(BigInteger, ForeignKey('person.id'))
    person = relationship(Person)
    email = Column(String(100), nullable=False)

class PersonEmailAddress(Base):
    __tablename__ = 'person_email_emailaddress'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(BigInteger, ForeignKey('person.id'))
    person = relationship(Person)
    language = Column(String(5), nullable=False)
    
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
