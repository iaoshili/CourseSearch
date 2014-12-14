import wikipedia
'''
Get a list of key words related to the query knowledge key word, intentionally remove the query word if it appears.
'''
def getRelatedKeyWord(knowledgeKeyWord):
	returnList = []
	wikiPage = wikipedia.page(knowledgeKeyWord)
	summary = wikiPage.summary
	relatedKeyWordList = wikiPage.links	
	indexToRemove = -1
	for i in xrange(0,len(relatedKeyWordList)):
		if relatedKeyWordList[i].lower() in summary.lower():
			returnList.append(relatedKeyWordList[i])

	if indexToRemove != -1:
		del relatedKeyWordList[indexToRemove]

	returnList.append(knowledgeKeyWord)

	return returnList

a = [5,3,4]
print a
[39, 35, 106, 105, 37]
