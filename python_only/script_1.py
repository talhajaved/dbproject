import csv

from itertools import groupby

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.algorithms.minmax import shortest_path


comment_limit = 1

comment_reply_of_dict = {}
file_obj_comment_reply = open('/Users/nyuad/Desktop/csv/outputDir-1k/comment_replyOf_comment.csv')
comment_reply_reader = csv.DictReader(file_obj_comment_reply, ('Comment.id','replyOfID') ,delimiter='|')
comment_reply_reader.next()
for item in comment_reply_reader:
    comment_reply_of_dict[item['Comment.id']] = item['replyOfID']
file_obj_comment_reply.close()


creator_dict = {}
comment_creator_dict = {}
file_obj_creator = open('/Users/nyuad/Desktop/csv/outputDir-1k/comment_hasCreator_person.csv')
creator_reader = csv.DictReader(file_obj_creator, delimiter='|')
for item in creator_reader:
    comment_creator_dict[item['Comment.id']] = item['Person.id']
    if item['Person.id'] in creator_dict:
        temp = item['Comment.id']
        if temp in comment_reply_of_dict:
            temp_reply = comment_reply_of_dict[temp]
            creator_dict[item['Person.id']].append(comment_creator_dict[temp_reply])
    else:
        creator_dict[item['Person.id']] =[]
        
for i in creator_dict:
    a = creator_dict[i]
    a = min([len(list(group)) for key, group in groupby(a)])
    print a


'''
# person know start
print 'start person knows'
person_knows_dict = {}
file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_knows_person.csv')
file_reader = csv.DictReader(file_obj, ('person_1','person_2') ,delimiter='|')
file_reader.next()
for item in file_reader:
    if item['person_1'] in person_knows_dict:
        pass
    else:
        person_knows_dict[] = 
    person_knows_list.append(PersonKnows(person_1_id=item['person_1'],
                                         person_2_id=item['person_2'],))
file_obj.close()
session.add_all(person_knows_list)
session.commit()
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
        results = shortest_path(gr,k)[1].values()
        results = [int(l) for l in results]
        temp = max(results)
        if graph_range < temp:
            graph_range = temp
    tag_graph_list.append((graph_range,tag_dict_names[i]))

sorted_list = sorted(tag_graph_list, key=itemgetter(1),)
sorted_list = sorted(tag_graph_list, key=itemgetter(0),reverse=True)
print 'done'
print sorted_list[0]
print sorted_list[1]
print sorted_list[2]
'''
