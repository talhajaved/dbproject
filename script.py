from sqlalchemy import *
import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import relationship

Base = declarative_base()
 


    
class Place(Base):
    __tablename__ = 'place'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    url = Column(String(250), nullable=False)
    type = Column(String(10), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'place',
        'polymorphic_on':type
    }
    
class Continent(Place):
    __tablename__ = 'continent'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, ForeignKey('place.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'continent',
    }

class Country(Place):
    __tablename__ = 'country'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, ForeignKey('place.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'country',
    }
    isPartOf = Column(BigInteger, ForeignKey('continent.id'),nullable=False)
    continent = relationship(Continent)

class City(Place):
    __tablename__ = 'city'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, ForeignKey('place.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'city',
    }
    isPartOf = Column(BigInteger, ForeignKey('country.id'),nullable=False)
    country = relationship(Country)

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    gender = Column(String(10))
    locationIP = Column(String(20))
    browserUsed = Column(String(20))
    creationDate = Column(DateTime)
    birthday = Column(Date, nullable=False)
    workAt = relationship('PersonWorksAt')
    studyAt = relationship('PersonStudiesAt')
    workAt = relationship('PersonKnows')
    likes = relationship('PersonLikesMessage')
    hasInterest  = relationship('Tag', secondary='person_has_interest')
    isMemberOf  = relationship('Forum', secondary='forum_has_member')
    isLocatedIn = Column(BigInteger, ForeignKey('city.id'),nullable=False)
    city  = relationship(City)

class Forum(Base):
    __tablename__ = 'forum'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    title = Column(String(50))
    creationDate = Column(DateTime)
    hasModerator = Column(BigInteger, ForeignKey('person.id'),nullable= False)
    person = relationship(Person)
    hasTag  = relationship('Tag', secondary='forum_has_tag')
    hasMember  = relationship('Person', secondary='forum_has_member')
    
class Message( Base):
    __tablename__ = 'message'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    locationIP = Column(String(20))
    browserUsed = Column(String(20))
    creationDate = Column(DateTime)
    length = Column(Integer)
    content = Column(String(250))
    type = Column(String(10), nullable=False)
    likedBy = relationship('PersonLikesMessage')
    hasCreator = Column(BigInteger, ForeignKey('person.id'),nullable= False)
    person = relationship(Person)
    isLocatedIn = Column(BigInteger, ForeignKey('country.id'),nullable=False)
    country = relationship(Country)
    __mapper_args__ = {
        'polymorphic_identity':'message',
        'polymorphic_on':type
    }

class Comment(Message):
    __tablename__ = 'comment'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, ForeignKey('message.id'),primary_key=True)
    replyOfId = Column(BigInteger, ForeignKey('message.id'),nullable=False)
    __mapper_args__ = {
        'polymorphic_identity':'comment',
        'inherit_condition':(id == Message.id)
    }

class Post(Message):
    __tablename__ = 'post'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    language = Column(String(250))
    imageFile = Column(String(250))
    forumId = Column(BigInteger, ForeignKey('forum.id'),nullable= False)
    forum  = relationship(Forum)
    id = Column(BigInteger, ForeignKey('message.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'post',
    }
    
class Organisation(Base):
    __tablename__ = 'organisation'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(250), nullable=False)
    type = Column(String(10), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'organisation',
        'polymorphic_on':type
    }

class University(Organisation):
    __tablename__ = 'university'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, ForeignKey('organisation.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'university',
    }
    person = relationship('PersonStudiesAt')
    isLocatedIn = Column(BigInteger, ForeignKey('city.id'),nullable=False)
    city = relationship(City)

class Company(Organisation):
    __tablename__ = 'company'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, ForeignKey('organisation.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'company',
    }
    person = relationship('PersonWorksAt')
    isLocatedIn = Column(BigInteger, ForeignKey('country.id'),nullable=False)
    country = relationship(Country)

class TagClass(Base):
    __tablename__ = 'tagclass'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    url = Column(String(250))
    tag  = relationship('Tag', secondary='tag_has_type')
    isSubclassOf  = relationship('TagClass', secondary='tagclass_is_subclass_of')

class Tag(Base):
    __tablename__ = 'tag'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    url = Column(String(250))
    person = relationship('Person', secondary='person_has_interest')
    hasType  = relationship('TagClass', secondary='tag_has_type')
    forumIncluded  = relationship('Forum', secondary='forum_has_tag')

class PersonSpeaksLanguage(Base):
    __tablename__ = 'person_speaks_language'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    person = relationship(Person)
    email = Column(String(100), primary_key=True)

class PersonEmailAddress(Base):
    __tablename__ = 'person_email_emailaddress'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    person = relationship(Person)
    language = Column(String(5),primary_key=True)

class PersonWorksAt(Base):
    __tablename__ = 'person_works_at'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    company_id = Column(BigInteger, ForeignKey('company.id'),primary_key=True)
    workFrom = Column(BigInteger)

class PersonStudiesAt(Base):
    __tablename__ = 'person_studies_at'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    university_id = Column(BigInteger, ForeignKey('university.id'),primary_key=True)
    classYear = Column(BigInteger)

class PersonHasInterest(Base):
    __tablename__ = 'person_has_interst'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    tag_id = Column(BigInteger, ForeignKey('tag.id'),primary_key=True)

class TagHasType(Base):
    __tablename__ = 'tag_has_type'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    tagclass_id = Column(BigInteger, ForeignKey('tagclass.id'),primary_key=True)
    tag_id = Column(BigInteger, ForeignKey('tag.id'),primary_key=True)

class TagClassIsSubclassOf(Base):
    __tablename__ = 'tagclass_is_subclass_of'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    parent_tagclass_id = Column(BigInteger, ForeignKey('tagclass.id'),primary_key=True)
    child_tagclass_id = Column(BigInteger, ForeignKey('tagclass.id'),primary_key=True)

class PersonKnows(Base):
    __tablename__ = 'person_knows'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_1_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    person_2_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    creationDate = Column(DateTime)
   
class ForumHasMember(Base):
    __tablename__ = 'forum_has_member'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    forum_id = Column(BigInteger, ForeignKey('forum.id'),primary_key=True)
    joinDate = Column(DateTime)
    
class ForumHasTag(Base):
    __tablename__ = 'forum_has_tag'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    forum_id = Column(BigInteger, ForeignKey('forum.id'),primary_key=True)
    tag_id = Column(BigInteger, ForeignKey('tag.id'),primary_key=True)

class PersonLikesMessage(Base):
    __tablename__ = 'person_likes_message'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    message_id = Column(BigInteger, ForeignKey('message.id'),primary_key=True)
    creationDate = Column(DateTime)

    
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
