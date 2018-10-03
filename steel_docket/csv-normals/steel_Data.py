import json
import glob,os
#stuff for pdf to txt file
import csv
import codecs
from openpyxl import load_workbook


wb = load_workbook(filename = 'Copy of Exclusion_Request_-_Zapp_Precision_Wire_-_Stainless_Products_-_HTS_7222200043.xlsx')
sheet_ranges = wb['range names']
print (sheet_ranges['F8'])
