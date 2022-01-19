import os
from os import startfile
import webbrowser
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import tkinter as tk
from tkinter import W

# import subprocess
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

option = webdriver.ChromeOptions()
option.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser-Beta\Application\brave.exe"
option.add_argument("--incognito --headless")
accounts_file = ""
available_accounts = 0
comment_link = ""


def launch():
    print("launch")
    # check if config exists
    try:
        with open("config.txt", 'r') as f:
            config_file = f.read()
            config_file = config_file.split("\n"[-1])
    except FileNotFoundError:
        setup("config")
    # Check browser path from config.txt
    if config_file[0][20:] == "False":
        browser_path = config_file[1][14:config_file[1].find(r'"', 14)]
        match browser_path[browser_path.rfind("\\") + 1:len(browser_path)]:
            case "chrome.exe":
                try:
                    os.path.isfile(browser_path)
                    print("Verified path for chrome")
                except FileNotFoundError:
                    print("error")
            case "brave.exe":
                try:
                    os.path.isfile(browser_path)
                    print("Verified path for brave")
                except FileNotFoundError:
                    print("error")
            case _:
                print(
                    'Browser path invalid or using an unsupported browser.'
                    + 'Check "Ignore browser path" to force continue.')
    elif not config_file[0][20:] == "True":
        setup("config")
    # calculate amount of available accounts from accounts.txt
    try:
        with open("accounts.txt", 'r') as f:
            accounts_file = f.read()
            if accounts_file == "":
                setup("accounts")
            else:
                accounts_file = accounts_file[127:]
                accounts_file = accounts_file.split("\n"[-1])
                available_accounts = len(accounts_file)
                # if user leaves empty space at the end its counted too, add check later
                print("available accs: " + str(available_accounts))
    except FileNotFoundError:
        setup("accounts")
    # check if chromedriver is present
    browser_version = browser.capabilities['browserVersion']
    driver_version = browser.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    if browser_version[0:2] != driver_version[0:2]:
        print("Chromedriver version missmatch, launching setup")
        setup("driver")
    else:
        gui()


def setup(mode):
    print("setup")
    window = tk.Tk()
    window.resizable(False, False)
    window.title("Opinion changer setup")
    window.geometry("440x600")
    tk.Button(text="Relaunch program", command=lambda: launch(), height=1, width=25).place(x=250, y=500, anchor=W)
    match mode:
        case "driver":
            tk.Label(window, text="Driver download", font="bold 11").place(x=0, y=12, anchor=W)
            tk.Label(window, text="1. Get your browser version").place(x=0, y=33, anchor=W)
            tk.Button(text="Check browser version",
                      command=lambda: webbrowser.open(r"https://www.whatsmybrowser.org/"), height=1,
                      width=25).place(
                x=0, y=58, anchor=W)
            tk.Label(window,
                     text='2. Select your browser version, then download "chromedriver_win32.zip"').place(x=0, y=93,
                                                                                                          anchor=W)
            tk.Button(text="Download driver",
                      command=lambda: webbrowser.open(r"https://chromedriver.chromium.org/downloads/"), height=1,
                      width=25).place(
                x=0, y=121, anchor=W)
            tk.Label(window,
                     text='3. Extract the file and paste it to this location').place(x=0, y=155, anchor=W)
            tk.Button(text="Open location",
                      command=lambda: print("open location in explorer, should be the same as the python exe"),
                      height=1, width=25).place(x=0, y=183, anchor=W)
            # os.path.abspath(os.getcwd())
            # add linux option
            # automate process with chromedriver-py
        case "accounts":
            with open("accounts.txt", 'w') as f:
                f.write(r"# This is the list containing the accounts that will be used for reacting to a post. "
                        + "Add new accounts like this:"
                        + "\nname:password")
            tk.Label(window, text="Accounts management", font="bold 11").place(x=0, y=220, anchor=W)
            tk.Label(window, text='•Press "Edit accounts" to manually add accounts').place(x=0, y=240, anchor=W)
            tk.Label(window, text='•Press "Auto-download" to download accounts from the github repository.') \
                .place(x=0, y=260, anchor=W)
            tk.Button(text="Edit accounts", command=lambda: startfile("accounts.txt"), height=1, width=25).place(
                x=240, y=290, anchor=W)
            tk.Button(text="Auto-download", command=lambda: startfile("accounts.txt"), height=1, width=25).place(
                x=0, y=290, anchor=W)
        case "config":
            print("config.txt not found or corrupted, launching setup")
            ignore_path = False
            # Window logic
            # MSEdge and Firefox not yet supported
            browser_name = ["Chrome", "Microsoft Edge", "Firefox", "Opera", "Brave", "Chromium", "Custom:"]
            selected_browser = tk.StringVar(window)
            selected_browser.set(browser_name[0])
            # UI elements
            tk.Label(window, text="More Options", font="bold 11").place(x=0, y=320, anchor=W)
            tk.Label(window, text="Browser:").place(x=0, y=350, anchor=W)

            def selection_event(event):
                if selected_browser.get() == "Custom:":
                    print("Custom path selected")
                    custom_path_textbox.place(x=0, y=376, anchor=W)
                else:
                    custom_path_textbox.place(x=-1000, y=-1000, anchor=W)
                    print("Custom path unselected")

            tk.OptionMenu(window, selected_browser, *browser_name, command=selection_event).place(x=60, y=350, anchor=W)
            custom_path_textbox = tk.Text(window, height=1, width=72, font="none 7")
            tk.Checkbutton(window, text='Ignore browser path', variable=ignore_path).place(x=0, y=400, anchor=W)
            write_config(custom_path_textbox.get(), selected_browser.get(), ignore_path)
        case "all":
            print("displaying whole config window")
    window.mainloop()


def gui():
    print("gui")
    comment_link = ""
    # prompt for link and store in comment_link
    # store amount of votes in vote_count
    # two buttons/slider for downvote/upvote, up = true, down = false
    # start button
    # if vote=True in separate thread upvote(vote_count)
    # or vote=False in separate thread downvote(vote_count)


def write_config(browser_path, browser_name, ignore_path):
    print("writing config")
    match browser_name:
        case "Chrome":
            browser_path = ""
        case "Microsoft Edge":
            browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        case "Firefox":

        case "Opera":

        case "Brave":
            browser_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        case "Chromium":

        case "Custom:":

    if not ignore_path:
        with open("config.txt", 'w') as f:
            f.write("ignore_browser_path=False\n" + browser_path)
    else:
        with open("config.txt", 'w') as f:
            f.write("ignore_browser_path=True\n" + browser_path)


def upvote(vote_count):
    print("upvote")
    used_accounts_count = 0
    # start loop with vote_count amount
    while (used_accounts_count < vote_count):
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
    while (used_accounts_count < vote_count):
        print("while in downvote")


setup("config")
try:
    browser = webdriver.Chrome(options=option)
except WebDriverException:
    print("Chromedriver not found, launching setup")
    setup("driver")
browser = webdriver.Chrome(options=option)
launch()
