import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#url of the page we want to scrape
url = "https://www.insti.app/feed"

# initiating the webdriver. Parameter includes the path of the webdriver.
options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/google-chrome"
chrome_driver_binary = "chromedriver"
driver = webdriver.Chrome(chrome_driver_binary, options=options)
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
ev = soup.find_all('app-event-card')
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
with open('source.html', 'w') as op:
	op.write(driver.page_source)

elem = driver.find_element(By.TAG_NAME,'mat-card').click()
with open('source1.html', 'w') as op:
	op.write(driver.page_source)
time.sleep(5)
s = BeautifulSoup(driver.page_source, "html.parser")
print(s.find('div', attrs={"class":"event-body"}).get_text())
driver.close() # closing the webdriver
