import CourseSearch

knowledgeKeyWord ="Algorithm"

coursePathAndNameList = getCoursesPathListAndNameList(SearchDir = "/Users/Greyjoy/Documents/Lab/Davis/CourseIntro/")
coursesPathList = coursePathAndNameList[0]
courseNameList = coursePathAndNameList[1]

relatedKeyWordList = getRelatedKeyWord(knowledgeKeyWord)
searchQueryWeights = getSearchQueryWeights(knowledgeKeyWord, relatedKeyWordList)
allCoursesWeightList = getCourseWeights(knowledgeKeyWord, relatedKeyWordList, coursesPathList, courseNameList)

IndexOfTopCourse = Rank(knowledgeKeyWord, searchQueryWeights, allCoursesWeightList, courseNameList)
printResult(IndexOfTopCourse, coursesPathList, courseNameList, knowledgeKeyWord)
