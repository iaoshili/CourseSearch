#!/usr/bin/python
from subprocess import call
import wikipedia
from sets import Set
import subprocess
import os
import re


'''
Get a list of key words related to the query knowledge key word, intentionally remove the query word if it appears.
'''
def getRelatedKeyWord(knowledgeKeyWord):
	wikiPage = wikipedia.page(knowledgeKeyWord)
	RelatedKeyWordList = wikiPage.links	
	indexToRemove = -1
	for i in xrange(0,len(RelatedKeyWordList)):
		if knowledgeKeyWord.lower() == RelatedKeyWordList[i].lower():
			indexToRemove = i
			break

	if indexToRemove != -1:
		del RelatedKeyWordList[indexToRemove]

	return wikiPage.links

'''
Return a list of weights assigned to the words related to the knowledge key word given.
'''
def getSearchQueryWeights(knowledgeKeyWord, relatedKeyWordList):
	wikiPage = wikipedia.page(knowledgeKeyWord)
	summary = wikiPage.summary
	searchQueryWeights = []

	for i in xrange(0,len(relatedKeyWordList)):		
		if relatedKeyWordList[i].lower() in summary.lower():
			searchQueryWeights.append(4) #Give weight 4 for words in summary
		else:
			searchQueryWeights.append(1) #Give weight 1 for word appear anywhere else

	return searchQueryWeights

'''
Return a list containing all the classes' paths and a list of course names. And remove duplicate.
'''
def getCoursesPathListAndNameList(SearchDir):
	# knowledgeKeyWord = raw_input("Please enter the knowledge you want to learn: ")
	courseNameSet = Set()
	coursesPathList = []
	courseNameList = []

	'''
	Recursively find all the file path in searchDir, and save them to a list.
	'''
	result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(SearchDir) for f in filenames if os.path.splitext(f)[1] == '.html']
	'''
	For each of the path name in the list, change them to the format that is 
	readable by linux system, and check if the given key word exist.
	'''
	for i in range(len(result)):
		CourseName = os.path.basename(result[i])[:-16]		
		if CourseName not in courseNameSet:			
			courseNameSet.add(CourseName)
			coursesPathList.append(result[i])
			courseNameList.append(CourseName)

	pathAndNameList = [coursesPathList,courseNameList]
	return pathAndNameList

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


def getCourseWeights(knowledgeKeyWord, relatedKeyWordList, coursesPathList,courseNameList):
	SectionList = {"About the Course":8, "Course Syllabus":7, "Categories":7,"Related Courses":3,
	"Recommended Background":3,"In-course Textbooks":5,"Suggested Readings":5,"FAQ":3}
	courseAllWeighList = []
	courseWeightList = []

	for i in xrange(0,len(relatedKeyWordList)):
		courseWeightList.append(0)

	for i in xrange(0,len(coursesPathList)):
		courseSummaryBeginLine = 0

		path = coursesPathList[i]
		courseName = courseNameList[i]
		
		f = open(path)
		lines = f.readlines()

		scoreToThisSection = 0

		#Iterate through the current file
		for i in range(0,len(lines)):
			currLine = lines[i]

			#Assign score to this section
			for section in SectionList.keys():
				if section in currLine:
					scoreToThisSection = SectionList.get(section)
					break

			for i in xrange(0,len(relatedKeyWordList)):
				if relatedKeyWordList[i].lower() in currLine.decode('utf-8').lower():
					courseWeightList[i] = max(courseWeightList[i], scoreToThisSection)
					f.close()

		#If you don't copy the data, you will overwrite them.
		courseWeightListToAdd = courseWeightList[:]
		courseAllWeighList.append(courseWeightListToAdd)

		for i in xrange(0,len(relatedKeyWordList)):
			courseWeightList[i] = 0

	return courseAllWeighList

def	Rank(knowledgeKeyWord, searchQueryWeights, allCoursesWeightList, courseNameList):
	NumToShow = 10
	scoreIfCourseNameMatch = 80
	scoreToThisCourse = []
	IndexOfTopCourse = []

	for i in xrange(0,len(courseNameList)):
		currCourseName = courseNameList[i]
		courseNameSplit = re.split('; |, |\*|\n|_ | |: ',currCourseName)
		couseNameWithoutSplit = " ".join(courseNameSplit)

		if knowledgeKeyWord.lower() in couseNameWithoutSplit.lower():
			scoreToThisCourse.append(scoreIfCourseNameMatch)
		else:
			scoreToThisCourse.append(0)

	#Iterate through all the courses
	for i in xrange(0,len(courseNameList)):		
		for j in xrange(0,len(searchQueryWeights)):
			scoreToThisCourse[i] += searchQueryWeights[j]*allCoursesWeightList[i][j]

	#Sort reference: http://stackoverflow.com/questions/6422700/how-to-get-indices-of-a-sorted-array-in-python
	#This weird snippet of code will do this: input [1, 2, 3, 100, 5], ouput:[0, 1, 2, 4, 3]
	sortedList = [i[0] for i in sorted(enumerate(scoreToThisCourse), key=lambda x:x[1])]
	for i in xrange(0,NumToShow):
		currCourseIndex = 0
		currPosition = len(courseNameList) - i - 1
		for i in xrange(0,len(sortedList)):
			if sortedList[i] == currPosition:
				currCourseIndex = i
				break
		IndexOfTopCourse.append(currCourseIndex)

	return IndexOfTopCourse

def printResult(IndexOfTopCourse, coursesPathList,courseNameList, knowledgeKeyWord):
	for i in xrange(0,len(IndexOfTopCourse)):
		path = coursesPathList[i]
		CourseName = courseNameList[i]
		f = open(path)
		lines = f.readlines()

		print "Possible course found: "+CourseName + "\n"

		for j in range(0,len(lines)):
			if knowledgeKeyWord in lines[j]:
				print lines[j]
				print lines[j+1]
				break

		print "=============================" +"\n"

		f.close()

# main()
