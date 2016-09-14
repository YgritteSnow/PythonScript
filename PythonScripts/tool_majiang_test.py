# -*- coding: utf-8 -*- 

import random
from tool_conv_csv import CSVLoader

g_needCount = (14, 13, 13, 13, 50)

g_dataMap, t1, t2 = CSVLoader().ParseAll(r"D:\MyProjects\PythonScript\PythonScripts\\majiang_card.csv", r"D:\MyProjects\CocosProject\test\src\\")
g_card_ho = g_dataMap.keys()

def randomCard():
	newCard = -1
	while newCard not in g_card_ho:
		newCard = g_card_ho[random.randint(0, len(g_card_ho)-1)]
	return newCard

def calCurInfo( originLists ):
	resMap = {}
	for handlist in originLists:
		for card in handlist:
			resMap.setdefault(card, 0)
			resMap[card] += 1
	return resMap

def generateTest_supply( originLists ):
	resMap = calCurInfo( originLists )
	for idx, handlist in enumerate(originLists):
		while len(handlist) < g_needCount[idx]:
			newCard = randomCard()
			while resMap.get(newCard, 0) >= g_dataMap[newCard]["count"]:
				newCard = randomCard()

			handlist.append(newCard)

	return originLists


a = generateTest_supply( ([1,2,3,4,5,6,7,8,9,1,1,1], [], [111,121,131,141,151,161,171,181], [], []) )
for i in a:
	for j in i:
		print str(j)+',',
	print ''