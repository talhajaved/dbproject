import config
from query1 import query1
from query2 import query2
import time


fileInput = open(config.test_file_path)
for line in fileInput:
	givenQuery = line.rstrip()
	assert givenQuery[:5] == "query"
	whichQuery = int(givenQuery[5])
	arg = givenQuery[6:].rstrip(")").lstrip("(")
	if (whichQuery == 1):
		inputParsed = arg.split(",")
		inputParsed = [int(e) for e in inputParsed]
		start = time.time()
		print line[:-2]
		print "STARTTIME (in seconds): "+str(start)
		output = query1(inputParsed[0],inputParsed[1],int(inputParsed[2]))
		print "Query Output: ",output
		end = time.time()
		print "ENDTIME (in seconds): "+str(end)
		print "RUNTIME (in seconds): "+str(end - start),'\n'
	elif (whichQuery == 2):
		inputParsed = arg.split(",")
		start = time.time()
		print line[:-2]
		print "STARTTIME (in seconds): "+str(start)
		output = query2(int(inputParsed[0]),inputParsed[1])
		print "Query Output: ",output
		end = time.time()
		print "ENDTIME (in seconds): "+str(end)
		print "RUNTIME (in seconds): "+str(end - start),'\n'


print "Done."

