import os
import zipfile
from os import startfile
import webbrowser
import tkinter as tk
from tkinter import W
import platform
import urllib.request
import tempfile
import oc_windows
import oc_linux


def terminate_all():
    print("Exiting program")
    oc_windows.terminate()
    oc_linux.terminate()
    exit()


def initialize():
    print("Initializing main file")
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
                    print("Browser not found")
                    terminate_all()
            case "brave.exe":
                try:
                    os.path.isfile(browser_path)
                    print("Verified path for brave")
                except FileNotFoundError:
                    print("Browser not found")
                    terminate_all()
            case "msedge.exe":
                try:
                    os.path.isfile(browser_path)
                    print("Verified path for msedge")
                except FileNotFoundError:
                    print("Browser not found")
                    terminate_all()
            case _:
                print(browser_path)
                print(
                    'Browser path invalid or using an unsupported browser.'
                    + 'Check "Ignore browser path" under options to force continue.')
                terminate_all()
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
                print("available accounts: " + str(available_accounts))
    except FileNotFoundError:
        setup("accounts")
    # check if chromedriver/msedgedriver is present
    if platform.system() == "Windows":
        if oc_windows.initialize() == "Missing":
            setup("driver")
    elif platform.system() == "Linux":
        if oc_linux.initialize() == "Missing":
            setup("driver")
    gui()


def setup(mode):
    print("setup")
    window = tk.Tk()
    window.resizable(False, False)
    window.title("Opinion changer setup")
    window.geometry("440x600")
    tk.Button(text="Relaunch program", command=lambda: terminate_all(), height=1, width=25).place(x=250, y=500,
                                                                                                  anchor=W)
    match mode:
        case "driver":
            if platform.system() == "Windows":
                print("on windows")
                # this code auto downloads latest stable x64 version of the msedge driver
                raw_html = urllib.request.Request(
                    url="https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/", headers={
                        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'})
                parsed_html = str(urllib.request.urlopen(raw_html).read())
                download_link_end = parsed_html.find(r'aria-label="x64 stable channel,') - 2
                download_link_start = parsed_html.find("href", download_link_end - 200) + 6
                # extracting downloaded driver to current directory
                # parsed_html[download_link_start:download_link_end]
                temp_zip = tempfile.mkstemp(suffix='.zip')
                with open(tempfile.gettempdir() + "msedgedriver.zip", 'wb') as f:
                    temp_zip_as_binary = urllib.request.Request(
                        url=parsed_html[download_link_start:download_link_end], headers={
                            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'})
                    temp_zip_as_binary = urllib.request.urlopen(temp_zip_as_binary).read()
                    f.write(temp_zip_as_binary)
                file = zipfile.ZipFile(tempfile.gettempdir() + "msedgedriver.zip")
                file.extractall(path=os.getcwd())
            elif platform.system() == "Linux":
                print("on linux")
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
                window.mainloop()
                # os.path.abspath(os.getcwd())
                # automate process with chromedriver-py
            else:
                print("Unsupported os")
                terminate_all()

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
            window.mainloop()
        case "config":
            print("config.txt not found or corrupted, launching setup")
            ignore_path = False
            # perform check for os here
            if platform.system() == "Windows":
                print("on windows")
                write_config("", "Microsoft Edge", False)
            elif platform.system() == "Linux":
                # UI logic
                # Firefox not yet supported
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

                tk.OptionMenu(window, selected_browser, *browser_name, command=selection_event).place(x=60, y=350,
                                                                                                      anchor=W)
                custom_path_textbox = tk.Text(window, height=1, width=72, font="none 7")
                tk.Checkbutton(window, text='Ignore browser path', variable=ignore_path).place(x=0, y=400, anchor=W)
                write_config(custom_path_textbox.get(), selected_browser.get(), ignore_path)
                window.mainloop()
            else:
                print("Unsupported os")
                terminate_all()

        case "all":
            print("displaying whole config window")


def gui():
    print("Starting main gui")
    comment_link = ""
    # prompt for link and store in comment_link
    # store amount of votes in vote_count
    # two buttons/slider for downvote/upvote, up = true, down = false
    # start button
    # if vote=True in separate thread upvote(vote_count)
    # or vote=False in separate thread downvote(vote_count)


def start_reddit_bots(comment_link, vote_count, vote_type):
    if platform.system() == "Windows":
        if vote_type:
            oc_windows.upvote(vote_count)
        else:
            oc_windows.downvote(vote_count)
    elif platform.system() == "Linux":
        if vote_type:
            oc_linux.upvote(vote_count)
        else:
            oc_linux.downvote(vote_count)
    else:
        print("How did u even get this far with an unsupported platform?!")
        terminate_all()


def write_config(browser_path, browser_name, ignore_path):
    print("writing config")
    match browser_name:
        case "Chrome":
            browser_path = ""
        case "Microsoft Edge":
            browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        case "Firefox":
            browser_path = ""
        case "Opera":
            browser_path = ""
        case "Brave":
            browser_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        case "Chromium":
            browser_path = ""
        case "Custom:":
            pass
    if not ignore_path:
        with open("config.txt", 'w') as f:
            f.write("ignore_browser_path=False\n" + 'browser_path="' + browser_path + '"')
    else:
        with open("config.txt", 'w') as f:
            f.write("ignore_browser_path=True\n" + browser_path)


config_file = ""
accounts_file = ""
available_accounts = 0
initialize()
