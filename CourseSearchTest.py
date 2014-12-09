from CourseSearch import *

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
	knowledgeKeyWord = "algorithm"
	print getRelatedKeyWord("algorithm")

	# coursePathAndNameList = CourseSearch.getCoursesPathListAndNameList(SearchDir = "/Users/Greyjoy/Documents/Lab/Davis/CourseIntro/")
	# coursesPathList = coursePathAndNameList[0]
	# courseNameList = coursePathAndNameList[1]

main()