#library used to query a websit
#import the beautiful soup functions to parse the data returned from the website
import http.client
import json
#Trying stuff using the API

def getResponse(doc_ID, api_key):
    conn = http.client.HTTPConnection("api.data.gov")

    url = "/regulations/v3/document.json?api_key=apiKey&documentId=docID"

    url = url.replace("apiKey", api_key)
    url = url.replace("docID", doc_ID)

    conn.request("GET", url)

    res = conn.getresponse()
    data = res.read()
    parsed_json = json.loads(data.decode("utf-8"))

    return parsed_json

def printIndividual(dict,label):
    str = dict[label]['label'] + ': ' + dict[label]['value']

    print(str)
    return

def downloadAttachment(dict):
    url = dict['attachments'][0]['fileFormats'][0]

    print(url)

    return

doc_ID = "USTR-2018-0005-3207"
CONST_API_KEY = "RcXuvUWp7vXEOnU3JpOh1pwEWGXd4sCmccwQC9gm"
dict = getResponse(doc_ID, CONST_API_KEY)

printIndividual(dict,'submitterName')
printIndividual(dict,'comment')

if dict['attachmentCount']['value'] != 0:
    downloadAttachment(dict)
