from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

#url of the page we want to scrape
url = "https://www.insti.app/feed"

months = {
	'January': '1', 
  	'February' : '2', 
  	'March' : '3', 
  	'April' : '4',
  	'May' : '5', 
  	'June' : '6', 
  	'July' : '7', 
  	'August' : '8', 
  	'September' : '9', 
  	'October' : '10', 
  	'November' : '11', 
  	'December' : '12'
}


def main():
	# get email address of the user's google account
    print("Provide your email address: ")
    attendeeMail = input()		

    # initiating the webdriver. Parameter includes the path of the webdriver.
    options = webdriver.ChromeOptions()

	# path of google chrome on your device
	# change it accordingly when you run the script
    options.binary_location = "/usr/bin/google-chrome"

	# path of chromedriver installed on your device
	# change it accordingly when you run the script
    chrome_driver_binary = "chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, options=options)
    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5)

	# scrapping event details using beautiful soup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    insti_events = list()
    for i in soup.find_all('app-event-card'):
        eventdetail = []
        for j in i.find_all('p'):
            eventdetail.append(j.text)
        insti_events.append(eventdetail)
    with open('events.txt','w') as fp:		# writing the headlines into a text file
    	for i in insti_events:
            fp.write(i[0])
            fp.write(';')
            fp.write(i[1])
            fp.write('\n')
    for i in soup.find_all('mat-card'):
        eventdetail = []
        for j in i.find_all('div'):
            eventdetail.append(j.text)
        for j in i.find_all('span'):
            eventdetail.append(j.text)
        insti_events.append(eventdetail)
    with open('events.txt','w') as fp:
        for i in insti_events:
            fp.write(i[0])
            fp.write(';')
            fp.write(i[1])
            fp.write('\n')

    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming event details...')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        #for event in events:
        #    start = event['start'].get('dateTime', event['start'].get('date'))
        #    print(start, event['summary'])
        # Refer to the Python quickstart on how to setup the environment:
        # https://developers.google.com/calendar/quickstart/python
        # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
        # stored credentials.

		# scrapping event's description using selenium
        desc = list()
        for j in driver.find_elements(By.TAG_NAME,'app-event-card'):
            ev = j.click()
            time.sleep(5)
            soup1 = BeautifulSoup(driver.page_source, "html.parser")
            d = soup1.find('div', attrs={'class':'description markdown'})
            desc.append(d.getText())
        for j in driver.find_elements(By.TAG_NAME,'mat-card'):
            ev = j.click()
            time.sleep(5)
            soup1 = BeautifulSoup(driver.page_source, "html.parser")
            d = soup1.find('div', attrs={'class':'description markdown'})
            desc.append(d.getText())

		# arranging all the information in a systematic format
        final_events = list()
        k = 0
        for i in insti_events:
          # print('i[0]',i[0].split())
          # print('i[1]',i[1].split())
            dateElement = i[1].split()[-2]
            venue = 'IIT Bombay'
            date = dateElement[:len(dateElement)-2]
            month = 'month'
            eventtime = i[1].split()[-4]
            if i[1].split()[-1] in months.keys():
                # print("SAHI H")
                month = months[i[1].split()[-1]]
            else:
                exact_venue = []
                reversed_details = i[1].split().copy()
                reversed_details.reverse()
                date_index = 0
                for word in reversed_details:
                    date_index += 1
                    if word == '|':
                        break
                    else:
                        exact_venue.append(word)
                exact_venue.reverse()
                venue_name = ''
                for word in exact_venue:
                    venue_name += word
                venue = venue_name
                month = months[reversed_details[date_index]]
                eventtime = reversed_details[date_index+3]
                date = reversed_details[date_index+1]
                date = date[:len(date)-2]
            #print("DESC \n", desc[k])
            #print('2023-'+month+'-'+date+'T'+eventtime+':00')
            event = {
                'summary': i[0],
                'location': venue,
                'description': desc[k],
                'start': {
                    'dateTime': '2023-'+month+'-'+date+'T'+eventtime+':00',
                    'timeZone': 'GMT+5:30',
                },
                'end': {
                    'dateTime': '2023-'+month+'-'+date+'T'+eventtime+':00',
                    'timeZone': 'GMT+5:30',
                },
                'recurrence': [
                    'RRULE:FREQ=DAILY;COUNT=1'
                ],
                'attendees': [
                    {'email': attendeeMail},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }       
            final_events.append(event)
            k += 1
		
        print('Adding events to Google Calender...')

        for i in final_events:
            i = service.events().insert(calendarId='primary', body=i).execute()
            print('Event created: %s' % (i.get('htmlLink')))


    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()