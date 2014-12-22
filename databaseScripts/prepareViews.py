import psycopg2 as pg
import time, config

def main():

	conn = pg.connect(database=config.db['db'], user=config.db['user'], password=config.db['password'],\
	   host =config.db['host'])
	cur = conn.cursor()

	start = time.time()


	personRepliesPair ="\
	CREATE MATERIALIZED VIEW personreplies\
	AS\
	SELECT commentReplyer.\"hasCreator\" as replyer, commentReplyee.\"hasCreator\" as replyee, count(*) as freq\
	FROM comment as commentReplyer, comment as commentReplyee, comment\
	WHERE comment.\"replyOf\" = 'comment'\
	AND commentReplyer.id = comment.id\
	AND commentReplyee.id = comment.\"replyOfCommentId\"\
	AND commentReplyer.\"hasCreator\" != commentReplyee.\"hasCreator\"\
	GROUP BY commentReplyer.\"hasCreator\", commentReplyee.\"hasCreator\";\
	CREATE MATERIALIZED VIEW personrepliespair\
	AS\
	SELECT freqReplyer.replyer as replyer, freqReplyer.replyee as replyee,\
 								CASE WHEN freqReplyer.freq > freqReplyee.freq THEN freqReplyee.freq\
 								     ELSE freqReplyer.freq\
 								     END\
	FROM PersonReplies as freqReplyer, PersonReplies as freqReplyee\
	WHERE freqReplyer.replyee = freqReplyee.replyer\
	AND freqReplyer.replyer = freqReplyee.replyee\
	;"

	personTagPair ="\
	CREATE MATERIALIZED VIEW knowntagpairs\
	AS\
	select person_knows.person_1_id as id1, person_knows.person_2_id as id2, tag.name as tagname,\
	Case When person1.birthday < person2.birthday THEN person1.birthday\
		 ELSE person2.birthday\
		 END\
	from person_knows, Person as person1, Person as person2, \
	person_has_interest as hasInterest1, person_has_interest as hasInterest2, Tag\
	where person1.id = hasInterest1.person_id\
	AND person2.id = hasInterest2.person_id\
	AND hasInterest1.tag_id = tag.id\
	AND hasInterest2.tag_id = tag.id\
	AND person_knows.person_1_id = person1.id\
	AND person_knows.person_2_id = person2.id\
	AND person_knows.person_1_id < person_knows.person_2_id\
	;"

	def runGetTime(cur,command):
		start = time.time()
		cur.execute(command)
		end = time.time()
		return end - start

	print "VIEW                   |COPY TIME (seconds)         "
	print "psRepliesPair     |"+ str(runGetTime(cur,personRepliesPair))
	print "personTagPair     |"+ str(runGetTime(cur,personTagPair))

	conn.commit()
	cur.close()
	conn.close()

if __name__ == "__main__":
  main()
