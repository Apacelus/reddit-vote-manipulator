# this file is specifically made for windows
import os.path

from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

options = EdgeOptions()
options.use_chromium = True  # deprecated?
options.add_argument("-inprivate")
# options.add_argument("-headless")
# options.add_argument("-disable-gpu")
options.binary_location = ""
abort_variable = False


def abort():
    global abort_variable
    abort_variable = True


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


def upvote(vote_count, comment_link):
    print("upvote")
    print(vote_count)
    browser = Edge(executable_path="msedgedriver.exe", options=options)
    # read accounts.txt
    with open("accounts.txt", 'r') as f:
        accounts_file = f.read()
    accounts_file = accounts_file[125:]
    accounts_file = accounts_file.split("\n"[-1])
    empty_lines = True
    print("here:" + str(accounts_file))
    while empty_lines:
        if accounts_file[len(accounts_file) - 1].find(":") == -1:
            del accounts_file[len(accounts_file) - 1]
        else:
            empty_lines = False
    used_accounts_count = 0
    global abort_variable
    abort_variable = False
    browser.get("https://reddit.com")
    # start loop with vote_count amount
    while used_accounts_count <= vote_count:
        if abort_variable:
            print("aborting")
            browser.quit()
            break
        else:
            print("while in upvote")
            # extract username and password
            print("used" + str(used_accounts_count))
            username = accounts_file[used_accounts_count][:accounts_file[used_accounts_count].find(r':')]
            print(username)
            password = accounts_file[used_accounts_count][accounts_file[used_accounts_count].find(r':') + 1:]
            print(password)
            # wait for previous user to logout
            WebDriverWait(browser, 10).until(ec.url_to_be("https://www.reddit.com/"))
            # open new incognito and login
            browser.get("https://www.reddit.com/login/")
            browser.find_element(By.ID, "loginUsername").send_keys(username)
            browser.find_element(By.ID, "loginPassword").send_keys(password)
            # press login
            browser.find_element(By.XPATH, "/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button").click()
            # check if reddit throws login error
            if browser.find_element(By.XPATH, "/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/div"):
                print("Incorrect username or password, skipping")
                used_accounts_count += 1
                continue
            elif browser.find_element(By.XPATH, "enter"):  # add check for timeout here
                pass
                # do timeout
            else:
                # wait for login redirect
                WebDriverWait(browser, 10).until(ec.url_to_be("https://www.reddit.com/"))
                browser.get(comment_link)
                # wait till upvote button loads, then click it
                WebDriverWait(browser, 10).until(ec.presence_of_element_located(
                    (By.XPATH,
                     r"/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[5]/div/div/div/div[1]/div/div/div/div[2]/div[3]/div[3]/div[1]/button[1]"))).click()
                # logout
                browser.find_element(By.XPATH,
                                     "/html/body/div[1]/div/div[2]/div[1]/header/div/div[2]/div[2]/div/div[2]").click()
                browser.find_element(By.XPATH, "/html/body/div[5]/div/a[11]").click()
        used_accounts_count += 1
    browser.quit()


def downvote(vote_count, comment_link):
    print("downvote")
    print(vote_count)
    browser = Edge(executable_path="msedgedriver.exe", options=options)
    # read accounts.txt
    with open("accounts.txt", 'r') as f:
        accounts_file = f.read()
    accounts_file = accounts_file[125:]
    accounts_file = accounts_file.split("\n"[-1])
    empty_lines = True
    print("here:" + str(accounts_file))
    while empty_lines:
        if accounts_file[len(accounts_file) - 1].find(":") == -1:
            del accounts_file[len(accounts_file) - 1]
        else:
            empty_lines = False
    # removing last character from link to prevent comment chains
    print(comment_link)
    comment_link = comment_link[0:len(comment_link) - 1]
    print(comment_link)
    used_accounts_count = 0
    global abort_variable
    abort_variable = False
    browser.get("https://reddit.com")
    # start loop with vote_count amount
    while used_accounts_count < vote_count:
        # checking if should be aborted
        if abort_variable:
            print("aborting")
            browser.quit()
            break
        else:
            print("while in downvote")
            # extract username and password
            username = accounts_file[used_accounts_count][:accounts_file[used_accounts_count].find(r':')]
            print(username)
            password = accounts_file[used_accounts_count][accounts_file[used_accounts_count].find(r':') + 1:]
            print(password)
            # wait for previous user to logout
            WebDriverWait(browser, 10).until(ec.url_to_be("https://www.reddit.com/"))
            # open new incognito and login
            browser.get("https://www.reddit.com/login/")
            browser.find_element(By.ID, "loginUsername").send_keys(username)
            browser.find_element(By.ID, "loginPassword").send_keys(password)
            # press login
            # check if login fails
            if browser.find_element(By.XPATH, "/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/div"):
                print("Incorrect username or password, skipping")
                used_accounts_count += 1
                continue
            elif browser.find_element(By.XPATH, "enter"):  # add check for timeout here
                pass
                # do timeout
            else:
                browser.find_element(By.XPATH, "/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button").click()
                # wait for login redirect
                WebDriverWait(browser, 10).until(ec.url_to_be("https://www.reddit.com/"))
                browser.get(comment_link)
                # wait till downvote button loads, then click it
                WebDriverWait(browser, 10).until(ec.presence_of_element_located(
                    (By.XPATH,
                     "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[5]/div/div/div/div[1]/div/div/div/div[2]/div[3]/div[3]/div[1]/button[2]"))).click()
                # logout
                browser.find_element(By.XPATH,
                                     "/html/body/div[1]/div/div[2]/div[1]/header/div/div[2]/div[2]/div/div[2]").click()
                browser.find_element(By.XPATH, "/html/body/div[5]/div/a[11]").click()
        used_accounts_count += 1
    browser.quit()
