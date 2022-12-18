from bs4 import BeautifulSoup
import requests
import sys
import re

login_credentials = {               # Login details
    "userName": sys.argv[1],
    "password": sys.argv[2],
    "url": "https://moodle.iitb.ac.in/login/index.php",
    "course": sys.argv[3]
}

def moodle_scrapper(data: dict) -> requests.Session():      # Function for scrapping announcements from Moodle
    announcement_scrapped = []
    login, password, url_domain, course_name = data.values()
    moodle_session = requests.Session()
    session_req = moodle_session.get(url=url_domain + "/login/index.php")
    pattern_auth = '<input type="hidden" name="logintoken" value="\w{32}">'
    token = re.findall(pattern_auth, session_req.text)
    token = re.findall("\w{32}", token[0])[0]
    authData = {'anchor': '', 'logintoken': token, 'username': login, 'password': password, 'rememberusername': 1}
    soup = BeautifulSoup((moodle_session.post(url=url_domain + "/login/index.php", data=authData)).content, 'html5lib')
    r = requests.get('https://www.insti.app/feed')        # getting request from url

    soup1 = BeautifulSoup(r.content, 'html5lib') 
    course_link = ""
    a = soup1.find('div')
    s1 = BeautifulSoup((moodle_session.post('https://moodle.iitb.ac.in/my/',data=authData)).content, 'html5lib')
    print(s1.find_all('section', attrs={'class': 'block_myoverview block  card mb-3'}))
    return a.getText()

annList = moodle_scrapper(data=login_credentials)
with open('announcements.txt', 'w') as fp:
    for i in annList:
        fp.write(i)
        #fp.write('\n')