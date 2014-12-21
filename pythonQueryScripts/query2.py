import config
import csv
from datetime import date

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.algorithms.searching import depth_first_search

input_directory = config.csv_files_input_directory 
		
def query2(k,d):
	number_of_tags = k
	results = d.split('-')
	results = [int(i) for i in results]
	d = date(results[0],results[1],results[2])
	person_set = set()
	file_obj_person = open(input_directory + '/person.csv')
	person_reader = csv.DictReader(file_obj_person, delimiter='|')
	for item in person_reader:
	    results = item ['birthday'].split('-')
	    results = [int(i) for i in results]
	    birthday = date(results[0],results[1],results[2])
	    if not(birthday < d):
	        person_set.add(item['id']) 
	file_obj_person.close()

	# tag loading start
	tag_dict = {}
	tag_dict_names = {}
	file_obj_tag = open(input_directory + '/tag.csv')
	tag_reader = csv.DictReader(file_obj_tag, delimiter='|')
	for item in tag_reader:
	    tag_dict[item['id']] = set()
	    tag_dict_names[item['id']] = item['name']
	file_obj_tag.close()
	# tag loading complete

	# person interests
	file_obj = open(input_directory + '/person_hasInterest_tag.csv')
	file_reader = csv.DictReader(file_obj, delimiter='|')
	for item in file_reader:
	    if item['Person.id'] in person_set:
	        tag_dict[item['Tag.id']].add(item['Person.id'])
	file_obj.close()
	# person interests

	# person knows
	person_knows_dict = {}
	file_obj = open(input_directory + '/person_knows_person.csv')
	file_reader = csv.DictReader(file_obj, ('person_1','person_2') ,delimiter='|')
	file_reader.next()
	for item in file_reader:
	    if item['person_1'] in person_set and item['person_1'] in person_set:
	        if item['person_1'] in person_knows_dict:
	            person_knows_dict[item['person_1']].append(item['person_2'])
	        else:
	           person_knows_dict[item['person_1']] = []
	file_obj.close()
	# person knows

	# construct graph
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
	    tag_graph_list.append((tag_dict_names[i],graph_range))


	sorted_list = sorted(tag_graph_list, key=lambda x:(-x[1],x[0]))
	result_string = ''
	for i in sorted_list[0:number_of_tags]:
	    if len(result_string) == 0:
	        result_string = i[0]
	    else:
	        result_string = result_string + ' ' + i[0]
	return result_string

