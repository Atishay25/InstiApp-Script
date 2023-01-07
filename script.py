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

    # initiating the webdriver. Parameter includes the path of the webdriver.
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"
    chrome_driver_binary = "chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver.get(url)
    # this is just to ensure that the page is loaded
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    insti_events = list()
    for i in soup.find_all('app-event-card'):
      eventdetail = []
      for j in i.find_all('p'):
        eventdetail.append(j.text)
      insti_events.append(eventdetail)
    with open('events.txt','w') as fp:
      for i in insti_events:
        fp.write(i[0])
        fp.write(';')
        fp.write(i[1])
        fp.write('\n')
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
        print('Getting the upcoming 10 events')
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
        desc = list()
        for j in driver.find_elements(By.TAG_NAME,'app-event-card'):
          ev = j.click()
          time.sleep(5)
          soup1 = BeautifulSoup(driver.page_source, "html.parser")
          d = soup1.find('div', attrs={'class':'description markdown'})
          desc.append(d.getText())

        final_events = list()
        k = 0
        for i in insti_events:
          print('i[0]',i[0].split())
          print('i[1]',i[1].split())
          dateElement = i[1].split()[-2]
          date = dateElement[:len(dateElement)-2]
          month = months[i[1].split()[-1]]
          eventtime = i[1].split()[-4]
          print("DESC \n", desc[k])
          print('2022-'+month+'-'+date+'T'+eventtime+':00')
          event = {
              'summary': i[0],
              'location': 'this is location',
              'description': desc[k],
              'start': {
                'dateTime': '2022-'+month+'-'+date+'T'+eventtime+':00',
                'timeZone': 'GMT+5:30',
              },
              'end': {
                'dateTime': '2022-'+month+'-'+date+'T'+eventtime+':00',
                'timeZone': 'GMT+5:30',
              },
              'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
              ],
              'attendees': [
                {'email': 'atishayjain2552@gmail.com'},
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
        for i in final_events:
          i = service.events().insert(calendarId='primary', body=i).execute()
          print('Event created: %s' % (i.get('htmlLink')))


    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()