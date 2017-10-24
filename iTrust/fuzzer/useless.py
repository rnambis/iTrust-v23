import sys
import re

buildslist = []

def useless(buildslist):
    logdict = {}
    testdict = {}
    #buildslist = [126,127,128,129,130]
    listlen = len(buildslist)
    for i in buildslist:
        with open('/var/lib/jenkins/jobs/itrust_job2/builds/'+str(i)+'/log', 'r') as logfile:
            logdata_list=logfile.readlines()
        #print logdata_list[4]
        loglen = len(logdata_list)
        print "Length of logs"+str(i)+" : "+str(loglen)
        j = 0
        while (j<loglen):
            test = re.search("Tests run: (\d+), Failures: 0,.*- in (.*)\n",logdata_list[j])
	    if test:
    	        #print test.group(1)
		if (logdict.has_key(test.group(2))):
		    temp = logdict.get(test.group(2))
                    if temp:
                        temp+=1
                        logdict.update({test.group(2):temp})
			testdict.update({test.group(2):int(test.group(1))})
	        else:
	     	    logdict.update({test.group(2):1})
		    testdict.update({test.group(2):int(test.group(1))})
                    #print logdict	
	    j+=1
        #i+=1
    values = logdict.values()
    logtestlist = logdict.keys()
    vallen = len(values)
    uselesstests = []
    uselesscount = 0
    for i in range(vallen):
	if values[i]==listlen:
	    uselesstests.append(logtestlist[i])
	    uselesscount+=testdict[logtestlist[i]]

    logfile.close()
    #print "Length of Dictionary: "+str(len(logdict))
    print uselesstests
    print "Number of useless tests: "+str(uselesscount)
    print "Exited Useless test detector!"



#useless(buildslist)
