import os  
import re

#Abandoned, in current system, just use path with space in it and open method will recognize it
#E.x. f = open("~/Desktop/path with space.txt")
def changeToLinuxPath( path ):
	linuxFormPath = ''
	splitBySpaceParts = path.split()
	for i in range(len(splitBySpaceParts)):
		if splitBySpaceParts[i] == "|":
			linuxFormPath += '\\'
		if i == len(splitBySpaceParts) - 1:
			linuxFormPath += splitBySpaceParts[i]
			break
		linuxFormPath += splitBySpaceParts[i] + "\ "
	return linuxFormPath

courseName = "statistical mechanics_ algorithms and computations"
courseNameLine = "  Statistical Mechanics: Algorithms and Computations"

courseNameSplit = re.split('; |, |\*|\n|_ | |: ',courseName)
couseNameWithoutSplit = " ".join(courseNameSplit)

courseNameLineSplit = re.split('; |, |\*|\n|_ | |: ',courseNameLine)

if courseNameSplit in courseNameLineSplit:
	print "Yeah"
# courseNameLWOSplit = "".join(couseNameWithoutSplit)
# print couseNameWithoutSplit
# SearchDir = "/Users/Greyjoy/Documents/Lab/Davis/CourseIntro/"
# result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(SearchDir) for f in filenames if os.path.splitext(f)[1] == '.html']
# f = open(result[0])
# lines = f.readlines()


# def checkIfExist( path, knowledgeKeyWord, CourseName):
# 	courseFound = False
	# f = open(path)
	# lines = f.readlines()

	# for i in range(0,len(lines)):
	# 	if knowledgeKeyWord in lines[i]:
	# 		courseFound = True
	# 		break

	# if courseFound == True:
	# 	print "Possible course found: "+CourseName + "\n"

	# 	for i in range(0,len(lines)):
	# 		if knowledgeKeyWord in lines[i]:
	# 			courseFound = True
	# 			print lines[i]
	# 			print lines[i+1]
	# 			break

	# if courseFound == True:
	# 	print "=============================" +"\n"
	# f.close()

# '''
# Return a list containing all the classes' names. And remove duplicate.
# '''
# def getCourseNameList(SearchDir):
# 	courseNameSet = Set()
# 	courseNameList = []
# 	'''
# 	Recursively find all the file path in searchDir, and save them to a list.
# 	'''
# 	result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(SearchDir) for f in filenames if os.path.splitext(f)[1] == '.html']
# 	'''
# 	For each of the path name in the list, change them to the format that is 
# 	readable by linux system, and check if the given key word exist.
# 	'''
# 	for i in range(len(result)):
# 		CourseName = os.path.basename(result[i])[:-16]
# 		if CourseName not in courseNameSet:			
# 			linuxPath = changeToLinuxPath(result[i])
# 			courseNameSet.add(CourseName)
# 			courseNameList.append(result[i])
# 			# checkIfExist(result[i], knowledgeKeyWord, CourseName)
# 	return courseNameList

#-q: quit silently
#-r: recursively find 
#-i: ignore case
#-m 1: max-count, stop reading the file after num matches
# if call(['egrep', '-r', '-i', '-m', '1',  KnowledgeToLearn, SearchDir]) == 0:
# 	print "Right place to learn!"
# else:
# 	print 'Oops. Not Found.'

#~/Documents/Lab/Davis/CourseIntro/Computer\ Science\ Artificial\ Intelligence/Artificial\ Intelligence\ Planning\ \|\ Coursera.html


#The awk method, which is awkward to use
# def checkIfExist( path, knowledgeKeyWord, CourseName):
# 	script = "awk -v courseName = $CourseName 'BEGIN {IGNORECASE = 1;}" + \
# 	" /" +knowledgeKeyWord + "/ " + "END {}' "+path
# 	print script
# 	call(script, shell=True)
# 	subprocess.check_output(script, shell=True)
# 	# print subprocess.check_output(call(script, shell = True))
# 	if result == "":
# 		print("empty")