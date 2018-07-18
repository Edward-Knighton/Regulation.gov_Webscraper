import http.client
import json
import urllib.request

def getAll(doc_ID,api_key,page):
    conn = http.client.HTTPConnection("api.data.gov")

    url = 'https://api.data.gov:443/regulations/v3/documents.json?api_key=apiKey&countsOnly=0&encoded=1&dktid=docID&po=PAGE'
    url = url.replace("apiKey", api_key)
    url = url.replace("docID", doc_ID)
    url = url.replace("PAGE",page)
    conn.request("GET", url)

    res = conn.getresponse()
    data = res.read()
    parsed_json = json.loads(data.decode("utf-8"))

    return parsed_json

def getOne(doc_ID, api_key):
    conn = http.client.HTTPConnection("api.data.gov")

    url = "/regulations/v3/document.json?api_key=apiKey&documentId=docID&"

    url = url.replace("apiKey", api_key)
    url = url.replace("docID", doc_ID)

    conn.request("GET", url)

    res = conn.getresponse()
    data = res.read()
    parsed_json = json.loads(data.decode("utf-8"))

    return parsed_json

def downloadAttachment(dict):
    url = dict['attachments'][0]['fileFormats'][0]
    print("Attachment Title: ", dict['attachments'][0]['title'])
    apiKEY = "&api_key=RcXuvUWp7vXEOnU3JpOh1pwEWGXd4sCmccwQC9gm"
    url = url + apiKEY
    fileLocation = 'C:/Users/EJ Knighton/Dropbox/Stuff for EJ/china docket/pdfs/' + dict['attachments'][0]['title'] + '.pdf'
    urllib.request.urlretrieve(url, fileLocation)
    return

def printLabels(dict,label):
    str = label + ': ' + dict[label]
    print(str)
    return

def individual(submit,CONST_API_KEY, count):
    print("count: ", count)
    if 'submitterName' not in submit:
        return
    printLabels(submit,'submitterName')
    printLabels(submit,'documentId')
    printLabels(submit,'commentText')

    if submit['attachmentCount'] != 0:
        singular = getOne(submit['documentId'],CONST_API_KEY)
        downloadAttachment(singular)

    print()
    print()
    return


#only prints 1 page of results currently
#need to set it up so that it does all of them

doc_ID = "USTR-2018-0005"
CONST_API_KEY = "RcXuvUWp7vXEOnU3JpOh1pwEWGXd4sCmccwQC9gm"
dict = getAll(doc_ID, CONST_API_KEY, '0')
totalNumRecords = dict['totalNumRecords']
totalPages = (totalNumRecords / 25) + 1
currentPage = 0
count = 0
while currentPage < totalPages-1:
    docs = dict['documents']
    for submit in docs:
        individual(submit, CONST_API_KEY, count)
        count = count + 1
    currentPage = currentPage + 1
    pageOffset = currentPage * 25
    pageOffsetstr = str(pageOffset)
    dict = getAll(doc_ID, CONST_API_KEY, pageOffsetstr)