import os
from os import startfile
import webbrowser
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import tkinter as tk
from tkinter import W
import subprocess

option = webdriver.ChromeOptions()
option.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser-Beta\Application\brave.exe"
option.add_argument("--incognito --headless")


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
                print("accounts.txt not found or corrupted, launching setup")
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
    # window.configure(bg="#ffffff")
    window.geometry("440x600")
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
            window.mainloop()
            # add linux option
            # automate process with chromedriver-py
        case "accounts":
            with open("accounts.txt", 'w') as f:
                f.write(r"# This is the list containing the accounts that will be used for reacting to a post. "
                        + "Add new accounts like this:"
                        + "\nname:password")
            tk.Label(window, text='- Press "Edit accounts" to manually add accounts').place(x=0, y=137, anchor=W)
            tk.Label(window, text='- Press "Auto-download" to download 20 accounts from my repository').place(x=0,
                                                                                                              y=137,
                                                                                                              anchor=W)
            tk.Button(text="Edit accounts", command=lambda: startfile("accounts.txt"), height=1, width=25).place(
                x=240, y=285, anchor=W)
            tk.Button(text="Auto-download", command=lambda: startfile("accounts.txt"), height=1, width=25).place(
                x=240, y=285, anchor=W)
            window.mainloop()
            # startfile("accounts.txt")
        case "config":
            print("config.txt not found or corrupted, launching setup")
            # open a seperate window(overlaying main window) for config
            # options for
            # browser select(chromium edge greyed out for now)
            # redownloading chromedriver
    tk.Button(text="Relaunch program", command=lambda: launch(), height=1, width=25).place(x=250, y=298, anchor=W)


def gui():
    print("gui")
    # prompt for link and store in comment_link
    # store amount of votes in vote_count
    # two buttons/slider for downvote/upvote, up = true, down = false
    # start button
    # if vote=True in separate thread upvote(vote_count)
    # or vote=False in separate thread downvote(vote_count)


def upvote(vote_count):
    print("upvote")
    # start loop with vote_count amount
    while (used_accounts_count < vote_count):
        print("while in upvote")
        # open new incognito and login
        # navigate to comment_link
        # press upvote
        # close window


def downvote(vote_count):
    print("downvote")
    # start loop with vote_count
    while (used_accounts_count < vote_count):
        print("while in downvote")
        # open new incognito and login
        # navigate to comment_link
        # press downvote
        # close winow


setup("driver")
try:
    browser = webdriver.Chrome(options=option)
except WebDriverException:
    print("Chromedriver not found, launching setup")
    setup("driver")
browser = webdriver.Chrome(options=option)
launch()
