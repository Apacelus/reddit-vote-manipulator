import os
import zipfile
import tkinter as tk
from tkinter import W
import platform
import urllib.request
import tempfile
from tkinter.messagebox import showerror, showinfo
from sys import exit

import oc_windows
import oc_linux


def terminate_all():
    print("Exiting program")
    oc_windows.abort()
    oc_linux.abort()
    exit()


def restart():
    print("restarting script")
    oc_windows.abort()
    oc_linux.abort()
    print(os.getcwd())
    if platform.system() == "Windows":
        os.system(os.getcwd() + r"\opinion-changer.exe")
    elif platform.system() == "Linux":
        # add linux code
        pass
    terminate_all()


def initialize():
    print("Initializing file")
    # check if config exists
    try:
        with open("config.txt", 'r') as f:
            config_file = f.read()
        print("read config: " + str(config_file))
    except FileNotFoundError:
        setup("config")
        main_window.quit()
        restart()
    if config_file == "":
        setup("config")
        restart()
    else:
        config_file = config_file.split("\n"[-1])
    # Check browser path from config.txt
    print("test_config: " + str(config_file))
    if config_file[0][20:] == "False":
        browser_path = config_file[1][14:config_file[1].find(r'"', 14)]
        match browser_path[browser_path.rfind("\\") + 1:len(browser_path)]:
            case "chrome.exe":
                try:
                    os.path.isfile(browser_path)
                    print("Verified path for chrome")
                except FileNotFoundError:
                    print("Browser not found")
                    terminate_all()  # dont quit, rather prompt for user input
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
                    print("Verified path for Microsoft edge")
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
        restart()
    # calculate amount of available accounts from accounts.txt
    try:
        with open("accounts.txt", 'r') as f:
            accounts_file = f.read()
        print(accounts_file)
        if accounts_file == "":
            setup("accounts")
            restart()
        else:
            accounts_file = accounts_file[127:]
            accounts_file = accounts_file.split("\n"[-1])
            empty_lines = True
            print("here:" + str(accounts_file))
            if accounts_file[0] == "":
                setup("accounts")
                restart()
            else:
                while empty_lines:
                    print("empty_lines: " + str(accounts_file))
                    if accounts_file[len(accounts_file) - 1].find(":") == -1:
                        del accounts_file[len(accounts_file) - 1]
                    else:
                        empty_lines = False
            print("available accounts: " + str(len(accounts_file)))
    except FileNotFoundError:
        setup("accounts")
        restart()
    # check if chromedriver/msedgedriver is present
    if platform.system() == "Windows":
        if oc_windows.initialize() == "Missing":
            print("testasdasdasd")
            setup("driver")
            restart()
    elif platform.system() == "Linux":
        if oc_linux.initialize() == "Missing":
            setup("driver")
            restart()
    else:
        print("Unsupported platform")
    gui(len(accounts_file))


def autodownload_accounts():
    print("Downloading pre-made accounts")
    with open("accounts.txt", 'w') as f:
        request = urllib.request.Request(
            url="https://raw.githubusercontent.com/Fornball/opinion-changer-reddit/main/premade_accounts.txt", headers={
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'})
        raw_accounts_file = urllib.request.urlopen(request).read()
        f.write(raw_accounts_file[2:len(raw_accounts_file) - 1].decode("ascii"))
    print("Download successful")


def setup(mode):
    print("setup")
    setup_window = tk.Toplevel(main_window)
    setup_window.resizable(False, False)
    setup_window.title("Opinion changer setup")
    setup_window.geometry("440x600")
    setup_window.grab_set()
    # UI elements
    close_options_button = tk.Button(setup_window, text="Close", height=1,
                                     width=25)
    accounts_management_label = tk.Label(setup_window, text="Accounts management", font="bold 11")
    manual_accounts_label = tk.Label(setup_window, text='•Press "Edit accounts" to manually add accounts')
    autodownload_label = tk.Label(setup_window,
                                  text='•Press "Auto-download" to download accounts from the github repository.')
    edit_accounts_button = tk.Button(setup_window, text="Edit accounts",
                                     command=lambda: os.startfile("accounts.txt"), height=1, width=25)
    autodownload_accounts_button = tk.Button(setup_window, text="Auto-download",
                                             command=lambda: [autodownload_accounts(), setup_window.quit()], height=1,
                                             width=25)
    match mode:
        case "driver":
            print("driver mode")
            if platform.system() == "Windows":
                print("on windows")
                # this code auto downloads the latest stable x64 version of the msedgedriver
                raw_html = urllib.request.Request(
                    url="https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/", headers={
                        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'})
                parsed_html = str(urllib.request.urlopen(raw_html).read())
                download_link_end = parsed_html.find(r'aria-label="x64 stable channel,') - 2
                download_link_start = parsed_html.find("href", download_link_end - 200) + 6
                # extracting downloaded driver to current directory
                # parsed_html[download_link_start:download_link_end]
                # temp_zip = tempfile.mkstemp(suffix='.zip')
                with open(tempfile.gettempdir() + "msedgedriver.zip", 'wb') as f:
                    temp_zip_as_binary = urllib.request.Request(
                        url=parsed_html[download_link_start:download_link_end], headers={
                            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'})
                    temp_zip_as_binary = urllib.request.urlopen(temp_zip_as_binary).read()
                    f.write(temp_zip_as_binary)
                file = zipfile.ZipFile(tempfile.gettempdir() + "msedgedriver.zip")
                file.extractall(path=os.getcwd())
            elif platform.system() == "Linux":
                # might be broken, left in for future linux update
                pass
                '''
                print("on linux")
                tk.Label(setup_window, text="Driver download", font="bold 11").place(x=0, y=12, anchor=W)
                tk.Label(setup_window, text="1. Get your browser version").place(x=0, y=33, anchor=W)
                tk.Button(text="Check browser version",
                          command=lambda: webbrowser.open(r"https://www.whatsmybrowser.org/"), height=1,
                          width=25).place(
                    x=0, y=58, anchor=W)
                tk.Label(setup_window,
                         text='2. Select your browser version, then download "chromedriver_win32.zip"').place(x=0, y=93,
                                                                                                              anchor=W)
                tk.Button(text="Download driver",
                          command=lambda: webbrowser.open(r"https://chromedriver.chromium.org/downloads/"), height=1,
                          width=25).place(
                    x=0, y=121, anchor=W)
                tk.Label(setup_window,
                         text='3. Extract the file and paste it to this location').place(x=0, y=155, anchor=W)
                tk.Button(text="Open location",
                          command=lambda: print("open location in explorer, should be the same as the python exe"),
                          height=1, width=25).place(x=0, y=183, anchor=W)
                setup_window.mainloop()
                # os.path.abspath(os.getcwd())
                # automate process with chromedriver-py
                '''
            else:
                print("Unsupported os")
                terminate_all()

        case "accounts":
            print("accounts mode")
            main_window.withdraw()
            with open("accounts.txt", 'w') as f:
                f.write(r"# This is the list containing the accounts that will be used for reacting to a post. "
                        + "Add new accounts like this:"
                        + "\nname:password")
            accounts_management_label.place(x=0, y=220, anchor=W)
            manual_accounts_label.place(x=0, y=240, anchor=W)
            autodownload_label.place(x=0, y=260, anchor=W)
            edit_accounts_button.place(x=240, y=290, anchor=W)
            autodownload_accounts_button.place(x=0, y=290, anchor=W)
            close_options_button.configure(command=lambda: terminate_all())
            close_options_button.place(x=250, y=580, anchor=W)
            setup_window.protocol("WM_DELETE_WINDOW", terminate_all)
            setup_window.mainloop()
            print("wtf")
        case "config":
            print("config mode")
            # main_window.withdraw()
            # setup_window.quit()
            # perform check for os here
            if platform.system() == "Windows":
                print("on windows")
                write_config("", "Microsoft Edge", False)
            elif platform.system() == "Linux":
                # might be broken, left in for future linux update
                pass
                '''
                # UI logic
                # Firefox not yet supported
                browser_name = ["Chrome", "Microsoft Edge", "Firefox", "Opera", "Brave", "Chromium", "Custom:"]
                selected_browser = tk.StringVar(setup_window)
                selected_browser.set(browser_name[0])
                # UI elements
                tk.Label(setup_window, text="More Options", font="bold 11").place(x=0, y=320, anchor=W)
                tk.Label(setup_window, text="Browser:").place(x=0, y=350, anchor=W)

                def selection_event(event):
                    if selected_browser.get() == "Custom:":
                        print("Custom path selected")
                        custom_path_textbox.place(x=0, y=376, anchor=W)
                    else:
                        custom_path_textbox.place(x=-1000, y=-1000, anchor=W)
                        print("Custom path unselected")

                tk.OptionMenu(setup_window, selected_browser, *browser_name, command=selection_event).place(x=60, y=350,
                                                                                                            anchor=W)
                custom_path_textbox = tk.Text(setup_window, height=1, width=72, font="none 7")
                tk.Checkbutton(setup_window, text='Ignore browser path', variable=ignore_path).place(x=0, y=400,
                                                                                                     anchor=W)
                write_config(custom_path_textbox.get(), selected_browser.get(), ignore_path)
                setup_window.mainloop()
                '''
            else:
                print("Unsupported os")
                terminate_all()

        case "all":
            print("displaying whole config setup_window")
            setup_window.quit()
            accounts_management_label.place(x=0, y=220, anchor=W)
            manual_accounts_label.place(x=0, y=240, anchor=W)
            autodownload_label.place(x=0, y=260, anchor=W)
            edit_accounts_button.place(x=240, y=290, anchor=W)
            autodownload_accounts_button.place(x=0, y=290, anchor=W)
            close_options_button.configure(command=lambda: setup_window.quit())
            close_options_button.place(x=250, y=580, anchor=W)
            setup_window.mainloop()


def check_fields(available_accounts):
    print("Checking fields")
    if comment_link.get("1.0", 'end-1c') == "":
        showerror("Error", 'Enter a link in the "Comment link" field')
    elif vote_count.get() == "":
        showerror("Error", 'Enter a number in the "opinions" field')
    elif int(vote_count.get()) == 0:
        showerror("Error", 'Enter at least 1 in the "opinions" field')
    elif int(vote_count.get()) > available_accounts:
        showerror("Error", 'Cant use more accounts than available. Please lower the amount of "opnions"')
    else:
        try:
            start_reddit_bots(comment_link.get("1.0", 'end-1c')[:len(comment_link.get("1.0", 'end-1c')) - 2],
                                  int(vote_count.get()), vote_decider.get())
            showinfo("Success", "Opinions changed successfully!")
        except ValueError:
            showerror("Error", 'Enter a number in the "opinions" field')


def gui(available_accounts):
    print("Starting main gui")
    # main_window.resizable(False, False)
    main_window.title("Opinion changer")
    main_window.geometry("440x130")
    tk.Label(main_window, text="Enter comment link:").place(x=0, y=15, anchor=W)
    comment_link.place(x=122, y=15, anchor=W)
    tk.Label(main_window, text="Enter amount of opinions(votes):").place(x=0, y=40, anchor=W)
    tk.Label(main_window, text="available: " + str(available_accounts)).place(x=260, y=40, anchor=W)
    vote_count.place(x=200, y=40, anchor=W)
    vote_count.configure(to=available_accounts)
    tk.Button(text="Change Opinions", bg="#ff9393",
              command=lambda: check_fields(available_accounts),
              height=1, width=20).place(x=0, y=110, anchor=W)
    tk.Button(text="Stop", command=lambda: oc_windows.abort(), height=1, width=7).place(x=380, y=110, anchor=W)
    tk.Button(text="More Options", command=lambda: setup("all"), height=1, width=18).place(x=195, y=110, anchor=W)
    vote_decider.place(x=0, y=70, anchor=W)
    tk.Label(main_window, text="Upvote Downvote").place(x=0, y=60, anchor=W)
    main_window.protocol("WM_DELETE_WINDOW", terminate_all)
    main_window.mainloop()


def start_reddit_bots(comment_link, vote_count, vote_type):
    if platform.system() == "Windows":
        if vote_type == 0:
            oc_windows.upvote(vote_count, comment_link)
        else:
            oc_windows.downvote(vote_count, comment_link)
    elif platform.system() == "Linux":
        if vote_type == 0:
            oc_linux.upvote(vote_count, comment_link)
        else:
            oc_linux.downvote(vote_count, comment_link)
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


main_window = tk.Tk()
comment_link = tk.Text(main_window, height=1, width=44, font="none 8")
vote_count = tk.Spinbox(main_window, from_=0, width=4)
vote_decider = tk.Scale(main_window, from_=0, to_=1, orient="horizontal")
initialize()
