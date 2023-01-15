import fileManagement

def presentPrompt(budget):
	function = globals()[budget.get("currentPrompt")]
	budget = function(budget)
	return budget

def start(budget):
	if budget.get("approved"):
		budget.set("currentPrompt","home")
		return home(budget)
	else:
		budget.set("currentPrompt","approvalMessage")
		return approvalMessage(budget)

def home(budget):
	budget.set("toPrint", "You are approved. Stay tuned for new features!")
	return budget

def approvalMessage(budget):
	budget.set("toPrint","User not approved... Contact Daniel to get your number added to the list of approved users!")
	return budget

def adminHome(budget):
	budget.set("toPrint","Admin actions: Make a selection: 1 - List Users; 2 - Approve a user; 3 - Remove user approval; 4 - Back to home")
	budget.set("approved", True)
	budget.set("prompted",True)
	budget.set("promptList",["listUsers","userApproval","approvalRemoval", "start"])
	return budget

def listUsers(budget):
	userList = fileManagement.listBudgets()
	outputFile = "Users: "
	for i in userList:
		outputFile = outputFile + i + ","
	outputFile = outputFile[:-1]
	outputFile = outputFile + "."
	budget.set("toPrint",outputFile)
	budget.set("currentPrompt","adminHome")
	budget.set("keepGoing",True)
	return budget


def userApproval(budget):
	budget.set("toPrint","Enter user ID / number to be approved.")
	budget.set("currentPrompt","userApproval1")
	return budget

def userApproval1(budget):
	messages = budget.get("messages")
	lastMessage = messages[len(messages)-1]
	approvedBudget = fileManagement.loadBudget(lastMessage)
	approvedBudget.set("approved",True)
	approvedBudget.set("currentPrompt","start")
	fileManagement.saveBudget(approvedBudget)
	budget.set("toPrint","User approved.")
	budget.set("currentPrompt","adminHome")
	budget.set("keepGoing",True)
	return budget

def approvalRemoval(budget):
	budget.set("toPrint","Enter user ID / number to be removed.")
	budget.set("currentPrompt","approvalRemoval1")
	return budget

def approvalRemoval1(budget):
	messages = budget.get("messages")
	lastMessage = messages[len(messages)-1]
	removedBudget = fileManagement.loadBudget(lastMessage)
	removedBudget.set("approved",False)
	removedBudget.set("currentPrompt","start")
	fileManagement.saveBudget(removedBudget)
	budget.set("toPrint","User removed.")
	budget.set("currentPrompt","adminHome")
	budget.set("keepGoing",True)
	return budget