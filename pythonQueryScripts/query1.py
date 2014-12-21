import config
import csv

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.algorithms.minmax import shortest_path

input_directory = config.csv_files_input_directory 

def query1(p1,p2,x):
	min_comment_limit = x
	valid_creators = set()

	if min_comment_limit == -1:	
		file_obj = open(input_directory + '/person.csv')
		file_reader = csv.DictReader(file_obj,delimiter='|')
		for item in file_reader:
		    valid_creators.add(item['id'])
		file_obj.close()

		person_knows_dict = {}
		file_obj = open('/Users/nyuad/Desktop/csv/outputDir-1k/person_knows_person.csv')
		file_reader = csv.DictReader(file_obj, ('person_1','person_2') ,delimiter='|')
		file_reader.next()
		for item in file_reader:
		    if item['person_1'] in person_knows_dict:
		        person_knows_dict[item['person_1']].append(item['person_2'])
		    else:
		        person_knows_dict[item['person_1']] = []
		file_obj.close()

		valid_creators_list = list(valid_creators)
		gr = graph()
		gr.add_nodes(valid_creators_list)
		for k in valid_creators_list:
		    if k in person_knows_dict:
		        for j in person_knows_dict[k]:
		            try:
		                gr.add_edge((k,j))
		            except:
		                pass
		b = shortest_path(gr, str(p1))[1]
		try:
		    return b[str(p2)]
		except:
		    return -1
	else:
		comment_reply_of_dict = {}
		file_obj_comment_reply = open(input_directory + '/comment_replyOf_comment.csv')
		comment_reply_reader = csv.DictReader(file_obj_comment_reply, ('Comment.id','replyOfID') ,delimiter='|')
		comment_reply_reader.next()
		for item in comment_reply_reader:
		    comment_reply_of_dict[item['Comment.id']] = item['replyOfID']
		file_obj_comment_reply.close()

		valid_person_dict = {}
		creator_comment_dict = {}
		file_obj_creator = open(input_directory + '/comment_hasCreator_person.csv')
		creator_reader = csv.DictReader(file_obj_creator, delimiter='|')
		for item in creator_reader:
		    creator_comment_dict[item['Comment.id']] = item['Person.id']
		    if item['Person.id'] in valid_person_dict:
		        temp = item['Comment.id']
		        if temp in comment_reply_of_dict:
		            temp_reply = comment_reply_of_dict[temp]
		            valid_person_dict[item['Person.id']].append(creator_comment_dict[temp_reply])
		    else:
		        valid_person_dict[item['Person.id']] =[]
		            
		for i in valid_person_dict:
		    person_valid = True
		    a = valid_person_dict[i]
		    d = {x:a.count(x) for x in a}
		    dict_del = []
		    for j in d:
		        if int(d[j]) < min_comment_limit+1:
		            dict_del.append(j)
		    for j in dict_del:
		        del d[j]
		    if person_valid == True:
		        valid_person_dict[i] = d.keys()

		# person know start
		person_knows_dict = {}
		file_obj = open(input_directory + '/person_knows_person.csv')
		file_reader = csv.DictReader(file_obj, ('person_1','person_2') ,delimiter='|')
		file_reader.next()
		for item in file_reader:
		    if item['person_1'] in person_knows_dict:
		        person_knows_dict[item['person_1']].append(item['person_2'])
		    else:		            
		        person_knows_dict[item['person_1']] = []		           
		file_obj.close()
		# person knows
		
		valid_creators_list = valid_person_dict.keys()
		gr = graph()
		gr.add_nodes(valid_creators_list)
		for k in valid_creators_list:
		    if k in person_knows_dict:
		        for j in person_knows_dict[k]:
		            try:
		                temp1 = valid_person_dict[k]
		                temp2 = valid_person_dict[j]
		                if j in temp1 and k in temp2:
		                    gr.add_edge((k,j))
		            except:
		                pass
		b = shortest_path(gr, str(p1))[1]
		c = shortest_path(gr, str(p1))[0]
		try:
		    return b[str(p2)]
		except:
		    return -1
