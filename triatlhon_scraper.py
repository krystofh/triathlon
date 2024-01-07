from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
import time
import os
# Scraping triathlon results website using dynamic content
# based on: https://www.youtube.com/watch?v=Xz514u4V_ts
# if website uses JavaScript to generate content dynamically, it will not be displayed using BeautifulSoup only
# 1) Check if content is generated dynamically
#    - open Chrome, inspect webpage
#    - CTRL+SHIFT+P and enter "Disable JavaScript"
#    - see what content is not displayed
# 2) Install Firefox Driver (or driver of other browser)
#    - https://www.tutorialspoint.com/how-to-get-firefox-working-with-selenium-webdriver-on-mac-osx
#    - Visit the link −  https://www.selenium.dev/downloads/ and go to the Browser segment. Click on the Documentation link below Firefox.
#    - download the release you need from https://github.com/mozilla/geckodriver/releases   
#    - unpack and using terminal: sudo mv geckodriver /usr/local/bin

# Create browser driver and BeautifulSoup
url = "https://www.leipziger-triathlon.de/ergebnisse/leipziger-triathlon/?ev=40"
browser_options = FirefoxOptions()
browser_options.headless = True # enable opening browser without GUI
driver = Firefox(options=browser_options)
driver.get(url) # get the page
time.sleep(2) # sleep to allow the webpage to load!

# View all results on one page
# Right-click on dropdown and "inspect", then: 
# a) right-click on the code and "copy xpath"   OR
# b) use the template below with the name and option value
selector_choice = driver.find_element(By.XPATH, "//select[@name='tab-results_length']/option[@value='-1']")
selector_choice.click()
time.sleep(2)

# Find table and parse it
soup = BeautifulSoup(driver.page_source, 'lxml') # parse server response with BeautifulSoup
table = soup.find('table', id ='tab-results') # table containing competition results
header = table.thead
header_cells = [header_cell.text.strip() for header_cell in header.find_all('th')]
print(header_cells)

# Load data
data = []
for row in table.tbody.children: # now the table has dynamically generated tbody
    row_content = [cell.text.strip() for cell in row.find_all('td')]
    if row_content != []:
        data.append(row_content)

# Create dataframe from parsed data
results_df = pd.DataFrame(data, columns=header_cells)
results_df.set_index("Platz", inplace=True)
driver.quit() # quit the browser

# Export CSV
results_df.to_csv(os.path.join("data", "triathlon_results.csv"))