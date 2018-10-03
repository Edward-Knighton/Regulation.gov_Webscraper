#PDF CONVERTER RETURNS PDF PASSED IN AS TEXT


#stuff for pdf to txt file
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io


#converts pdf, returns its text content as a string
def download(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    #Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    #Process each page contained in the document.
    try:
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            data =  retstr.getvalue()
    finally:
        return data
    return data
