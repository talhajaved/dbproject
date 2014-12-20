from declarative import Base, Place, Continent, Country, City, TagClass, Person
from declarative import  Forum, Organisation, University, Company, Tag, TagHasType
from declarative import PersonSpeaksLanguage, PersonEmailAddress, PersonWorksAt, PersonStudiesAt
from declarative import ForumHasMember, ForumHasTag, PersonHasInterest, TagClassIsSubclassOf
from declarative import PersonKnows, Message, Post, Comment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import csv

engine = create_engine('postgresql://postgres:database@localhost:5432/dbproject')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()




# places loading start

print 'start read place'
continent_dict = {}
city_dict = {}
country_dict = {}
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/place.csv')
places_reader = csv.DictReader(file_obj, delimiter='|')
for line in places_reader:
    if line['type'] == 'continent':
        continent_dict[line['id']] = line
    elif line['type']== 'country':
        country_dict[line['id']] = line
    elif line['type'] == 'city':
        city_dict[line['id']] = line
file_obj.close()



file_obj =open('/Users/nyuad/Desktop/csv/outputDir-1k/place_isPartOf_place.csv')
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
for key in country_dict:
    item = country_dict[key]
    country_list.append(Country(id=key,name=item['name'],url=item['url'],isPartOf = item['isPartOf']))
for key in city_dict:
    item = city_dict[key]
    city_list.append(City(id=key,name=(item['name']).decode("utf-8", "replace"),url=(item['url']).decode("utf-8", "replace"),isPartOf = item['isPartOf']))

session.add_all(continent_list)
session.add_all(country_list)
session.add_all(city_list)
#session.add(City(id='1564', name='Mekhligang', url='http://dbpedia.org/resource/Mekhligang', isPartOf ='68'))
session.commit()
print 'close place'
# places loading complete


# person loading start
print 'start read person'
person_list = []
file_obj_person = open('/Users/nyuad/Desktop/csv/outputDir-1k/person.csv')
file_obj_location = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_isLocatedIn_place.csv')
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
session.commit()
print 'close person'
# person loading complete


# forum loading start
print 'start read forum'
forum_list = []
file_obj_forum = open('/Users/nyuad/Desktop/csv/outputDir-1k/forum.csv')
file_obj_mod = open('/Users/nyuad/Desktop/csv/outputDir-1k/forum_hasModerator_person.csv')
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
session.commit()
print 'close forum'
# forum loading complete


# organization loading start
print 'start read organization'
university_list = []
company_list = []
file_obj_org = open('/Users/nyuad/Desktop/csv/outputDir-1k/organisation.csv')
file_obj_loc = open('/Users/nyuad/Desktop/csv/outputDir-1k/organisation_isLocatedIn_place.csv')
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
session.add_all(company_list)
session.commit()
print 'close organization'
# organisation loading complete


# tagclass loading start
print 'start read tagclass'
tagclass_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/tagclass.csv')
tagclass_reader = csv.DictReader(file_obj, delimiter='|')
for item in tagclass_reader:
    tagclass_list.append(TagClass(id=item['id'],name=item['name'],url=item['url']))
file_obj.close()
session.add_all(tagclass_list)
session.commit()
print 'close tagclass'
# tagclass loading complete


# tag loading start
print 'start read tag'
tag_list = []
file_obj_tag = open('/Users/nyuad/Desktop/csv/outputDir-1k/tag.csv')
tag_reader = csv.DictReader(file_obj_tag, delimiter='|')
for item in tag_reader:
    tag_list.append(Tag(id=item['id'],
                        name=item['name'].decode("utf-8", "replace"),
                        url=item['url'].decode("utf-8", "replace")))
file_obj_tag.close()
session.add_all(tag_list)
session.commit()
print 'close tag'
# tag loading complete


# person speaks language loading start
print 'start person speaks languages'
person_lang_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_speaks_language.csv')
file_reader = csv.DictReader(file_obj, delimiter='|')
for item in file_reader:
    person_lang_list.append(PersonSpeaksLanguage(person_id=item['Person.id']
                                                 ,language=item['language']))
file_obj.close()
session.add_all(person_lang_list)
session.commit()
print 'close person speaks languages'
# person speaks language loading complete


# person email start
print 'start person emails'
person_email_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_email_emailaddress.csv')
file_reader = csv.DictReader(file_obj, delimiter='|')
for item in file_reader:
    person_email_list.append(PersonEmailAddress(person_id=item['Person.id']
                                                 ,email=item['email'].decode("utf-8", "replace")))
file_obj.close()
session.add_all(person_email_list)
session.commit()
print 'close person emails'
# person emails complete


# person work start
print 'start person works'
person_work_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_workAt_organisation.csv')
file_reader = csv.DictReader(file_obj, delimiter='|')
for item in file_reader:
    person_work_list.append(PersonWorksAt(person_id=item['Person.id'],
                                           company_id=item['Organisation.id']
                                                 ,workFrom=item['workFrom']))
file_obj.close()
session.add_all(person_work_list)
session.commit()
print 'close person works'
# personworks complete


# person study start
print 'start person studies'
person_study_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_studyAt_organisation.csv')
file_reader = csv.DictReader(file_obj, delimiter='|')
for item in file_reader:
    person_study_list.append(PersonStudiesAt(person_id=item['Person.id'],
                                           university_id=item['Organisation.id']
                                                 ,classYear=item['classYear']))
file_obj.close()
session.add_all(person_study_list)
session.commit()
print 'close personstudies'
# person studies complete


# person study start
print 'start person has interests'
person_interest_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_hasInterest_tag.csv')
file_reader = csv.DictReader(file_obj, delimiter='|')
for item in file_reader:
    person_interest_list.append(PersonHasInterest(person_id=item['Person.id'],
                                           tag_id=item['Tag.id']))
file_obj.close()
session.add_all(person_interest_list)
session.commit()
print 'close person has interests'
# person interests complete


# tag_has_type loading start
print 'start read tag_has_type'
tag_has_type_list = []
file_obj_type = open('/Users/nyuad/Desktop/csv/outputDir-1k/tag_hasType_tagclass.csv')
type_reader = csv.DictReader(file_obj_type, delimiter='|')
for item in type_reader:
    tag_has_type_list.append(TagHasType(tagclass_id=item['TagClass.id'],tag_id=item['Tag.id']))
file_obj_type.close()
session.add_all(tag_has_type_list)
session.commit()
print 'close tag_has_type'
# tag_has_type loading complete


# forum has member start
print 'forum has member'
forum_member_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/forum_hasMember_person.csv')
file_reader = csv.DictReader(file_obj, delimiter='|')
for item in file_reader:
    forum_member_list.append(ForumHasMember(person_id=item['Person.id'],
                                           forum_id=item['Forum.id']
                                                 ,joinDate=item['joinDate']))
file_obj.close()
session.add_all(forum_member_list)
session.commit()
print 'close forum has member'
# forum has member complete


# forum has tag start
print 'forum has tag'
forum_tag_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/forum_hasTag_tag.csv')
file_reader = csv.DictReader(file_obj, delimiter='|')
for item in file_reader:
    forum_tag_list.append(ForumHasTag(tag_id=item['Tag.id'],
                                           forum_id=item['Forum.id']))
file_obj.close()
session.add_all(forum_tag_list)
session.commit()
print 'close forum has tag'
# forum has tag complete


 # tagclass is subclass of loading start
print 'start tagclass subclass'
tagclass_subclass_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/tagclass_isSubclassOf_tagclass.csv')
file_reader = csv.DictReader(file_obj, ('parentID','childID') ,delimiter='|')
file_reader.next()
for item in file_reader:
    tagclass_subclass_list.append(TagClassIsSubclassOf(parent_id=item['parentID'],child_id=item['childID']))
file_obj.close()
session.add_all(tagclass_subclass_list)
session.commit()
print 'close tagclass subclass'
# tagclass is subclass of loading complete


# person know start
print 'start person knows'
person_knows_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_knows_person.csv')
file_reader = csv.DictReader(file_obj, ('person_1','person_2') ,delimiter='|')
file_reader.next()
for item in file_reader:
    person_knows_list.append(PersonKnows(person_1_id=item['person_1'],
                                         person_2_id=item['person_2'],))
file_obj.close()
session.add_all(person_knows_list)
session.commit()
print 'close person knows'
# person knows


# post loading start
print 'start read post'
post_list = []
file_obj_post = open('/Users/nyuad/Desktop/csv/outputDir-1k/post.csv')
file_obj_loc = open('/Users/nyuad/Desktop/csv/outputDir-1k/post_isLocatedIn_place.csv')
file_obj_creator = open('/Users/nyuad/Desktop/csv/outputDir-1k/post_hasCreator_person.csv')
file_obj_forum = open('/Users/nyuad/Desktop/csv/outputDir-1k/forum_containerOf_post.csv')
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
session.commit()
print 'close post'
# post loading complete


# comment loading start
print 'start read comment'
comment_list = []
reply_dict = {}
last_reply_of_post = False
file_obj_comment = open('/Users/nyuad/Desktop/csv/outputDir-1k/comment.csv')
file_obj_loc = open('/Users/nyuad/Desktop/csv/outputDir-1k/comment_isLocatedIn_place.csv')
file_obj_creator = open('/Users/nyuad/Desktop/csv/outputDir-1k/comment_hasCreator_person.csv')
file_obj_post_reply = open('/Users/nyuad/Desktop/csv/outputDir-1k/comment_replyOf_post.csv')
file_obj_comment_reply = open('/Users/nyuad/Desktop/csv/outputDir-1k/comment_replyOf_comment.csv')
comment_reader = csv.DictReader(file_obj_comment, delimiter='|')
loc_reader = csv.DictReader(file_obj_loc, delimiter='|')
creator_reader = csv.DictReader(file_obj_creator, delimiter='|')
post_reply_reader = csv.DictReader(file_obj_post_reply, ('Comment.id','replyOfID') ,delimiter='|')
comment_reply_reader = csv.DictReader(file_obj_comment_reply, ('Comment.id','replyOfID') ,delimiter='|')
comment_reply_reader.next()
post_reply_reader.next()

for item in post_reply_reader:
    reply_dict[item['Comment.id']] = item['replyOfID']
file_obj_post_reply.close()

for item in comment_reply_reader:
    reply_dict[item['Comment.id']] = item['replyOfID']
file_obj_comment_reply.close()

for item in comment_reader:
    location_line = loc_reader.next()
    creator_line = creator_reader.next()
    comment_list.append(Comment(id=item['id'],
                               creationDate=item['creationDate'],locationIP=item['locationIP'],
                              browserUsed=item['browserUsed'],isLocatedIn = location_line['Place.id'],
                            hasCreator = creator_line['Person.id'],content = item['content'].decode("utf-8", "replace"),
                            replyOfId = reply_dict[str(item['id'])]))

file_obj_comment.close()
file_obj_loc.close()
file_obj_creator.close()
session.add_all(comment_list)
session.commit()
print 'close comment'
# comment loading complete

session.close()



