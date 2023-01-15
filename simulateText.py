from getMessageResponse import getResponse

fromNum = input("Number to text from: ")

textData = ""

while textData != "stopsimulation":
	textData = input("Message: ").lower()
	response = getResponse(textData)
	print(response)