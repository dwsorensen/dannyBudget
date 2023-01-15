from budgetClass import Budget
from fileManagement import *
from promptFunctions import presentPrompt

def getResponse(userMessage, userNumber):

	budget = loadBudget(userNumber)
	print("Prompted - " + str(budget.get("prompted")))
	budget.append("messages", userMessage)
	budget = checkStatus(budget)
	print("Current prompt - " + budget.get("currentPrompt"))

	if not budget.get("skipPrompt"):
		budget = presentPrompt(budget)
		print("Prompted - " + str(budget.get("prompted")))
	else:
		print("Prompted - " + str(budget.get("prompted")))
		budget.set("skipPrompt", False)

	print("Prompted - " + str(budget.get("prompted")))
	response = budget.get("toPrint")
	saveBudget(budget)
	return response