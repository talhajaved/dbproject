def query2SQL(k,d,cur):

	filterBirthday = "\
	CREATE OR REPLACE VIEW valid_tag_pairs (fromnode, tonode, tag) AS (\
	  SELECT pk.person_1_id, pk.person_2_id, tr.tagname\
	  FROM person_knows as pk, knowntagpairs as tr WHERE\
	  pk.person_1_id = tr.id1 AND pk.person_2_id = tr.id2\
	  AND tr.birthday >= '" + str(d) + "'\
	  )\
	;"

	allTags = "\
		SELECT DISTINCT tag\
		FROM valid_tag_pairs;\
	"

	tagRange = lambda thisTag: "\
	CREATE OR REPLACE VIEW edge (fromnode, tonode) AS (\
	    SELECT fromnode, tonode\
	    FROM valid_tag_pairs Where tag = '"+ thisTag+"'\
	    UNION\
	    SELECT tonode, fromnode\
	    FROM valid_tag_pairs Where tag = '"+ thisTag+"'\
	  );\
	WITH RECURSIVE search_graph(id, tonode, depth, path, cycle) AS (\
	        SELECT g.fromnode, g.tonode, 1,\
	          ARRAY[g.fromnode],\
	          false\
	        FROM edge g\
	      UNION ALL\
	        SELECT g.fromnode, g.tonode, sg.depth + 1,\
	          path || g.fromnode,\
	          g.fromnode = ANY(path)\
	        FROM edge g, search_graph sg\
	        WHERE g.fromnode = sg.tonode AND NOT cycle)\
	SELECT MAX(temp2.reach) FROM (Select count(*) as reach FROM (\
		SELECT distinct id, path[1] FROM search_graph where cycle = 'f'\
		order by id) as temp\
		Group by temp.id) as temp2;\
	"	

	validTags = []
	cur.execute(filterBirthday)
	cur.execute(allTags)
	for line in cur:
		validTags.append(line[0])

	# print groupNodeQuery(nameTags[0])
	results = []
	for eachTag in validTags:
		cur.execute(tagRange(eachTag))
		for each in cur:
			results.append((eachTag, each[0]))
	results.sort(key=lambda item: (-item[1], item[0]))

	result_string = ''
	for i in results[0:int(k)]:
	    if len(result_string):
	        result_string = result_string + ' ' + i[0]
	    else:
	        result_string = i[0]
	return result_string


