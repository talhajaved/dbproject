import csv
from datetime import date
from operator import itemgetter

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.algorithms.searching import depth_first_search
d = date(1984,07,02)

# person loading start
print 'start read person'
person_list = []
file_obj_person = open('/Users/nyuad/Desktop/csv/outputDir-1k/person.csv')
person_reader = csv.DictReader(file_obj_person, delimiter='|')
for item in person_reader:
    results = item ['birthday'].split('-')
    results = [int(i) for i in results]
    birthday = date(results[0],results[1],results[2])
    if not(birthday < d):
        person_list.append(item['id']) 
file_obj_person.close()
print 'close person'
# person loading complete
person_set =  set(person_list)

# tag loading start
print 'start read tag'
tag_dict = {}
tag_dict_names = {}
file_obj_tag = open('/Users/nyuad/Desktop/csv/outputDir-1k/tag.csv')
tag_reader = csv.DictReader(file_obj_tag, delimiter='|')
for item in tag_reader:
    tag_dict[item['id']] = set()
    tag_dict_names[item['id']] = item['name']
file_obj_tag.close()
print 'close tag'
# tag loading complete

# person interests
print 'start person has interests'
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_hasInterest_tag.csv')
file_reader = csv.DictReader(file_obj, delimiter='|')
for item in file_reader:
    if item['Person.id'] in person_set:
        tag_dict[item['Tag.id']].add(item['Person.id'])
file_obj.close()
print 'close person has interests'
# person interests complete

# person know start
print 'start person knows'
person_knows_dict = {}
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_knows_person.csv')
file_reader = csv.DictReader(file_obj, ('person_1','person_2') ,delimiter='|')
file_reader.next()
for item in file_reader:
    if item['person_1'] in person_set and item['person_1'] in person_set:
        if item['person_1'] in person_knows_dict:
            person_knows_dict[item['person_1']].append(item['person_2'])
        else:
           person_knows_dict[item['person_1']] = []
file_obj.close()
print 'close person knows'
# person knows


tag_graph_list = []
for i in tag_dict:
    gr = graph()
    gr.add_nodes(tag_dict[i])
    for k in tag_dict[i]:
        if k in person_knows_dict:
            for j in person_knows_dict[k]:
                try:
                    gr.add_edge((k,j))
                except:
                    pass
    graph_range = 0
    for k in tag_dict[i]:
        temp = len(depth_first_search(gr,k)[1])
        if graph_range < temp:
            graph_range = temp
    tag_graph_list.append((graph_range,tag_dict_names[i]))



sorted_list = sorted(tag_graph_list, key=itemgetter(1))
sorted_list = sorted(tag_graph_list, key=itemgetter(0),reverse=True)
for i in sorted_list:
    print i
print 'done'
print sorted_list[0:5]

