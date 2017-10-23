import fnmatch
import os
import re
import random
import requests
import time
import subprocess


#from git import Repo

sha1 = ""
def fuzzing():
	print "kiran krishnan"
	files = []
        dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        #print dir_name 
	for root, dirnames, filenames in os.walk(dir_name):
		for filename in fnmatch.filter(filenames, '*.java'):
			if "model" in root or "mysql" in root:
				continue
			#print filename
			files.append(os.path.join(root, filename))
	for file_name in files:
		if "model" in file_name or "mysql" in file_name:
			print file_name
		#print i,"\n"
		f = open(file_name, 'r')
		lines = f.readlines()
		#lines = [" if(openAccordion < nID)", " if(openAccordion << nID)"]
		#print lines
		#break
		# To swap <
		lt = random.randint(1,1001)
		gt = random.randint(1,1001)
		eq = random.randint(1,1001)
		neq = random.randint(1,1001)
		one = random.randint(1,1001)
		zero = random.randint(1,1001)
		chgStr = random.randint(1,1001)
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
					if(lt >= 375 and lt < 500):
						line = re.sub('!=','==',line)
					#print "---------------------------------------END------------------------------"
					#print line,"\n"
					#print "!= fuzzed"

			if(re.match('(.*)0(.*)',line) is not None):
				#print"---------------------------------------START----------------------------"
				#print line,"\n"
				if(lt >= 500 and lt < 625):
					line = re.sub('0','1',line)
				#print "---------------------------------------END------------------------------"
				#print line,"\n"
				#print "0 fuzzed"
	
			if(re.match('(.*)1(.*)',line) is not None):
				#print"---------------------------------------START----------------------------"
				#print line,"\n"
				if(lt >= 625 and lt < 750):
					line = re.sub('1','0',line)
				#print "---------------------------------------END------------------------------"
				#print line,"\n"                      
				#print "1 fuzzed"
 	                        
			if(re.match('.*\"(.*)\".*',line) is not None) and (re.match('\".*\\.*\"',line) is not None) and (re.match('\".*@.*\"',line) is not None):
				#print"---------------------------------------START----------------------------"
				#print line,"\n"
				if(lt >= 750 and lt <= 1001):
					match = re.search(".*(\".*\").*",line)
					line = line.replace(match.group(1),"\"shit\"")
				#print "---------------------------------------END------------------------------"
				#print line,"\n"                      
				#print "string fuzzed"

			lines2.append(line)

		#if set(lines2) == set(lines):
			#print "false"
		#else:
			#print "true"
		os.system('chmod 777 ' + file_name)
		fout = open(file_name,'w')
		for l in lines2:
			fout.write(l)
		#print(file_name)
		
def gitcommit(i):
	#os.system('git add . && git commit -m "fuzzed %d"' %i)
	os.system('git add --all . && git commit -am "fuzzed %d"' %i)
	sha1 = os.popen('git rev-parse HEAD').read()
	print sha1

def revertcommit(i,sha):
	while True:
		response = requests.get('http://159.203.180.176:8080/job/itrust_test2/4/api/json',
								auth=('admin', 'ece6144f110d430586988c71da1f3ae1'))
		data = response.json()
		try: 
			
			if data['building'] != False:
				time.sleep(5)
				continue
			os.system('git checkout %s' %sha)
			break
		except ValueError:
			print data

def main():
	for i in range(1):
		os.system('git checkout -B fuzzer')
		fuzzing()
		gitcommit(i)
		#revertcommit(i,sha1)


if __name__ == "__main__":
	main()

