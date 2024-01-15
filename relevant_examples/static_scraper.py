from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import time

# Scraping static website
# if website uses JavaScript to generate content dynamically, it will not be displayed
# results not viewable - see triahlon_scraper.py instead

# Presteps
url = "https://www.leipziger-triathlon.de/ergebnisse/leipziger-triathlon/?ev=40"
headers = {'User-Agent': 'Mozilla/5.0', "cookie": "CONSENT=YES+cb.20230531-04-p0.en+FX+908"} # add metadata of a fake browser
req = Request(url, headers=headers)
page = urlopen(req).read() # send request to view page
soup = BeautifulSoup(page, 'html.parser') # parse server response with BeautifulSoup

# Find table and parse it
table = soup.find('table', id ='tab-results') # table containing competition results

header = table.thead
# header.find_all('th')[0]
#     <th>Platz</th>
# header.find_all('th')[0].text
#     'Platz'
header_cells = [header_cell.text.strip() for header_cell in header.find_all('th')]
print(header_cells)
# for row in table.tr.next_siblings:
for row in table.tbody.children:
    print(row)
