from CourseSearch import *

def testCourseWeight():
	knowledgeKeyWord ="Algorithm"

	coursePathAndNameList = getCoursesPathListAndNameList(SearchDir = "/Users/Greyjoy/Documents/Lab/Davis/CourseIntro/")
	coursesPathList = coursePathAndNameList[0]
	courseNameList = coursePathAndNameList[1]

	relatedKeyWordList = getRelatedKeyWord(knowledgeKeyWord)
	searchQueryWeights = getSearchQueryWeights(knowledgeKeyWord, relatedKeyWordList)
	allCoursesWeightList = getCourseWeights(knowledgeKeyWord, relatedKeyWordList, coursesPathList, courseNameList)

	programRank1ClassIndex = -1
	for i in xrange(0,len(courseNameList)):
		if courseNameList[i] == "Artificial Intelligence Planning":
			print i
			break

	print "Algorithm, part II weight: "
	print getCourseScore(searchQueryWeights, allCoursesWeightList[37],knowledgeKeyWord,courseNameList)

	print "AI planning weight:"
	print getCourseScore(searchQueryWeights, allCoursesWeightList[0],knowledgeKeyWord,courseNameList)

def courseIntroHtmlFindCourseNameLocation():
	path = coursesPathList[i]
	courseName = courseNameList[i]
	courseNameSplit = re.split('; |, |\*|\n|_ | |: ',courseNameList[i])
	courseNameWOSplit = " ".join(courseNameSplit)

	f = open(path)
	lines = f.readlines()

	for i in range(0,len(lines)):
		currLine = lines[i]
		currLineSplit = re.split('; |, |\*|\n|_ | |: ',currLine)
		currLineWOSplit = "".join(currLineSplit)
		if courseNameWOSplit.lower() in currLineWOSplit.lower():
			break
	
	print path
	print courseNameWOSplit

def main():
	search = CourseSearch("dynamic programming","/Users/Greyjoy/Documents/Lab/Davis/CourseIntro/")
	print search.courseNameList[37]
	print search.coursesScoreList[37]
	search.rank()
	# print "Score for Algorithm, partII"
	# print search.coursesScoreList[37]
	# print "Score for AI, planning"
	# print search.coursesScoreList[0]

main()