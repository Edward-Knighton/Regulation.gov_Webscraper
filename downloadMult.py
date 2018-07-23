import http.client
import json
import urllib.request
from tqdm import tqdm

def getAll(doc_ID,api_key,page):
    conn = http.client.HTTPConnection("api.data.gov")

    url = 'https://api.data.gov:443/regulations/v3/documents.json?api_key=apiKey&countsOnly=0&encoded=1&dktid=docID&po=PAGE&rpp=1000'
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

def downloadAttachment(dict, fh, folderName):
    count = 0
    for attachment in dict['attachments']:
        print()
        if dict['attachments'][count]['postingRestriction'] == 'No_restrictions':
            url = dict['attachments'][count]['fileFormats'][0]
            print("Attachment Title ",count+1,": ", dict['attachments'][count]['title'], file=fh)
            apiKEY = "&api_key=RcXuvUWp7vXEOnU3JpOh1pwEWGXd4sCmccwQC9gm"
            url = url + apiKEY
            fileLocation = folderName +'/' + dict['attachments'][0]['title'] + '.pdf'
            urllib.request.urlretrieve(url, fileLocation)
        else:
            print('Attachment Reason Restricted: ', dict['attachments'][count]['reasonRestricted'], file=fh)
        count = count + 1
    return

def printLabels(dict,label, fh):
    str = label + ': ' + dict[label]
    print(str, file=fh)
    return

def individual(submit,CONST_API_KEY, count, fh, folderName):
    print("Submit number: ", count, file=fh)
    if 'submitterName' not in submit:
        return
    printLabels(submit,'submitterName', fh)
    printLabels(submit,'documentId', fh)
    if 'organization' in submit:
        print('Organization: ', submit['organization'], file=fh)
    printLabels(submit,'commentText', fh)
    if submit['attachmentCount'] != 0:
        singular = getOne(submit['documentId'],CONST_API_KEY)
        downloadAttachment(singular, fh, folderName)

    print(file=fh)
    print(file=fh)
    return


#only prints 1 page of results currently
#need to set it up so that it does all of them
def main():
    print("This is a tool to download comments from the regulations.gov website")
    doc_ID = input("What is the Docket ID of the regulation you are trying to download comments from?  :  ")
    #doc_ID = "USTR-2018-0005"
    CONST_API_KEY = "RcXuvUWp7vXEOnU3JpOh1pwEWGXd4sCmccwQC9gm"

    dict = getAll(doc_ID, CONST_API_KEY, '0')
    totalNumRecords = dict['totalNumRecords']
    totalPages = (totalNumRecords / 1000) + 1

    print("Due to Gov API, this program can only download 1000 submits per hour")
    print("This doc_ID has a total of ",totalNumRecords,"submits")
    print("What submit would you like to start on?")
    pageOffsetstr = input("(It would be 0 if starting from the first submit)  :  ")
    pageOffset = int(pageOffsetstr)

    max = input("How many submits would you like to download?  :  ")
    print("What is the name of the folder that you would like the attachments saved to?")
    folderName = input("(Folder must be in the same as the python script)  :  ")

    max = int(max)
    max = max + pageOffset
    maxstr = str(max)
    fileName = "Submits_From_" + pageOffsetstr + "_to_" + maxstr + "_from_DOCID_" + doc_ID + ".txt"

    fh = open(fileName,"w")
    count = pageOffset
    pbar = tqdm(total=max-pageOffset)

    docs = dict['documents']
    for submit in docs:
        if count < max:
            individual(submit, CONST_API_KEY, count, fh, folderName)
            pbar.update(1)
            count = count + 1
        else:
            break
    #pageOffset = currentPage * 1000
    #pageOffsetstr = str(pageOffset)
    dict = getAll(doc_ID, CONST_API_KEY, pageOffsetstr)
    pbar.close()
    print("Submits can be found in: ", fileName)
    print("Exiting now")
    fh.close()
    return


if __name__ == "__main__":
    main()