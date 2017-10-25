import fnmatch
import os
import re
import random
import requests
import time
import subprocess
from useless import useless


#from git import Repo

sha1 = ""

def fuzzing():
	#print "kiran krishnan"
	files = []
        dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        #print dir_name 
	for root, dirnames, filenames in os.walk(dir_name):
		for filename in fnmatch.filter(filenames, '*.java'):
			if "model" in root or "mysql" in root or "test" in root or "AddApptRequestAction.java" in filename:
				continue
			#print filename
			files.append(os.path.join(root, filename))
	for file_name in files:
		#if "model" in file_name or "mysql" in file_name or "test" in file_name or "AddApptRequestAction.java" in file_name:
			#print file_name
		
		#print i,"\n"
		f = open(file_name, 'r')
		lines = f.readlines()
		#lines = [" if(openAccordion < nID)", " if(openAccordion << nID)"]
		#print lines
		#break
		# To swap <
		lt = random.randint(1,1001)
		#print lt
		lines1 = lines
		lines2 = []
		for line in lines:
				
			#print(line,': ----------------------------------------------------------inside for')
			if(re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				#print (line,": ---------------------------------------------------inside if if")
				if(re.match('(.*)<(.*)',line) is not None ) and (re.match('.*<.+>.*',line) is None):
					#print"---------------------------------------START----------------------------"
					#print line,"\n"
					if(lt < 125):
						line = re.sub('<','>',line)
					#print "---------------------------------------END------------------------------"
					#print line,"\n"
					#print "< fuzzed"

			if(re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
	                        #print (line,": ---------------------------------------------------inside if if")
				if(re.match('(.*)>(.*)',line) is not None) and (re.match('.*<.+>.*',line) is None):
					#print"---------------------------------------START----------------------------"
					#print line,"\n"
					if(lt >= 125 and lt < 250):
						line = re.sub('>','<',line)
					#print "---------------------------------------END------------------------------
					#print line,"\n"                        
					#print "> fuzzed"

			if(re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				#print (line,": ---------------------------------------------------inside if if")
				if(re.match('(.*)==(.*)',line) is not None):
					#print"---------------------------------------START----------------------------"
					#print line,"\n
					if(lt >= 250 and lt < 375):
						line = re.sub('==','!=',line)
					#print "---------------------------------------END------------------------------"
					#print line,"\n"
					#print "= fuzzed"

			if(re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				#print (line,": ---------------------------------------------------inside if if")
				if(re.match('(.*)!=(.*)',line) is not None):
					#print"---------------------------------------START----------------------------"
					#print line,"\n"
					if(lt >= 375 and lt < 700):
						line = re.sub('!=','==',line)
					#print "---------------------------------------END------------------------------"
					#print line,"\n"
					#print "!= fuzzed"

			#if(re.match('(.*)&&(.*)',line) is not None) and (re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				#print"---------------------------------------START----------------------------"
				#print line,"\n"
			#	if(lt >= 500 and lt < 625):
			#		line = re.sub('&&','||',line)
				#print "---------------------------------------END------------------------------"
				#print line,"\n"
				#print "0 fuzzed"
	
			#if(re.match('(.*)||(.*)',line) is not None) and (re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				#print"---------------------------------------START----------------------------"
				#print line,"\n"
			#	if(lt >= 625 and lt < 750):
			#		line = re.sub('||','&&',line)
				#print "---------------------------------------END------------------------------"
				#print line,"\n"                      
				#print "1 fuzzed"
 	                        
			if(re.match('.*\"(.*)\".*',line) is not None) and (re.match('\".*\\.*\"',line) is not None) and (re.match('\".*@.*\"',line) is not None):
				#print"---------------------------------------START----------------------------"
				#print line,"\n"
				if(lt >= 700 and lt <= 1001):
					match = re.search(".*(\".*\").*",line)
					line = line.replace(match.group(1),"\"ThisISRanDOm\"")
				#print "---------------------------------------END------------------------------"
				#print line,"\n"                      
				#print "string fuzzed"

			lines2.append(line)

		#if set(lines2) == set(lines):
			#print file_name
		#else:
			#print "true"
		#os.system('chmod 777 ' + file_name)
		fout = open(file_name,'w')
		for l in lines2:
			fout.write(l)
		#print(file_name)
		
def gitcommit(i):
	#os.system('git add . && git commit -m "fuzzed %d"' %i)
	os.system('git add --all . && git commit -am "fuzzed %d"' %(i+1))
	sha1 = os.popen('git rev-parse HEAD').read()
	#print sha1

def revertcommit(sha):
	
	
        response = requests.get('http://159.203.180.176:8080/job/itrust_job2/api/json',
                                 auth=('admin', 'e1c89f67a1b4440fb1dd4dd3c4cf41aa'))
        data = response.json()
        buildNumber = data['nextBuildNumber']
	#time.sleep(5)
	while True:
		#print 'http://159.203.180.176:8080/job/itrust_job2/' + str(buildNumber)  + '/api/json'                
		try:
			response = requests.get('http://159.203.180.176:8080/job/itrust_job2/' + str(buildNumber)  + '/api/json',
								auth=('admin', 'e1c89f67a1b4440fb1dd4dd3c4cf41aa'))
			data = response.json()
			
			if data['building'] != False:
				#time.sleep(5)
				continue
			os.system('git checkout master && git branch -D fuzzer')
			break

		except ValueError:
			#print data
			continue
	return buildNumber

#	print "-----------------------------------"
#	print data
def main():
	builds = []
	for i in range(1000):

		os.system('git checkout -B fuzzer')
		fuzzing()
		gitcommit(i)
		builds.append(revertcommit(sha1))
	useless(builds)
	#print builds

if __name__ == "__main__":
	main()

