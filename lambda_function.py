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
    
    responseMessage = ""
    try:
        responseMessage = getResponse(messageText, fromText)
    except:
        responseMessage = "Internal error occured. My sincerest apologies."
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=responseMessage,from_='+' + os.environ['twilioNumber'],to='+' + fromText)