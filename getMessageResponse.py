from budgetClass import Budget
from fileManagement import *
from promptFunctions import presentPrompt

def getResponse(userMessage, userNumber):

	budget = loadBudget(userNumber)
	budget.set("keepGoing", False)
	budget.append("messages", userMessage)
	budget = checkStatus(budget)

	if not budget.get("skipPrompt"):
		budget = presentPrompt(budget)
	else:
		budget.set("skipPrompt", False)

	response = budget.get("toPrint")
	keepGoing = budget.get("keepGoing")
	saveBudget(budget)
	return [response, keepGoing]