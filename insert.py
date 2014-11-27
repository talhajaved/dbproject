from declarative import Base, Place, Continent, Country, City, TagClass
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import csv

engine = create_engine('sqlite:///test.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

'''
continent_dict = {}
city_dict = {}
country_dict = {}

# places loading start

print 'start read 1'
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
print 'close 1'


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

# places loading complete
'''

# tagclass loading start
print 'start read 2'
tagclass_list = []
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/tagclass.csv')
tagclass_reader = csv.DictReader(file_obj, delimiter='|')
for item in tagclass_reader:
    tagclass_list.append(TagClass(id=item['id'],name=item['name'],url=item['url']))
file_obj.close()
print 'close 2'


session.add_all(tagclass_list)
session.commit()

# places loading complete


session.close()
