from runQuery1 import query1SQL
from dbUtilities import createDB, deleteDB
import createTables, insertData, prepareViews, runQuery1
import psycopg2 as pg
import time, config

def connectToDB():
  conn = pg.connect(database=config.db['db'], user=config.db['user'], password=config.db['password'],\
   host =config.db['host'])
  return conn


print "Deleting database "+config.db['db']+" if already exists....\n"
deleteDB()

print "Now creating database "+config.db['db']+"...\n"
createDB()

print "Now creating the schema...\n"
createTables.main()

print "Now loading data from folder "+config.csv_files_input_directory+"...\n"
insertData.main()

print "Now creating the materialized views...\n"
prepareViews.main()

print"Running the queries now ..."

fileInput = open(config.test_file_path)
for line in fileInput:
	conn = connectToDB()
	cur = conn.cursor()
	givenQ = line.rstrip()
	assert givenQ[:5] == "query"
	whichQ = int(givenQ[5])
	arg = givenQ[6:].rstrip(")").lstrip("(")
	if (whichQ == 1):
		inputParsed = arg.split(",")
		inputParsed = [int(e) for e in inputParsed]
		start = time.time()
		print line[:-1]
		print "STARTTIME (in seconds): "+str(start)
		output = query1SQL(inputParsed[0],inputParsed[1],inputParsed[2],cur)
		print "Query Output: ",output
		end = time.time()
		print "ENDTIME (in seconds): "+str(end)
		print "RUNTIME (in seconds): "+str(end - start),'\n'
	cur.close()
	conn.close()

print "Completed."
