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


	def runGetTime(cur,command):
		start = time.time()
		cur.execute(command)
		end = time.time()
		return end - start

	print "TABLE             |COPY TIME (seconds)         "
	print "psRepliesPair     |"+ str(runGetTime(cur,personRepliesPair))

	conn.commit()
	cur.close()
	conn.close()

if __name__ == "__main__":
  main()
