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
	budget.set("toPrint","You've made it to the admin panel. You've been approved. Make a selection: 1 - Approve a user; 2 - Back to home")
	budget.set("approved", True)
	budget.set("prompted",True)
	budget.set("promptList",["userApproval", "start"])
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
	fileManagement.saveBudget(approvedBudget)
	print("Approved budget " + approvedBudget.get("budgetID"))
	budget.set("toPrint","User approved.")
	budget.set("currentPrompt","start")
	budget.set("Keep sending", True)
	return budget