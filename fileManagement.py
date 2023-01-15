import os
import pickle
from budgetClass import Budget
import promptFunctions

filePath = "./userFiles"

def loadBudget(userID):
	global filePath
	if not os.path.exists(filePath):
		os.mkdir(filePath)

	currentFiles = os.listdir('./userFiles')
	fileName = userID + ".p"

	if fileName in currentFiles:
		file = open(filePath + '/' + fileName, 'rb')
		budget = pickle.load(file)
		file.close()
	else:
		budget = Budget(userID)
		budget.set("currentPrompt", "start")
		saveBudget(budget)
	return budget

def checkStatus(budget):
	if not budget.get("approved"):
		budget.set("currentPrompt","approvalMessage")
	messages = budget.get("messages")
	lastMessage = messages[len(messages)-1]
	print("lastMessage - " + lastMessage)
	if lastMessage == "secretpassword":
		print("Password - entered")
		budget.set("currentPrompt", "adminHome")

	if budget.get("prompted"):
		print("You've been prompted boyo")
		try:
			intSelect = int(lastMessage) - 1
			print("promptLIst  - " + str(budget.get("promptList")))
			print("budget.get(promptlist)[intSelect]" + str(budget.get("promptList")[intSelect]))
			budget.set("currentPrompt",budget.get("promptList")[intSelect])
			budget.set("prompted",False)
		except:
			budget.set("skipPrompt",True)
			budget.set("toPrint","Invalid selection.")

	return budget

def saveBudget(budget):
	global filePath
	fileName = budget.get("budgetID") + ".p"
	file = open(filePath + '/' + fileName, "wb")
	pickle.dump(budget, file)
	file.close()

if __name__ == '__main__':
	loadFile("12345")