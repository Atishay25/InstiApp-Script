#### This program scrapes naukri.com's page and gives our result as a
#### list of all the job_profiles which are currently present there.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#url of the page we want to scrape
url = "https://www.insti.app/feed"

# initiating the webdriver. Parameter includes the path of the webdriver.
options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/google-chrome"
chrome_driver_binary = "chromedriver"
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
driver.get(url)
# this is just to ensure that the page is loaded
time.sleep(5)

html = driver.page_source

# this renders the JS code and stores all
# of the information in static HTML code.

# Now, we could simply apply bs4 to html variable
soup = BeautifulSoup(html, "html.parser")
"""all_divs = soup.find('div', {'id' : 'nameSearch'})
job_profiles = all_divs.find_all('a')

# printing top ten job profiles
count = 0
for job_profile in job_profiles :
	print(job_profile.text)
	count = count + 1
	if(count == 10) :
		break"""
events = list()
for i in soup.find_all('app-event-card'):
	event =[]
	for j in i.find_all('p'):
		event.append(j.text)
	events.append(event)

with open('events.txt', 'w') as fp:
    for i in events:
        fp.write(i[0])
        fp.write(';')
        fp.write(i[1])
        fp.write('\n')

driver.close() # closing the webdriver
