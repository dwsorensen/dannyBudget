import os
import pickle
from budgetClass import Budget
import promptFunctions
import boto3
import botocore

s3Bucket = 'userdatapickles'
#Check if we're running in lambda or on local computer
if os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None:
	#Credentials automatically added by aws
	session = boto3.Session()
else:
	session = boto3.Session(aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

s3 = session.resource('s3')

def loadBudget(userID):
	global s3, s3Bucket

	try:
		budgetObject = s3.Object(s3Bucket,userID)
		budget = pickle.loads(budgetObject.get()['Body'].read())
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "NoSuchKey":
			budget = Budget(userID)
			saveBudget(budget)
		else:
			raise

	return budget

def listBudgets():
	global s3
	bucket = s3.Bucket(s3Bucket)
	idList = []
	for obj in bucket.objects.all():
		idList.append(obj.key)
	return idList

def checkStatus(budget):
	if not budget.get("approved"):
		budget.set("currentPrompt","approvalMessage")
	messages = budget.get("messages")
	lastMessage = messages[len(messages)-1]
	if lastMessage == "secretpassword":
		budget.set("currentPrompt", "adminHome")

	if budget.get("prompted"):
		try:
			intSelect = int(lastMessage) - 1
			budget.set("currentPrompt",budget.get("promptList")[intSelect])
			budget.set("prompted",False)
		except:
			budget.set("skipPrompt",True)
			budget.set("toPrint","Invalid selection.")

	return budget

def saveBudget(budget):
	global s3, s3Bucket
	pickle_byte_obj = pickle.dumps(budget)
	s3.Object(s3Bucket,budget.get("budgetID")).put(Body = pickle_byte_obj)

if __name__ == '__main__':
	loadBudget("12345")