from getMessageResponse import getResponse

fromNum = input("Number to text from: ")

textData = ""

while textData not in ["stopsimulation", "exit()"]:
	textData = input("Message: ").lower()
	keepGoing = True
	while keepGoing:
		[response, keepGoing] = getResponse(textData, fromNum)
		print("")
		print(response)
		print("")