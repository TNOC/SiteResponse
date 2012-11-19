#!/usr/bin/python

import time
import httplib

class responseClass:
	count = 0
	status = 0;
	text = "undefined"
	def __init__(self, tempStatus, tempText):
		self.count = 0
		self.status = tempStatus
		self.text = tempText

	def incrementCount(self):
		self.count = self.count + 1

def printResponseCodes ( list ):
	print "%-7s %-30s %-18s" % ("Status", "Text", "Count")
	for key, item in list.items():
		print "%-7s %-30s %-18s" % (item.status, item.text, item.count)
	print "\n"

def printGoodVsBad ( list, count):
	goodCount = list[200].count
	badCount = count - goodCount

	print "Good: ", goodCount, " Bad: ", badCount

httpStatusCodes = {}
httpStatusCodes[100] = responseClass("100", "CONTINUE");
httpStatusCodes[101] = responseClass("101", "SWITCHING_PROTOCOLS");
httpStatusCodes[102] = responseClass("102", "PROCESSING");

httpStatusCodes[200] = responseClass("200", "OK");
httpStatusCodes[201] = responseClass("201", "CREATED");
httpStatusCodes[202] = responseClass("202", "ACCEPTED");
httpStatusCodes[203] = responseClass("203", "NON_AUTHORITATIVE_INFORMATION");
httpStatusCodes[204] = responseClass("204", "NO_CONTENT");
httpStatusCodes[205] = responseClass("205", "RESET_CONTENT");
httpStatusCodes[206] = responseClass("206", "PARTIAL_CONTENT");
httpStatusCodes[207] = responseClass("207", "MULTI_STATUS");
httpStatusCodes[226] = responseClass("200", "IM_USED");

httpStatusCodes[300] = responseClass("300", "MULTIPLE_CHOICES");
httpStatusCodes[301] = responseClass("301", "MOVED_PERMANENTLY");
httpStatusCodes[302] = responseClass("302", "FOUND");
httpStatusCodes[303] = responseClass("303", "SEE_OTHER");
httpStatusCodes[304] = responseClass("304", "NOT_MODIFIED");
httpStatusCodes[305] = responseClass("305", "USE_PROXY");
httpStatusCodes[307] = responseClass("307", "TEMPORARY_REDIRECT");

httpStatusCodes[400] = responseClass("400", "BAD_REQUEST");
httpStatusCodes[401] = responseClass("401", "UNAUTHORIZED");
httpStatusCodes[402] = responseClass("402", "PAYMENT_REQUIRED");
httpStatusCodes[403] = responseClass("403", "UNAUTHORIZED");
httpStatusCodes[404] = responseClass("404", "NOT_FOUND");





count = 1

while (count <= 10):
	#print 'Count ', count
	
	conn = httplib.HTTPConnection('choiceadvantage.com', 80)

	#conn.set_debuglevel(1)

	conn.connect()
	request = conn.putrequest('POST', '/')
	
	headers = {}
	headers['Content-Type'] = 'application/json'
	headers['User-Agent'] = 'Envjs/1.618 (SpyderMonkey; U; Linux x86_64 2.6.38-10-generic;  pl_PL.utf8; rv:2.7.1) Resig/20070309 PilotFish/1.3.pre03'
	headers['Accept'] = '*/*'
	
	for k in headers:
	    conn.putheader(k, headers[k])
	conn.endheaders()
	
	conn.send('[{"id":"route"}]')

	resp = conn.getresponse()
	#print resp.status
	#print resp.reason
	#print resp.read()

	httpStatusCodes[resp.status].incrementCount()

	print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

	printResponseCodes( httpStatusCodes )
	printGoodVsBad( httpStatusCodes, count )
	
	print "\n\n"

	conn.close()

	if (count % 30 == 0): #save to file once an hour
		writeFile = open("output.txt", "a+")

		writeFile.write( time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) )
		writeFile.write( "\t" )
		writeFile.write( "Good: " )
		writeFile.write( repr(httpStatusCodes[200].count) )
		writeFile.write( " Bad: " )
		writeFile.write( repr(count - httpStatusCodes[200].count)  )
		writeFile.write( "\n\n")

		writeFile.close()

	count = count + 1

	#sleep works with seconds so (minutes * 60)
	time.sleep(5 * 60) #every five minutes

print "Exiting"
