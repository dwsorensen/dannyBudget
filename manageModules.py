import os
import pickle
import boto3
import botocore
from screenClass import Screen

s3Bucket = 'moduleinformation'
#Check if we're running in lambda or on local computer
if os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None:
	#Credentials automatically added by aws
	session = boto3.Session()
else:
	session = boto3.Session(aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

s3 = session.resource('s3')

def forceValidResponse(validResponses):
	foundIt = False
	while foundIt == False:
		userInput = input(": ")
		if userInput.lower() in validResponses:
			foundIt = True
			print("")
			return userInput.lower()
		else:
			try:
				userInt = int(userInput)
				if userInt in validResponses:
					foundIt = True
					return userInt
			except:
				pass
		print("Invalid entry.")

def saveModuleList(moduleList):
	global s3Bucket, s3
	dataStream = pickle.dumps(moduleList)
	s3.Object(s3Bucket,"moduleList").put(Body = dataStream)

def loadModuleList():
	global s3Bucket, s3
	try:
		moduleListObject = s3.Object(s3Bucket,"moduleList")
		moduleList = pickle.loads(moduleListObject.get()['Body'].read())
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "NoSuchKey":
			moduleList = []
			saveModuleList(moduleList)
		else:
			raise
	return moduleList

def makeItemizedList(list):
	dictionary = {}
	promptText = ""
	for i, x in enumerate(list):
		dictionary[(i+1)] = x
		promptText = promptText + str(i + 1) + ": " + x +"\n"
	return [dictionary, promptText]

def getUserSelection(list):
	[dictionary, promptText] = makeItemizedList(list)
	print(promptText)
	userSelection = forceValidResponse(dictionary.keys())
	return dictionary[userSelection]

def saveScreen(screen):
	global s3, s3Bucket
	fileName = screen.module + "/" + screen.ID
	dataStream = pickle.dumps(screen)
	s3.Object(s3Bucket, fileName).put(Body = dataStream)

def findModuleScreens(module):
	global s3, s3Bucket
	bucket = s3.Bucket(s3Bucket)
	curatedScreens = []
	for obj in bucket.objects.all():
		if obj.key.startswith(module + "/"):
			curatedScreens.append(pickle.loads(obj.get()['Body'].read()).ID)
	return curatedScreens


	

def moduleManagementScreen():
	global s3, s3Bucket
	quit = False
	while quit == False:
		print("")
		print ("Modules:")
		for i in loadModuleList():
			print ("-" + i)
		print("\n1: Add Module\n2: Edit Module\n3: Remove Module\n4: Quit")
		userResponse = forceValidResponse([1,2,3,4])
		if userResponse == 1:
			print("Input module name")
			moduleName = input(": ")
			moduleList = loadModuleList()
			moduleList.append(moduleName)
			saveModuleList(moduleList)
			rootScreen = Screen(moduleName, "root")
			saveScreen(rootScreen)
			print("Module '" + moduleName + "' created and root screen added.")
		elif userResponse == 2:
			moduleList = loadModuleList()
			if len(moduleList) == 0:
				print("No modules.")
			else:
				print("Select the module to edit.")
				chosenModule = getUserSelection(moduleList)
				print("You have selected '" + chosenModule + "'.")
				screenManagementScreen(chosenModule)
		elif userResponse == 3:
			moduleList = loadModuleList()
			#TODO: Delete deleted module screens.
			if len(moduleList) == 0:
				 print("No modules.")
			else:
				print("Select the module to remove.")
				chosenModule = getUserSelection(moduleList)
				moduleList.remove(chosenModule)
				saveModuleList(moduleList)

				bucket = s3.Bucket(s3Bucket)
				for obj in bucket.objects.all():
					if obj.key.startswith(chosenModule + "/"):
						obj.delete()

				print("Module '" + chosenModule + "' removed.")
		elif userResponse == 4:
			quit = True

def screenManagementScreen(module):
	global s3, s3Bucket
	quit = False
	while quit == False:
		print("")
		print("Screens:")
		for i in findModuleScreens(module):
			print("-" + i)
		print("\n1: Add Screen\n2: Configure Screen\n3: Remove Screen\n4: Back to Modules")
		userResponse = forceValidResponse([1,2,3,4])
		if userResponse == 1:
			print("Input screen name.")
			screenName = input(": ")
			screen = Screen(module, screenName)
			saveScreen(screen)
			print("Screen '" + screenName + " created.")
		elif userResponse == 2:
			screenList = findModuleScreens(module)
			if len(screenList) == 0:
				print("No screens.")
			else:
				print("Select the screen to configure.")
				chosenScreen = getUserSelection(screenList)
				key = module + "/" + chosenScreen
				screenObject = s3.Object(s3Bucket,key)
				screen = pickle.loads(screenObject.get()['Body'].read())
				screen = configureScreen(screen)
				saveScreen(screen)
		elif userResponse == 3:
			screenList = findModuleScreens(module)
			if len(screenList) == 0:
				print("No screens.")
			else:
				print("Select the screen to remove.")
				chosenScreen = getUserSelection(screenList)
				key = module + "/" + chosenScreen
				s3.Object(s3Bucket, key).delete()
				print("Screen removed.")


		elif userResponse == 4:
			quit = True

def configureScreen(screen):
	print("")
	print("Configuring '" + screen.ID + "'.")
	print("Properties:")
	for i in screen.properties:
		print("-" + i + ": " + screen.properties[i])
	print("")
	print("Select a property:")
	screenProperty = getUserSelection(screen.properties)
	screen = configureProperty(screen, screenProperty)
	return screen

def configureProperty(screen, screenProperty):
	titleString = screenProperty + ": "
	if screenProperty in screen.propertiesHelp:
		titleString = titleString + screen.propertiesHelp[screenProperty]
	print("Current value - " + str(screen.properties[screenProperty]))
	print("Please note that you could very much destroy the code if you mess it up.")
	print("Input new value:")
	newValue = input(": ")
	screen.properties[screenProperty] = newValue
	return screen


if __name__ == "__main__":
	moduleManagementScreen()