import sys
import re

buildslist = []

def useless(buildslist):
    logdict = {}
    buildslist = [112,113,114,115,116,117,118,119,120,121]
    listlen = len(buildslist)
    for i in buildslist:
        with open('/var/lib/jenkins/jobs/itrust_test2/builds/'+str(i)+'/log', 'r') as logfile:
            logdata_list=logfile.readlines()
        #print logdata_list[4]
        loglen = len(logdata_list)
        print "Length of logs"+str(i)+" : "+str(loglen)
        j = 0
        while (j<loglen):
            test = re.search("Tests run: \d+, Failures: 0,.*- in (.*)\n",logdata_list[j])
	    if test:
    	        #print test.group(1)
		if (logdict.has_key(test.group(1))):
		    temp = logdict.get(test.group(1))
                    if temp:
                        temp+=1
                        logdict.update({test.group(1):temp})
	        else:
	     	    logdict.update({test.group(1):1})
                    #print logdict	
	    j+=1
        #i+=1
    values = logdict.values()
    logtestlist = logdict.keys()
    vallen = len(values)
    uselesstests = []
    for i in range(vallen):
	if values[i]==listlen:
	    uselesstests.append(logtestlist[i])

    logfile.close()
    print uselesstests
    print "Number of useless tests: "+str(len(uselesstests))
    print "Exited Useless test detector!"


#useless(buildslist)
