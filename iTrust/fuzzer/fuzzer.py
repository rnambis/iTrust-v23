import matplotlib
matplotlib.use('Agg')
import fnmatch
import os
import re
import random
import requests
import time
import subprocess
from useless_iteration import useless
from matplotlib import pyplot as plt
passing = []

#from git import Repo

sha1 = ""

def fuzzing():
	files = []
        dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	for root, dirnames, filenames in os.walk(dir_name):
		for filename in fnmatch.filter(filenames, '*.java'):
			if "model" in root or "mysql" in root or "test" in root or "AddApptRequestAction.java" in filename:
				continue
			files.append(os.path.join(root, filename))
	for file_name in files:
			#print file_name
		
		#print i,"\n"
		f = open(file_name, 'r')
		lines = f.readlines()
		lt = random.randint(1,1000)
		#lines = [" if(openAccordion < nID)", " if(openAccordion << nID)"]
		#print lines
		#break
		# To swap <
		#print lt
		lines1 = lines
		new_lines = []
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
					if(lt >= 250 and lt < 600):
						line = re.sub('==','!=',line)
					#print "---------------------------------------END------------------------------"
					#print line,"\n"
					#print "= fuzzed"

			if(re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				#print (line,": ---------------------------------------------------inside if if")
				if(re.match('(.*)!=(.*)',line) is not None):
					#print"---------------------------------------START----------------------------"
					#print line,"\n"
					if(lt >= 600 and lt < 900):
						line = re.sub('!=','==',line)
					#print "---------------------------------------END------------------------------"
					#print line,"\n"
					#print "!= fuzzed"

			#if(re.match('(.*) 0(.*)',line) is not None) and (re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				#print"---------------------------------------START----------------------------"
				#print line,"\n"
				#if(lt >= 500 and lt < 625):
					#line = re.sub(' 0',' 1',line)
				#print "---------------------------------------END------------------------------"
				#print line,"\n"
				#print "0 fuzzed"
	
			#if(re.match('(.*) 1(.*)',line) is not None) and (re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				#print"---------------------------------------START----------------------------"
				#print line,"\n"
			#	if(lt >= 625 and lt < 700):
			#		line = re.sub(' 1',' 0',line)
				#print "---------------------------------------END------------------------------"
				#print line,"\n"                      
				#print "1 fuzzed"
 	                        
			if(re.match('.*\"(.*)\".*',line) is not None) and (re.match('\".*\\.*\"',line) is not None) and (re.match('\".*@.*\"',line) is not None):
				#print"---------------------------------------START----------------------------"
				#print line,"\n"
				if(lt >= 900 and lt <= 1000):
					match = re.search(".*(\".*\").*",line)
					line = line.replace(match.group(1),"\"ThisISRanDOm\"")
				#print "---------------------------------------END------------------------------"
				#print line,"\n"                      
				#print "string fuzzed"

			new_lines.append(line)

		#if set(lines2) == set(lines):
			#print file_name
		#else:
			#print "true"
		#os.system('chmod 777 ' + file_name)
		f.close()
		fout = open(file_name,'w')
		for l in new_lines:
			fout.write(l)
		#print(file_name)
		fout.close()
		
def gitcommit(i):
	#os.system('git add . && git commit -m "fuzzed %d"' %i)
	os.system('git add --all . && git commit -am "fuzzed %d"' %(i+1))
	sha1 = os.popen('git rev-parse HEAD').read()
	#print sha1

def revertcommit(sha):
	
	#pass = os.popen('cat /var/lib/jenkins/secrets/initialAdminPassword').read().strip()
        response = requests.get('http://127.0.0.1:8080/job/itrust_job2/api/json',
                                 auth=('admin', '1536380596b840d597ba68ffafd69f7e'))
        data = response.json()
        buildNumber = data['nextBuildNumber']
	#time.sleep(5)
	while True:
		#print 'http://159.203.180.176:8080/job/itrust_job2/' + str(buildNumber)  + '/api/json'                
		try:
			response = requests.get('http://127.0.0.1:8080/job/itrust_job2/' + str(buildNumber)  + '/api/json',
								auth=('admin', '1536380596b840d597ba68ffafd69f7e'))
			data = response.json()
			
			if data['building'] == False:
				#time.sleep(5)
				os.system('git stash && git checkout -f master && git branch -D fuzzer')
				break

		except ValueError:
			#print data
			continue
	return buildNumber

#	print "-----------------------------------"
#	print data
def main():
	builds = []
	for i in range(100):
		os.system('git checkout -B fuzzer')
		fuzzing()
		gitcommit(i)
		builds.append(revertcommit(sha1))
		print "build "+str(i)+" over, useless called" 
		val = useless(builds)
		print "useless done"
		passing.append(val)
		print passing
	x = [j+1 for j in xrange(100)]
	plt.plot(x,passing)
	plt.xlabel('Build Number')
	plt.ylabel('No of passing tests')
	plt.savefig('/var/lib/jenkins/tests.png')
	#print builds

if __name__ == "__main__":
	main()

