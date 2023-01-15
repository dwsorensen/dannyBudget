defaultValues = {
	"skipPrompt" : False,
	"messages" : [],
	"toPrint" : "uhhh null I mean null error",
	"currentPrompt" : "start",
	"prompted": False,
	"promptList": [],
	"skipPrompt": False,
	"keepSending": False
}
class Budget:
	def __init__(self, budgetID, approved=False, activated =False):
		self.properties = {
			"approved" : approved,
			"activated" : activated,
			"budgetID" : budgetID
		}

	def get(self, label):
		if label not in self.properties:
			global defaultValues
			if label in defaultValues:
				self.properties[label] = defaultValues[label]
			else:
				self.properties[label] = "empty"

		return self.properties[label]

	def set(self, label, value):
		self.properties[label] = value

	def append(self, label, value):
		if label in self.properties:
			self.properties[label].append(value)
		else:
			self.properties[label] = [value]

	def lastMessage(self):
		messages = self.get(messages)
		return messages[len(messages)-1]