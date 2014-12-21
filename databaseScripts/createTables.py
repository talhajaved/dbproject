import psycopg2 as pg
import config
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, BigInteger, Date
import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



def deleteDB():
  conn = pg.connect(database=config.db['default-db'], user=config.db['user'], password=config.db['password'],\
    host =config.db['host'])
  conn.set_isolation_level(0);
  cur = conn.cursor()
  cur.execute("DROP DATABASE IF EXISTS "+config.db['db']+";")
  conn.commit()
  conn.set_isolation_level(1);
  cur.close()
  conn.close()

def createDB():
  conn = pg.connect(database=config.db['default-db'], user=config.db['user'],\
    password=config.db['password'], host =config.db['host'])
  conn.set_isolation_level(0);
  cur = conn.cursor()
  cur.execute("CREATE DATABASE "+config.db['db']+";")
  conn.set_isolation_level(1);
  cur.close()
  conn.close()

deleteDB()
createDB()

Base = declarative_base()
    
class Place(Base):
    __tablename__ = 'place'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    url = Column(String(250))
    type = Column(String(10))
    __mapper_args__ = {
        'polymorphic_identity':'place',
        'polymorphic_on':type
    }
    
class Continent(Place):
    __tablename__ = 'continent'
    id = Column(BigInteger, ForeignKey('place.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'continent',
        'inherit_condition':(id == Place.id)
    }

class Country(Place):
    __tablename__ = 'country'
    id = Column(BigInteger, ForeignKey('place.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'country',
        'inherit_condition':(id == Place.id)
    }
    isPartOf = Column(BigInteger, ForeignKey('continent.id'),nullable=False)
    continent = relationship(Continent,foreign_keys='Country.isPartOf')

class City(Place):
    __tablename__ = 'city'
    id = Column(BigInteger, ForeignKey('place.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'city',
        'inherit_condition':(id == Place.id)
    }
    isPartOf = Column(BigInteger, ForeignKey('country.id'),nullable=False)
    country = relationship(Country,foreign_keys='City.isPartOf')

class Person(Base):
    __tablename__ = 'person'
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
    likes = relationship('PersonLikesPost')
    hasInterest  = relationship('Tag', secondary='person_has_interest')
    isMemberOf  = relationship('Forum', secondary='forum_has_member')
    isLocatedIn = Column(BigInteger, ForeignKey('city.id'),nullable=False)
    city  = relationship(City)

class Forum(Base):
    __tablename__ = 'forum'
    id = Column(BigInteger, primary_key=True)
    title = Column(String(100))
    creationDate = Column(DateTime)
    hasModerator = Column(BigInteger, ForeignKey('person.id'),nullable= False)
    person = relationship(Person)
    hasTag  = relationship('Tag', secondary='forum_has_tag')
    hasMember  = relationship('Person', secondary='forum_has_member')
    
class Post(Base):
    __tablename__ = 'post'
    id = Column(BigInteger, primary_key=True)
    locationIP = Column(String(20))
    browserUsed = Column(String(20))
    creationDate = Column(DateTime)
    length = Column(Integer)
    content = Column(String(1000))
    likedBy = relationship('PersonLikesPost')
    hasCreator = Column(BigInteger, ForeignKey('person.id'),nullable= False)
    person = relationship(Person)
    isLocatedIn = Column(BigInteger, ForeignKey('country.id'),nullable=False)
    country = relationship(Country)
    language = Column(String(5))
    imageFile = Column(String(250))
    forumId = Column(BigInteger, ForeignKey('forum.id'),nullable= False)
    forum  = relationship(Forum)
    hasTag  = relationship('Tag', secondary='post_has_tag')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(BigInteger, primary_key=True)
    locationIP = Column(String(20))
    browserUsed = Column(String(20))
    creationDate = Column(DateTime)
    length = Column(Integer)
    content = Column(String(1000))
    hasCreator = Column(BigInteger, ForeignKey('person.id'),nullable= False)
    person = relationship(Person)
    isLocatedIn = Column(BigInteger, ForeignKey('country.id'),nullable=False)
    country = relationship(Country)
    replyOf = Column(String(10))
    replyOfPostId = Column(BigInteger, ForeignKey('post.id'),nullable= True)
    post = relationship(Post)
    replyOfCommentId = Column(Integer, ForeignKey('comment.id'),nullable= True)
     
class Organisation(Base):
    __tablename__ = 'organisation'
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
    id = Column(BigInteger, ForeignKey('organisation.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'university',
    }
    person = relationship('PersonStudiesAt')
    isLocatedIn = Column(BigInteger, ForeignKey('city.id'),nullable=False)
    city = relationship(City)

class Company(Organisation):
    __tablename__ = 'company'
    id = Column(BigInteger, ForeignKey('organisation.id'),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'company',
    }
    person = relationship('PersonWorksAt')
    isLocatedIn = Column(BigInteger, ForeignKey('country.id'),nullable=False)
    country = relationship(Country)

class TagClass(Base):
    __tablename__ = 'tagclass'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    url = Column(String(250))
    tag  = relationship('Tag', secondary='tag_has_type')
    isParentOf  = relationship('TagClass', secondary='tagclass_is_subclass_of',foreign_keys='TagClassIsSubclassOf.parent_id')
    isSubclassOf  = relationship('TagClass', secondary='tagclass_is_subclass_of',foreign_keys='TagClassIsSubclassOf.child_id')

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    url = Column(String(250))
    person = relationship('Person', secondary='person_has_interest')
    hasType  = relationship('TagClass', secondary='tag_has_type')
    forumIncluded  = relationship('Forum', secondary='forum_has_tag')
    postIncluded  = relationship('Post', secondary='post_has_tag')

class PersonSpeaksLanguage(Base):
    __tablename__ = 'person_speaks_language'
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    person = relationship(Person)
    language = Column(String(5), primary_key=True)

class PersonEmailAddress(Base):
    __tablename__ = 'person_email_emailaddress'   
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    person = relationship(Person)
    email = Column(String(100),primary_key=True)

class PersonWorksAt(Base):
    __tablename__ = 'person_works_at'
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    company_id = Column(BigInteger, ForeignKey('company.id'),primary_key=True)
    workFrom = Column(BigInteger)

class PersonStudiesAt(Base):
    __tablename__ = 'person_studies_at'
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    university_id = Column(BigInteger, ForeignKey('university.id'),primary_key=True)
    classYear = Column(BigInteger)

class PersonHasInterest(Base):
    __tablename__ = 'person_has_interest'
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    tag_id = Column(BigInteger, ForeignKey('tag.id'),primary_key=True)

class TagHasType(Base):
    __tablename__ = 'tag_has_type'
    tagclass_id = Column(BigInteger, ForeignKey('tagclass.id'),primary_key=True)
    tag_id = Column(BigInteger, ForeignKey('tag.id'),primary_key=True)

class TagClassIsSubclassOf(Base):
    __tablename__ = 'tagclass_is_subclass_of'
    parent_id = Column(BigInteger, ForeignKey('tagclass.id'),primary_key=True)
    child_id = Column(BigInteger, ForeignKey('tagclass.id'),primary_key=True)

class PersonKnows(Base):
    __tablename__ = 'person_knows'
    person_1_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    person_2_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    creationDate = Column(DateTime)
   
class ForumHasMember(Base):
    __tablename__ = 'forum_has_member'
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    forum_id = Column(BigInteger, ForeignKey('forum.id'),primary_key=True)
    joinDate = Column(DateTime)
    
class ForumHasTag(Base):
    __tablename__ = 'forum_has_tag'
    forum_id = Column(BigInteger, ForeignKey('forum.id'),primary_key=True)
    tag_id = Column(BigInteger, ForeignKey('tag.id'),primary_key=True)

class PostHasTag(Base):
    __tablename__ = 'post_has_tag'
    post_id = Column(BigInteger, ForeignKey('post.id'),primary_key=True)
    tag_id = Column(BigInteger, ForeignKey('tag.id'),primary_key=True)

class PersonLikesPost(Base):
    __tablename__ = 'person_likes_post'
    person_id = Column(BigInteger, ForeignKey('person.id'),primary_key=True)
    post_id = Column(BigInteger, ForeignKey('post.id'),primary_key=True)
    creationDate = Column(DateTime)

    
def main():
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    #engine = create_engine('sqlite:///test.db')
    engine_path = config.db['default-db']+"://"+ config.db['user']+":"+config.db['password']\
                  +"@"+config.db['host']+":"+config.db['port']+"/"+config.db['db']
    engine = create_engine(engine_path)
     
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)


if __name__ == "__main__":
  main()

