# this file is specifically made for linux
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def initialize():
    print("Intializing linux")
    print("Checking chrome driver")


'''
browser_version = browser.capabilities['browserVersion']
driver_version = browser.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
if browser_version[0:2] != driver_version[0:2]:
    print("Chromedriver version missmatch, launching setup")
    setup("driver")

    
    try:
        browser = webdriver.Chrome(options=option)
    except WebDriverException:
        print("Chromedriver not found, launching setup")
        setup("driver")
    browser = webdriver.Chrome(options=option)
    '''
'''
option = webdriver.ChromeOptions()
option.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser-Beta\Application\brave.exe"
option.add_argument("--incognito --headless")
'''


def upvote(vote_count):
    pass


def downvote(vote_count):
    pass


def terminate():
    pass
