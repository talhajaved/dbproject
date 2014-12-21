from createTables import Base, Place, Continent, Country, City, TagClass, Person
from createTables import  Forum, Organisation, University, Company, Tag, TagHasType
from createTables import PersonSpeaksLanguage, PersonEmailAddress, PersonWorksAt, PersonStudiesAt
from createTables import ForumHasMember, ForumHasTag, PersonHasInterest, TagClassIsSubclassOf
from createTables import PersonKnows, Post, Comment, PersonLikesPost, PostHasTag
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import csv, time
import config

input_directory = config.csv_files_input_directory 

# places loading start
def insertPlace():
  print 'LOADING Place'
  continent_dict = {}
  city_dict = {}
  country_dict = {}
  file_obj = open(input_directory + '/place.csv')
  places_reader = csv.DictReader(file_obj, delimiter='|')
  for line in places_reader:
      if line['type'] == 'continent':
          continent_dict[line['id']] = line
      elif line['type']== 'country':
          country_dict[line['id']] = line
      elif line['type'] == 'city':
          city_dict[line['id']] = line
  file_obj.close()

  file_obj =open(input_directory + '/place_isPartOf_place.csv')
  places_relation_reader = csv.DictReader(file_obj, ('id','isPartOf') ,delimiter='|')
  for line in places_relation_reader:
      if line['id'] in city_dict:
          temp = city_dict[line['id']]
          temp['isPartOf'] = line['isPartOf']
          city_dict[line['id']] = temp
      elif line['id'] in country_dict:
          temp = country_dict[line['id']]
          temp['isPartOf'] = line['isPartOf']
          country_dict[line['id']] = temp
  file_obj.close()

  continent_list = []
  country_list =[]
  city_list =[]

  for key in continent_dict:
      item = continent_dict[key]
      continent_list.append(Continent(id=key,name=item['name'],url=item['url']))
  continent_dict = {}
  for key in country_dict:
      item = country_dict[key]
      country_list.append(Country(id=key,name=item['name'],url=item['url'],isPartOf = item['isPartOf']))
  country_dict = {}
  for key in city_dict:
      item = city_dict[key]
      city_list.append(City(id=key,name=(item['name']).decode("utf-8", "replace"),url=(item['url']).decode("utf-8", "replace"),isPartOf = item['isPartOf']))
  city_dict = {}

  session.add_all(continent_list)
  continent_list = []
  session.add_all(country_list)
  country_list =[]
  session.add_all(city_list)
  city_list =[]
  session.commit()
  # places loading complete  


# person loading start
def insertPerson():
  print 'LOADING Person'
  person_list = []
  file_obj_person = open(input_directory + '/person.csv')
  file_obj_location = open(input_directory + '/person_isLocatedIn_place.csv')
  person_reader = csv.DictReader(file_obj_person, delimiter='|')
  location_reader = csv.DictReader(file_obj_location, delimiter='|')
  for item in person_reader:
      location_line = location_reader.next()
      person_list.append(Person(id=item['id'],
                                firstName=item['firstName'].decode("utf-8", "replace"),
                                lastName=item['lastName'].decode("utf-8", "replace"),
                                gender=item['gender'],birthday = item['birthday'],
                                creationDate=item['creationDate'],locationIP=item['locationIP'],
                                browserUsed=item['browserUsed'],isLocatedIn = location_line['Place.id']))
  file_obj_person.close()
  file_obj_location.close()
  session.add_all(person_list)
  person_list = []
  session.commit()
  # person loading complete


# forum loading start
def insertForum():
  print 'LOADING Forum'
  forum_list = []
  file_obj_forum = open(input_directory + '/forum.csv')
  file_obj_mod = open(input_directory + '/forum_hasModerator_person.csv')
  forum_reader = csv.DictReader(file_obj_forum, delimiter='|')
  mod_reader = csv.DictReader(file_obj_mod, delimiter='|')
  for item in forum_reader:
      mod_line = mod_reader.next()
      forum_list.append(Forum(id=item['id'],
                              title=item['title'].decode("utf-8", "replace"),
                                 creationDate=item['creationDate'],
                                 hasModerator=mod_line['Person.id'],))
  file_obj_forum.close()
  file_obj_mod.close()
  session.add_all(forum_list)
  forum_list = []
  session.commit()
  # forum loading complete


# organization loading start
def insertOrganization():
  print 'LOADING Organization'
  university_list = []
  company_list = []
  file_obj_org = open(input_directory + '/organisation.csv')
  file_obj_loc = open(input_directory + '/organisation_isLocatedIn_place.csv')
  org_reader = csv.DictReader(file_obj_org, delimiter='|')
  loc_reader = csv.DictReader(file_obj_loc, delimiter='|')
  for item in org_reader:
      location_line = loc_reader.next()
      if item['type'] == 'university':
          university_list.append(University(id=item['id'],
                              name=item['name'].decode("utf-8", "replace"),
                              url=item['url'].decode("utf-8", "replace")
                                            ,isLocatedIn = location_line['Place.id']))
      elif item['type'] =='company':
          company_list.append(Company(id=item['id'],
                              name=item['name'].decode("utf-8", "replace"),
                              url=item['url'].decode("utf-8", "replace")
                                         ,isLocatedIn = location_line['Place.id']))
  file_obj_org.close()
  file_obj_loc.close()
  session.add_all(university_list)
  university_list = []
  session.add_all(company_list)
  company_list = []
  session.commit()
  # organisation loading complete

# tagclass loading start
def insertTagClass():
  print 'LOADING Tagclass'
  tagclass_list = []
  file_obj = open(input_directory + '/tagclass.csv')
  tagclass_reader = csv.DictReader(file_obj, delimiter='|')
  for item in tagclass_reader:
      tagclass_list.append(TagClass(id=item['id'],name=item['name'],url=item['url']))
  file_obj.close()
  session.add_all(tagclass_list)
  tagclass_list = []
  session.commit()
  # tagclass loading complete


# tag loading start
def insertTag():
  print 'LOADING Tag'
  tag_list = []
  file_obj_tag = open(input_directory + '/tag.csv')
  tag_reader = csv.DictReader(file_obj_tag, delimiter='|')
  for item in tag_reader:
      tag_list.append(Tag(id=item['id'],
                          name=item['name'].decode("utf-8", "replace"),
                          url=item['url'].decode("utf-8", "replace")))
  file_obj_tag.close()
  session.add_all(tag_list)
  tag_list = []
  session.commit()
  # tag loading complete


# person speaks language loading start
def insertPersonSpeaksLanguage():
  print 'LOADING Person Speaks Languages'
  person_lang_list = []
  file_obj = open(input_directory + '/person_speaks_language.csv')
  file_reader = csv.DictReader(file_obj, delimiter='|')
  for item in file_reader:
      person_lang_list.append(PersonSpeaksLanguage(person_id=item['Person.id']
                                                   ,language=item['language']))
  file_obj.close()
  session.add_all(person_lang_list)
  person_lang_list = []
  session.commit()
  # person speaks language loading complete


# person email start
def insertPersonEmailAddress():
  print 'LOADING Person Emails'
  person_email_list = []
  file_obj = open(input_directory + '/person_email_emailaddress.csv')
  file_reader = csv.DictReader(file_obj, delimiter='|')
  for item in file_reader:
      person_email_list.append(PersonEmailAddress(person_id=item['Person.id']
                                                   ,email=item['email'].decode("utf-8", "replace")))
  file_obj.close()
  session.add_all(person_email_list)
  person_email_list = []
  session.commit()
  # person emails complete


# person work start
def insertPersonWorksAt():
  print 'LOADING Person Works'
  person_work_list = []
  file_obj = open(input_directory + '/person_workAt_organisation.csv')
  file_reader = csv.DictReader(file_obj, delimiter='|')
  for item in file_reader:
      person_work_list.append(PersonWorksAt(person_id=item['Person.id'],
                                             company_id=item['Organisation.id']
                                                   ,workFrom=item['workFrom']))
  file_obj.close()
  session.add_all(person_work_list)
  person_work_list = []
  session.commit()
  # personworks complete


# person study start
def insertPersonStudiesAt():
  print 'LOADING Person Studies'
  person_study_list = []
  file_obj = open(input_directory + '/person_studyAt_organisation.csv')
  file_reader = csv.DictReader(file_obj, delimiter='|')
  for item in file_reader:
      person_study_list.append(PersonStudiesAt(person_id=item['Person.id'],
                                             university_id=item['Organisation.id']
                                                   ,classYear=item['classYear']))
  file_obj.close()
  session.add_all(person_study_list)
  person_study_list = []
  session.commit()
  # person studies complete


# person study start
def insertPersonHasInterests():
  print 'LOADING Person Interests'
  person_interest_list = []
  file_obj = open(input_directory + '/person_hasInterest_tag.csv')
  file_reader = csv.DictReader(file_obj, delimiter='|')
  for item in file_reader:
      person_interest_list.append(PersonHasInterest(person_id=item['Person.id'],
                                             tag_id=item['Tag.id']))
  file_obj.close()
  session.add_all(person_interest_list)
  person_interest_list = []
  session.commit()
  # person interests complete


# tag_has_type loading start
def insertTagHasType():
  print 'LOADING TagHasType'
  tag_has_type_list = []
  file_obj_type = open(input_directory + '/tag_hasType_tagclass.csv')
  type_reader = csv.DictReader(file_obj_type, delimiter='|')
  for item in type_reader:
      tag_has_type_list.append(TagHasType(tagclass_id=item['TagClass.id'],tag_id=item['Tag.id']))
  file_obj_type.close()
  session.add_all(tag_has_type_list)
  tag_has_type_list = []
  session.commit()
  # tag_has_type loading complete


# forum has member start
def insertForumHasMember():
  print 'LOADING Forum Members'
  forum_member_list = []
  file_obj = open(input_directory + '/forum_hasMember_person.csv')
  file_reader = csv.DictReader(file_obj, delimiter='|')
  for item in file_reader:
      forum_member_list.append(ForumHasMember(person_id=item['Person.id'],
                                             forum_id=item['Forum.id']
                                                   ,joinDate=item['joinDate']))
  file_obj.close()
  session.add_all(forum_member_list)
  forum_member_list = []
  session.commit()
  # forum has member complete


# forum has tag start
def insertForumHasTag():
  print 'LOADING Forum Tags'
  forum_tag_list = []
  file_obj = open(input_directory + '/forum_hasTag_tag.csv')
  file_reader = csv.DictReader(file_obj, delimiter='|')
  for item in file_reader:
      forum_tag_list.append(ForumHasTag(tag_id=item['Tag.id'],
                                             forum_id=item['Forum.id']))
  file_obj.close()
  session.add_all(forum_tag_list)
  forum_tag_list = []
  session.commit()
  # forum has tag complete


 # tagclass is subclass of loading start


# tag is subclass start
def insertTagClassIsSubclassOf():
  print 'LOADING Tagclass Subclass'
  tagclass_subclass_list = []
  file_obj = open(input_directory + '/tagclass_isSubclassOf_tagclass.csv')
  file_reader = csv.DictReader(file_obj, ('parentID','childID') ,delimiter='|')
  file_reader.next()
  for item in file_reader:
      tagclass_subclass_list.append(TagClassIsSubclassOf(parent_id=item['parentID'],child_id=item['childID']))
  file_obj.close()
  session.add_all(tagclass_subclass_list)
  tagclass_subclass_list = []
  session.commit()
  # tagclass is subclass of loading complete


# person know start
def insertPersonKnows():
  print 'LOADING Person Knows'
  person_knows_list = []
  file_obj = open(input_directory + '/person_knows_person.csv')
  file_reader = csv.DictReader(file_obj, ('person_1','person_2') ,delimiter='|')
  file_reader.next()
  for item in file_reader:
      person_knows_list.append(PersonKnows(person_1_id=item['person_1'],
                                           person_2_id=item['person_2'],))
  file_obj.close()
  session.add_all(person_knows_list)
  person_knows_list = []
  session.commit()
  # person knows


# post loading start
def insertPost():
  print 'LOADING Post'
  post_list = []
  file_obj_post = open(input_directory + '/post.csv')
  file_obj_loc = open(input_directory + '/post_isLocatedIn_place.csv')
  file_obj_creator = open(input_directory + '/post_hasCreator_person.csv')
  file_obj_forum = open(input_directory + '/forum_containerOf_post.csv')
  org_reader = csv.DictReader(file_obj_post, delimiter='|')
  loc_reader = csv.DictReader(file_obj_loc, delimiter='|')
  creator_reader = csv.DictReader(file_obj_creator, delimiter='|')
  forum_reader = csv.DictReader(file_obj_forum, delimiter='|')
  for item in org_reader:
      location_line = loc_reader.next()
      creator_line = creator_reader.next()
      forum_line = forum_reader.next()
      post_list.append(Post(id=item['id'],
                                 creationDate=item['creationDate'],locationIP=item['locationIP'],
                                browserUsed=item['browserUsed'],isLocatedIn = location_line['Place.id'],
                              hasCreator = creator_line['Person.id'],content = item['content'].decode("utf-8", "replace"),
                              language = item['language'], forumId = forum_line['Forum.id']))
  file_obj_post.close()
  file_obj_loc.close()
  file_obj_creator.close()
  file_obj_forum.close()
  session.add_all(post_list)
  post_list = []
  session.commit()
  # post loading complete


# forum has tag start
def insertPostHasTag():
  print 'LOADING PostHasTag'
  post_tag_list = []
  file_obj = open(input_directory + '/post_hasTag_tag.csv')
  file_reader = csv.DictReader(file_obj, delimiter='|')
  for item in file_reader:
      post_tag_list.append(PostHasTag(tag_id=item['Tag.id'],
                                             post_id=item['Post.id']))
  file_obj.close()
  session.add_all(post_tag_list)
  post_tag_list = []
  session.commit()
  # forum has tag complete


# comment loading start
def insertComment():
  print 'LOADING Comment'
  comment_list = []
  reply_dict = {}
  last_reply_of_post = False
  file_obj_comment = open(input_directory + '/comment.csv')
  file_obj_loc = open(input_directory + '/comment_isLocatedIn_place.csv')
  file_obj_creator = open(input_directory + '/comment_hasCreator_person.csv')
  file_obj_post_reply = open(input_directory + '/comment_replyOf_post.csv')
  file_obj_comment_reply = open(input_directory + '/comment_replyOf_comment.csv')
  comment_reader = csv.DictReader(file_obj_comment, delimiter='|')
  loc_reader = csv.DictReader(file_obj_loc, delimiter='|')
  creator_reader = csv.DictReader(file_obj_creator, delimiter='|')
  post_reply_reader = csv.DictReader(file_obj_post_reply, ('Comment.id','replyOfID') ,delimiter='|')
  comment_reply_reader = csv.DictReader(file_obj_comment_reply, ('Comment.id','replyOfID') ,delimiter='|')
  comment_reply_reader.next()
  post_reply_reader.next()

  for item in post_reply_reader:
      reply_dict[item['Comment.id']] = ('post',item['replyOfID'])
  file_obj_post_reply.close()

  for item in comment_reply_reader:
      reply_dict[item['Comment.id']] = ('comment',item['replyOfID'])
  file_obj_comment_reply.close()

  for item in comment_reader:
      location_line = loc_reader.next()
      creator_line = creator_reader.next()
      if reply_dict[item['id']][0] == 'post':
          comment_list.append(Comment(id=item['id'],
                                 creationDate=item['creationDate'],locationIP=item['locationIP'],
                                browserUsed=item['browserUsed'],isLocatedIn = location_line['Place.id'],
                              hasCreator = creator_line['Person.id'],content = item['content'].decode("utf-8", "replace"),
                              replyOfPostId = reply_dict[item['id']][1],replyOf = 'post'))
      else:
          comment_list.append(Comment(id=item['id'],
                                 creationDate=item['creationDate'],locationIP=item['locationIP'],
                                browserUsed=item['browserUsed'],isLocatedIn = location_line['Place.id'],
                              hasCreator = creator_line['Person.id'],content = item['content'].decode("utf-8", "replace"),
                              replyOfCommentId = reply_dict[item['id']][1],replyOf = 'comment'))
  file_obj_comment.close()
  file_obj_loc.close()
  file_obj_creator.close()
  session.add_all(comment_list)
  comment_list = []
  reply_dict = {}
  session.commit()
  # comment loading complete


# person likes posts start
def insertPersonLikesPost():
  print 'LOADING PersonLikesPosts\n'
  person_post_list = []
  file_obj = open(input_directory + '/person_likes_post.csv')
  file_reader = csv.DictReader(file_obj, delimiter='|')
  for item in file_reader:
      person_post_list.append(PersonLikesPost(person_id=item['Person.id'],
                                             post_id=item['Post.id'],creationDate=item['creationDate']))
  file_obj.close()
  session.add_all(person_post_list)
  person_post_list = []
  session.commit()
  # person likes post complete

def main():
  engine_path = config.db['default-db']+"://"+ config.db['user']+":"+config.db['password']\
              +"@"+config.db['host']+":"+config.db['port']+"/"+config.db['db']
  engine = create_engine(engine_path)
  Base.metadata.bind = engine
  DBSession = sessionmaker(bind=engine)
  global session
  session = DBSession()

  start = time.time()
  insertPlace()
  end = time.time()
  placeLoadTime = end - start
  
  start = time.time()
  insertPerson()
  end = time.time()
  personLoadTime = end - start

  start = time.time()
  insertForum()
  end = time.time()
  forumLoadTime = end - start
  
  start = time.time()
  insertTagClass()
  end = time.time()
  tagClassLoadTime = end - start

  start = time.time()
  insertOrganization()
  end = time.time()
  organizationLoadTime = end - start

  start = time.time()
  insertTag()
  end = time.time()
  tagLoadTime = end - start

  start = time.time()
  insertPersonWorksAt()
  end = time.time()
  workAtLoadTime = end - start

  start = time.time()
  insertPersonStudiesAt()
  end = time.time()
  studyAtLoadTime = end - start

  start = time.time()
  insertPersonHasInterests()
  end = time.time()
  hasInterestLoadTime = end - start  
  
  start = time.time()
  insertPersonEmailAddress()
  end = time.time()
  emailLoadTime = end - start

  start = time.time()
  insertPersonSpeaksLanguage()
  end = time.time()
  languageLoadTime = end - start

  start = time.time()
  insertPersonKnows()
  end = time.time()
  knowsLoadTime = end - start

  start = time.time()
  insertTagHasType()
  end = time.time()
  hasTypeLoadTime = end - start

  start = time.time()
  insertForumHasMember() 
  end = time.time()
  hasMemberLoadTime = end - start
  
  start = time.time()
  insertForumHasTag()
  end = time.time()
  forumHasTagLoadTime = end - start

  start = time.time()
  insertTagClassIsSubclassOf()
  end = time.time()
  tagSubclassLoadTime = end - start  
  
  start = time.time()
  insertPost()
  end = time.time()
  postLoadTime = end - start

  start = time.time()
  insertPostHasTag()
  end = time.time()
  postHasTagLoadTime = end - start

  start = time.time()
  insertComment()
  end = time.time()
  commentLoadTime = end - start

  start = time.time()
  insertPersonLikesPost()
  end = time.time()
  likesLoadTime = end - start

  session.close()

  print "TABLE                   |COPY TIME (seconds)         "
  print "Place                   |"+ str(placeLoadTime)
  print "Person                  |"+ str(personLoadTime)
  print "Forum                   |"+ str(forumLoadTime)
  print "Commen                  |"+ str(commentLoadTime)
  print "Tag                     |"+ str(tagLoadTime)
  print "TagClass                |"+ str(tagClassLoadTime)
  print "Organization            |"+ str(organizationLoadTime)
  print "Post                    |"+ str(postLoadTime)
  print "Speaks                  |"+ str(languageLoadTime)
  print "Email                   |"+ str(emailLoadTime)
  print "Knows                   |"+ str(knowsLoadTime)
  print "Likes                   |"+ str(likesLoadTime)
  print "HasInterest             |"+ str(hasInterestLoadTime)
  print "WorkAt                  |"+ str(workAtLoadTime)
  print "StudyAt                 |"+ str(studyAtLoadTime)
  print "ForumHasTagLoadTime     |"+ str(forumHasTagLoadTime)
  print "ForumHasMember          |"+ str(hasMemberLoadTime)
  print "PostHasTag              |"+ str(postHasTagLoadTime)
  print "TagHasType              |"+ str(hasTypeLoadTime)
  print "TagClassSubclass        |"+ str(hasTypeLoadTime)

if __name__ == "__main__":
  main()
