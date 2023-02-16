# Regulation.gov Webscraper

**NOTE:** The version of the regulations.gov api that this project uses has been deccomissioned. There is no plan to update this project use the new api at this time, but information on the updated api can be found [here](https://open.gsa.gov/api/regulationsgov/#api-description).

This scipt allows users to easily download and analyze comments on all legislature submitted to regulations.gov

Users have the option to download all data as a CSV file, a TXT file for text-classification purposes, or simply download all files relating to the legislature for custom use.

## Run information 
 - Clone the repository
 - Run `pip install -r requirements.txt` in the base directory 
 - Run `python Reg_Gov_Scraper.__main__.py` in the base directory and input the Docket ID of the regulation you are trying to download comments from when prompted.

Built using modules from pdf to text converter pdfminer.six which can be found at: https://github.com/pdfminer/pdfminer.six