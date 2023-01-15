import os
from twilio.rest import Client
import base64
from getMessageResponse import getResponse

def lambda_handler(event, context):
    bodyDecoded = str(base64.b64decode(event['body']))
    messageText = bodyDecoded
    messageText = messageText[(messageText.find("Body=") + 5):]
    messageText = messageText[:messageText.find("&")]
    fromText = bodyDecoded
    fromText = fromText[(fromText.find("From=") + 5):]
    fromText = fromText[(fromText.find("B")+1):]
    fromText = fromText[:fromText.find("&")]

    account_sid = os.environ['sid']
    auth_token = os.environ['token']
    keepGoing = True
    while keepGoing:
        try:
            [responseMessage, keepGoing] = getResponse(messageText, fromText)
        except Exception as e:
            responseMessage = "Internal error occured. My sincerest apologies."
            keepGoing = False
            print(repr(e))
        client = Client(account_sid, auth_token)
        message = client.messages.create(body=responseMessage,from_='+' + os.environ['twilioNumber'],to='+' + fromText)