def query1SQL(p1,p2,X, cur):
	withReplyRel = "\
	CREATE OR REPLACE VIEW edge (fromnode, tonode, weight) AS (\
	  SELECT pk.person_1_id, pk.person_2_id, 1\
	  FROM person_knows as pk, personrepliespair as pr WHERE\
	  pk.person_1_id = pr.replyer AND pk.person_2_id = pr.replyee\
	  AND pr.freq > "+str(X)+"\
	);\
	CREATE MATERIALIZED VIEW node (id) AS (\
	  SELECT replyer FROM personrepliespair\
	  UNION\
	  SELECT replyee FROM personrepliespair\
	);\
	"

	withOnlyFriends = "\
	CREATE OR REPLACE VIEW edge (fromnode, tonode, weight) AS (\
	  SELECT person_1_id, person_2_id,1 FROM person_knows\
	  UNION\
	  SELECT person_2_id, person_1_id,1 FROM person_knows\
	);\
	CREATE MATERIALIZED VIEW node (id) AS (\
	  SELECT person_1_id FROM person_knows\
	  UNION\
	  SELECT person_2_id FROM person_knows\
	);\
	"

	graphSearchCommand = "\
	CREATE OR REPLACE FUNCTION dijkstra2(startnode int, endnode int)\
	  RETURNS int AS\
	$BODY$\
	DECLARE\
	    rowcount int;\
	    currentfromnode int;\
	    currentestimate int;\
	BEGIN\
	    CREATE TEMP TABLE nodeestimate\
	    (\
	        id int PRIMARY KEY,\
	        estimate int NOT NULL,\
	        predecessor int NULL,\
	        done boolean NOT NULL\
	    ) ON COMMIT DROP;\
	    INSERT INTO nodeestimate (id, estimate, predecessor, done)\
	        SELECT node.id, 999999999, NULL, FALSE FROM node;\
	    UPDATE nodeestimate SET estimate = 0 WHERE nodeestimate.id = startnode;\
	    GET DIAGNOSTICS rowcount = ROW_COUNT;\
	    IF rowcount <> 1 THEN\
	        DROP TABLE nodeestimate;\
	        RETURN -1;\
	    END IF;\
	    LOOP\
	        currentfromnode := NULL;\
	        SELECT nodeestimate.id, estimate INTO currentfromnode, currentestimate\
		        FROM nodeestimate WHERE done = FALSE AND estimate < 999999999\
		        ORDER BY estimate LIMIT 1;\
	        IF currentfromnode IS NULL OR currentfromnode = endnode THEN EXIT; END IF;\
	        UPDATE nodeestimate SET done = TRUE WHERE nodeestimate.id = currentfromnode;\
	        UPDATE nodeestimate n\
	            SET estimate = currentestimate + weight, predecessor = currentfromnode\
	            FROM edge AS e\
	            WHERE n.id = e.tonode AND n.done = FALSE AND e.fromnode = currentfromnode AND (currentestimate + e.weight) < n.estimate;\
	    END LOOP;\
	    SELECT estimate INTO currentestimate FROM nodeestimate WHERE id = endnode;\
	    RETURN currentestimate;\
	END;\
	$BODY$\
	  LANGUAGE plpgsql VOLATILE\
	  COST 100;\
	 Select * FROM dijkstra2("+str(p1)+","+str(p2)+")\
	 ;"


	if (X < 0):
		query = withOnlyFriends+graphSearchCommand
	else:
		query = withReplyRel+graphSearchCommand


	cur.execute(query)
	output = None
	for record in cur:
		output = record
		break

	if output[0]:
		return output[0]
	else:
		return -1


