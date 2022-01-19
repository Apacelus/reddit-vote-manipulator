# this file is specifically made for windows
import os.path

from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

options = EdgeOptions()
options.use_chromium = True  # deprecated?
options.add_argument("-inprivate")
options.add_argument("-headless")
options.add_argument("-disable-gpu")
options.binary_location = ""
browser = ""


def initialize():
    print("Initializing windows specific")
    with open("config.txt", 'r') as f:
        config_file = f.read()
        config_file = config_file.split("\n"[-1])
    options.binary_location = config_file[1][14:config_file[1].find(r'"', 14)]
    print("Checking msedge driver")
    if not os.path.isfile(os.getcwd() + r"\msedgedriver.exe"):
        print("msedge driver missing")
        return "Missing"
    else:
        print("success")
        browser = Edge(executable_path="msedgedriver.exe", options=options)
        # checking if browser works
        try:
            browser.get("https://google.com")
            print("Initialization complete, program is working correctly")
        except WebDriverException:
            print("Please restart the program. If the problem persists, update microsoft edge and your system")
            os.remove(os.getcwd() + "msedgedriver.exe")
            # reading accounts_file
            with open("accounts.txt", 'r') as f:
                accounts_file = f.read()
            accounts_file = accounts_file[127:]
            accounts_file = accounts_file.split("\n"[-1])
            available_accounts = len(accounts_file)
            # if user leaves empty space at the end its counted too, add check later
            print("available accs: " + str(available_accounts))


def upvote(vote_count):
    print("upvote")
    used_accounts_count = 0
    # start loop with vote_count amount
    while used_accounts_count < vote_count:
        print("while in upvote")
        # extract username and password
        username = accounts_file[used_accounts_count][:accounts_file[used_accounts_count].find(r':') - 1]
        password = accounts_file[used_accounts_count][accounts_file[used_accounts_count].find(r':') + 1:]
        # open new incognito and login
        browser.get("https://www.reddit.com/login/")
        browser.find_element(By.ID, "loginUsername").send_keys(username)
        browser.find_element(By.ID, "loginPassword").send_keys(password).send_keys(Keys.RETURN)
        browser.get(comment_link)
        browser.find_element(By.XPATH,
                             r"/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[5]/div/div/div/div/div/div/div/div[2]/div[3]/div[3]/div[1]/button[1]")
        browser.quit()
        used_accounts_count += 1


def downvote(vote_count):
    print("downvote")
    used_accounts_count = 0
    # start loop with vote_count
    while used_accounts_count < vote_count:
        print("while in downvote")


def terminate():
    pass
