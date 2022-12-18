from bs4 import BeautifulSoup
import requests
import sys
import re

login_credentials = {               # Login details
    "userName": sys.argv[1],
    "password": sys.argv[2],
    "url": "https://moodle.iitb.ac.in/login/index.php",
    "ta": sys.argv[3]
}

def moodle_scrapper(data: dict) -> requests.Session():      # Function for scrapping announcements from Moodle
    announcement_scrapped = []
    login, password, url_domain, ta_name = data.values()
    moodle_session = requests.Session()
    session_req = moodle_session.get(url=url_domain + "/login/index.php")
    pattern_auth = '<input type="hidden" name="logintoken" value="\w{32}">'
    token = re.findall(pattern_auth, session_req.text)
    token = re.findall("\w{32}", token[0])[0]
    authData = {'anchor': '', 'logintoken': token, 'username': login, 'password': password, 'rememberusername': 1}
    soup = BeautifulSoup((moodle_session.post(url=url_domain + "/login/index.php", data=authData)).content, 'html5lib')
    course_link = ""
    nav = soup.find('nav', attrs={"aria-label":"Site"})
    for button in nav.find_all('a'):
        if "CS 251-2022-1" in button.getText().strip():
            course_link = course_link + button.get('href')
            print(course_link,"aevjdshbxz")
            break
    announcementLink = ""
    for i in (BeautifulSoup((moodle_session.post(course_link, data=authData)).content, 'html5lib')).find_all('a'):
        if "Participants" in i.getText():
            announcementLink += i.get('href')
    showall = (BeautifulSoup((moodle_session.post(announcementLink, data=authData)).content, 'html5lib')).find('a', attrs = {'data-action': 'showcount'}).get('href')
    allpage = BeautifulSoup((moodle_session.post(showall,data=authData)).content, 'html5lib')
    participantTable = allpage.find('table', attrs = {'id':'participants'})
    ta_link = ""
    for name in participantTable.find_all('th', attrs = {'class':'cell c0'}):
        if name.find('a').getText() == ta_name:
            ta_link = name.find('a').get('href')
            break
    ta_page = BeautifulSoup((moodle_session.post(ta_link,data=authData)).content, 'html5lib')
    ta_forumLink = ""
    for post in ta_page.find_all('div', attrs = {'class': 'card-body'}):
        for listLi in post.find_all('li'):
            if listLi.getText() == "Forum posts":
                ta_forumLink = listLi.find('a').get('href')
                break
    ta_forumPosts = BeautifulSoup((moodle_session.post(ta_forumLink,data=authData)).content, 'html5lib')
    forumpages = ta_forumPosts.find('ul', attrs={'class': 'mt-1 pagination'})
    pages = forumpages.find_all('li')
    pagelinks = []
    pagelinks.append(ta_forumLink)
    for eachpage in pages[1:-1]:
        pagelinks.append(eachpage.find('a').get('href'))
    for eachforum in pagelinks:
        Articles = (BeautifulSoup((moodle_session.post(eachforum,data=authData)).content, 'html5lib')).find_all('article', attrs={'class':'forum-post-container mb-2'})
        for eachArticle in Articles:
            head = eachArticle.find('h3')
            postTitle = ""
            if "CS 251-2022-1" in head.getText():
                postTitle = head.getText().strip()
                contentList = postTitle.split('\n')
                if(len(contentList) == 2):
                    postTitle = contentList[-1].strip()
                else:
                    postTitle = contentList[-1].strip('-> ')
            postTime = eachArticle.find('time').getText()
            announcement_scrapped.append(postTime+'; '+postTitle)
    announcement_scrapped.reverse()
    return announcement_scrapped

annList = moodle_scrapper(data=login_credentials)
with open('announcements.txt', 'w') as fp:
    for i in annList:
        fp.write(i)
        fp.write('\n')