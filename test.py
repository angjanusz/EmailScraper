from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import csv
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
store = file.Storage('storage.json') 
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('../client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
user_id =  'me'
label_id_one = 'INBOX'
label_id_two = 'UNREAD'
unread_msgs = GMAIL.users().messages().list(userId='me',labelIds=[label_id_one, label_id_two]).execute()
mssg_list = unread_msgs['messages']

print ("Total unread messages in inbox: ", str(len(mssg_list)))
for mssg in mssg_list:
    temp_dict = { }
    m_id = mssg['id']
    message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()
    payld = message['payload']
    headr = payld['headers']
    try:
        
        # Fetching message body
        mssg_parts = payld['parts'] # fetching the message parts
        part_one  = mssg_parts[0] # fetching first element of the part 
        part_body = part_one['body'] # fetching body of the message
        part_data = part_body['data'] # fetching data from the body
        clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
        #clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
        #clean_two = base64.b64decode (part_data, altchars=None, validate=True) # decoding from Base64 to UTF-8
        clean_one = base64.b64decode(bytes(clean_one, 'UTF-8'))
        clean_two = clean_one.decode("utf-8")
        #soup = BeautifulSoup(clean_one)
        #mssg_body = soup.body()
        # mssg_body is a readible form of message body
        # depending on the end user's requirements, it can be further cleaned 
        # using regex, beautiful soup, or any other method
        #temp_dict = mssg_body
        test_find=clean_two.find('PM')
        print (test_find)

    except :
        pass

    #print (temp_dict)
    print ("eyyy lmao")
