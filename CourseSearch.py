#!/usr/bin/python
from subprocess import call
import wikipedia
from sets import Set
import subprocess
import os
import re

class CourseSearch:	

	def __init__(self, knowledgeKeyWord, searchDir):
		self.knowledgeKeyWord = knowledgeKeyWord
		self.searchDir = searchDir

		self.coursesPathList = []
		self.courseNameList = []
		self.getCoursesPathListAndNameList()

		self.relatedKeyWordList = self.getRelatedKeyWord()
		self.queryWeightList = self.getQueryWeightList()
		self.coursesWeightList = self.getCoursesWeightList()
		self.coursesScoreList = self.getCoursesScoreList()

	'''
	Return a list containing all the classes' paths and a list of course names. And remove duplicate.
	'''
	def getCoursesPathListAndNameList(self):
		courseNameSet = Set()

		'''
		Recursively find all the file path in searchDir, and save them to a list.
		'''
		result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(self.searchDir) for f in filenames if os.path.splitext(f)[1] == '.html']
		'''
		For each of the path name in the list, change them to the format that is 
		readable by linux system, and check if the given key word exist.
		'''
		for i in range(len(result)):
			CourseName = os.path.basename(result[i])[:-16]		
			if CourseName not in courseNameSet:			
				courseNameSet.add(CourseName)
				self.coursesPathList.append(result[i])
				self.courseNameList.append(CourseName)

	'''
	Get a list of key words related to the query knowledge key word, 
	intentionally set the query word to be the last one of the list.
	'''
	def getRelatedKeyWord(self):
		wikiPage = wikipedia.page(self.knowledgeKeyWord)
		relatedKeyWordList = wikiPage.links	
		indexToRemove = -1
		for i in xrange(0,len(relatedKeyWordList)):
			if self.knowledgeKeyWord.lower() == relatedKeyWordList[i].lower():
				indexToRemove = i
				break

		if indexToRemove != -1:
			del relatedKeyWordList[indexToRemove]

		relatedKeyWordList.append(self.knowledgeKeyWord)

		return relatedKeyWordList

	'''
	Return a list of weights assigned to the words related to the knowledge key word given.
	Give a tremendously big weight to the knowledgeKeyWord
	'''
	def getQueryWeightList(self):
		weightForQueryWord = 10

		wikiPage = wikipedia.page(self.knowledgeKeyWord)
		summary = wikiPage.summary
		queryWeightList = []	

		for i in xrange(0,len(self.relatedKeyWordList)-1):		
			if self.relatedKeyWordList[i].lower() in summary.lower():
				queryWeightList.append(4) #Give weight 4 for words in summary
			else:
				queryWeightList.append(0) #Give weight 0 for word appear anywhere else
		queryWeightList.append(weightForQueryWord)

		return queryWeightList

	'''
	Return a list, each element is itself a weight list for the course in that index
	'''
	def getCoursesWeightList(self):
		SectionList = {"About the Course":8, "Course Syllabus":7, "Categories":7,"Related Courses":3,
		"Recommended Background":3,"In-course Textbooks":5,"Suggested Readings":5,"FAQ":3}
		coursesWeightList = []
		courseWeightList = []

		for i in xrange(0,len(self.relatedKeyWordList)):
			courseWeightList.append(0)

		for i in xrange(0,len(self.coursesPathList)):
			courseSummaryBeginLine = 0

			path = self.coursesPathList[i]
			courseName = self.courseNameList[i]
			
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

				for i in xrange(0,len(self.relatedKeyWordList)):
					if self.relatedKeyWordList[i].lower() in currLine.decode('utf-8').lower():
						courseWeightList[i] += scoreToThisSection
			
			f.close()

			#If you don't copy the data, you will overwrite them.
			courseWeightListToAdd = courseWeightList[:]
			coursesWeightList.append(courseWeightListToAdd)

			for i in xrange(0,len(self.relatedKeyWordList)):
				courseWeightList[i] = 0

		return coursesWeightList

	def getCoursesScoreList(self):
		scoreIfCourseNameMatch = 1000
		scoreList = []
		score = 0.0
		for i in xrange(0,len(self.courseNameList)):
			for j in xrange(0,len(self.queryWeightList)):
				score += self.queryWeightList[j]*self.coursesWeightList[i][j]
				currCourseName = self.courseNameList[i]

			courseNameSplit = re.split('; |, |\*|\n|_ | |: ',currCourseName)
			couseNameWithoutSplit = " ".join(courseNameSplit)
			if self.knowledgeKeyWord.lower() in couseNameWithoutSplit.lower():
				score += scoreIfCourseNameMatch

			scoreList.append(score)
			score = 0.0

		return scoreList

	def	rank(self):
		NumToShow = 5
		scoreToThisCourse = []
		IndexOfTopCourse = []
		IndexSet = Set()

		scoreListClone = self.coursesScoreList[:]
		sortedList = sorted(scoreListClone)
		for i in xrange(0,NumToShow):
			score = sortedList[-1-i]
			for j in xrange(0,len(self.coursesScoreList)):
				if self.coursesScoreList[j] == score and j not in IndexSet:
					IndexOfTopCourse.append(j)
					IndexSet.add(j)
					# print self.courseNameList[j]
					# print self.coursesScoreList[j]
					break
		self.printResult(IndexOfTopCourse) 

	def printResult(self, IndexOfTopCourse):
		for i in IndexOfTopCourse:			
			path = self.coursesPathList[i]
			CourseName = self.courseNameList[i]
			f = open(path)
			lines = f.readlines()

			print "Possible course found: "+CourseName + "\n"

			for j in range(0,len(lines)):
				if self.knowledgeKeyWord in lines[j]:
					print lines[j-1]
					print lines[j]
					print lines[j+1]
					break

			print "=============================" +"\n"

			f.close()
