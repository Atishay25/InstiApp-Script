# InstiApp-Script

A Python script (``script.py``) that fetches details of various events happening in insti from instiApp and uploads them to Google Calender

## Requirements
- Install [chromedriver](https://chromedriver.chromium.org/downloads)
- Install Google client library
    ```
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
- Install selenium, Beautiful Soup and requests
  ```
  pip install selenium
  ```
  ```
  pip install bs4
  ```
  ```
  pip install requests
  ```
- Change the path of webdriver and google chrome app according to your device in ``script.py``, around line no. 50 and 54

## Run
```
python3 script.py
```
Then provide your email address, when asked