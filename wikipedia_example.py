from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import pandas as pd

# Example scraping static website
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
headers = {'User-Agent': 'Mozilla/5.0'}
req = Request(url, headers=headers)
page = urlopen(req).read()
soup = BeautifulSoup(page, 'html.parser')

# Parse table and header
#   class="wikitable sortable static-row-numbers plainrowheaders srn-white-background jquery-tablesorter"table = soup.find_all('table', {"class":'wikitable sortable static-row-numbers plainrowheaders srn-white-background jquery-tablesorter'})
#   approach not working, use index
table = soup.find_all('table')[2]
header1 = table.find_all('tr', {"class":"static-row-header"})[0].find_all('th')
header_cells_1 = [header_cell.text.strip() for header_cell in header1]
header2 = table.find_all('tr', {"class":"static-row-header"})[1].find_all('th')
header_cells_2 = [header_cell.text.strip() for header_cell in header2]
print(header_cells_1)
print(header_cells_2) # not productive due to multiline header, use manual approach
header = ['Country/Territory', 'UN region', 'IMF forecast', 'IMF year', 'World Bank estimate', 'World Bank year', 'UN estimate', 'UN year']

# Parse data
column_data = table.find_all('tr')
parsed_data = []
for row in column_data[1:]:
    row_data = [data.text.strip() for data in row.find_all('td')]
    if row_data != []:
        parsed_data.append(row_data)
df = pd.DataFrame(parsed_data, columns = header)
df.set_index("Country/Territory", inplace=True)
print(df.head())