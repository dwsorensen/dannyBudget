import os
import pickle
from budgetClass import Budget

filePath = "./userFiles"

def loadFile(userID):
	global filePath
	if not os.path.exists(filePath):
		print("Creating file")
		os.mkdir(filePath)

	currentFiles = os.listdir('./userFiles')
	fileName = userID + ".p"

	if fileName in currentFiles:
		print("Found it")
		file = open(filePath + '/' + fileName, 'rb')
		currentBudget = pickle.load(file)
		file.close()
	else:
		currentBudget = Budget(userID)
		saveBudget(currentBudget)
	return currentBudget


def saveBudget(budget):
	global filePath
	fileName = budget.getLabel() + ".p"
	file = open(filePath + '/' + fileName, "wb")
	pickle.dump(fileName, file)
	file.close()

if __name__ == '__main__':
	loadFile("12345")
