#!/usr/bin/env python
import re
from selenium import webdriver
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup 

driver = webdriver.Firefox() # used selenium package as it works better with pages that require login or pages protected with captcha
pages = [] # store every page content in a list
for i in range(1, 46): # each page has 10 exterminated rats, total no. of rats is 450 so 45 pages, also confirmed manualy
    print(i)
    driver.get(f'https://www.idf.il/%D7%A0%D7%95%D7%A4%D7%9C%D7%99%D7%9D/%D7%97%D7%9C%D7%9C%D7%99-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94/?page={i}&firstName=&lastName=&unit=&city=&startDate=&endDate=')
    pages.append(driver.page_source)

# now we use the beautifulsoup to extract the elements we need exactly, these can be determined using inspector in firefox, see attached screenshot
casualties = []
for page in pages:
    soup = BeautifulSoup(page)
    dates = soup.select('div.list-casualties p') # all the dates are in p tags below the div tag with a list-casualties css class
    for date in dates:
        casualties.append(re.search(r'.*? \((.*)\)', date.text).group(1)) # the regex extracts the text between parenthesis

# we convert the Hebrew months to English ones
casualties = [c.replace('בדצמבר', 'Dec').replace('בנובמבר', 'Nov').replace('באוקטובר', 'Oct') for c in casualties]

# we convert the results to a dataframe
casualties_df = pd.DataFrame({d: len([c for c in casualties if c == d]) for d in set(casualties)}, index=[0]).T.reset_index()
casualties_df.sort_values('Date', inplace=True)

# plot the results
plt.plot(casualties_df.iloc[1:].Date, casualties_df.iloc[1:].Count.cumsum())
plt.show()
