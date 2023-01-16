class Screen:

	def __init__(self, module, screenID):
		self.ID = screenID
		self.module = module

		self.properties = {
		"promptText": "Empty",
		"parentScreen": "Empty"
		}

		self.propertiesHelp = {
		"promptText" : "The text sent to the user. Can be a string or a function.",
		"parentScreen": "The screen that is the parent of this screen in the hierarchy."
		}