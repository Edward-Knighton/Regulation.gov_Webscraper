import http.client
import json
import urllib.request
from tqdm import tqdm
import glob,os
#stuff for pdf to txt file
from pdfHelp import myPdfConvert as pdf



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

def downloadAttachment(dict, fh):
    print(file=fh)
    if dict['attachments'][0]['postingRestriction'] == 'No_restrictions':
        url = dict['attachments'][0]['fileFormats'][0]
        print("Attachment Title: ", dict['attachments'][0]['title'], file=fh)
        print(file=fh)
        apiKEY = "&api_key=RcXuvUWp7vXEOnU3JpOh1pwEWGXd4sCmccwQC9gm"
        url = url + apiKEY
        fileLocation = dict['attachments'][0]['title'] + '.pdf'
        urllib.request.urlretrieve(url, fileLocation)
        return fileLocation
    else:
        print('Attachment Reason Restricted: ', dict['attachments'][0]['reasonRestricted'], file=fh)
        return 'Restricted'

def printLabels(dict,label, fh):
    str = label + ': ' + dict[label]
    print(str, file=fh)
    return

def individual(submit,CONST_API_KEY, count, fh):
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
        fileName = downloadAttachment(singular, fh)
        #print('fileName: ', fileName)
        for file in glob.glob(fileName):
            with open(file) as fp:
                if fileName != 'Restricted':
                    fileText = pdf.download(fileName)
                    if fileText == fileName:
                        print('PDF Could not be opened Properly', file=fh)
                    else:
                        print(fileText, file=fh)
                    if os.path.isfile(fileName):
                        os.remove(fileName)
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

    max = int(max)
    max = max + pageOffset
    maxstr = str(max)
    fileName = "Submits_From_" + pageOffsetstr + "_to_" + maxstr + "_from_DOCID_" + doc_ID + ".txt"

    fh = open(fileName,"w")
    count = pageOffset
    pbar = tqdm(total=max-pageOffset)
    dict = getAll(doc_ID, CONST_API_KEY, pageOffsetstr)
    docs = dict['documents']
    for submit in docs:
        if count < max:
            individual(submit, CONST_API_KEY, count, fh)
            pbar.update(1)
            count = count + 1
        else:
            break
    #pageOffset = currentPage * 1000
    #pageOffsetstr = str(pageOffset)
    dict = getAll(doc_ID, CONST_API_KEY, pageOffsetstr)
    pbar.close()
    print()
    print("Submits can be found in: ", fileName)
    print("Exiting now")
    fh.close()
    return


if __name__ == "__main__":
    main()
