# Simple-Texting
A Python Module for Simple Texting's API 

For more information about the Simple Texting API, please see https://app2.simpletexting.com/account/api

Requirements:
  requests
  xmltodict
  
Usage:

Create the client 
st = simpletexting.Client(token='your_token')

Send Message
#send_message(self, numbers, message) - Numbers being the list of numbers to send the message to
st.send_message(numbers, 'Test1')
