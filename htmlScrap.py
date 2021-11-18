import os.path

import requirementChk
requirementChk.__main__()

from selenium.common.exceptions import WebDriverException as WebDriverException, NoSuchElementException as NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from cryptography.fernet import InvalidToken
from cryptography import __version__ as CryptVer

from time import sleep
from platform import system as sysplatform
from itertools import zip_longest
from os import path as os_path, mkdir as os_mkdir, getcwd as os_getcwd, remove as os_rm, replace as os_move, walk as os_search
from pathlib import Path as os_fullpath
from shutil import copy as os_cp, copytree as os_dircp
from pandas import DataFrame, read_csv, __version__ as PandasVer
from sty import fg
from calendar import monthrange
from datetime import datetime

import authentication
import config

monthsShort = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthsLong = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def shortToLongDayName(original):
    original = original.lower()
    if original == "mon":
        return "Monday"
    elif original == "tue":
        return "Tuesday"
    elif original == "wed":
        return "Wednesday"
    elif original == "thu":
        return "Thursday"
    elif original == "fri":
        return "Friday"
    elif original == "sat":
        return "Saturday"
    elif original == "sun":
        return "Sunday"


def longToShortDayName(original):
    original = original.lower()
    if original == "monday":
        return "Mon"
    elif original == "tuesday":
        return "Tue"
    elif original == "wednesday":
        return "Wed"
    elif original == "thursday":
        return "Thu"
    elif original == "friday":
        return "Fri"
    elif original == "saturday":
        return "Sat"
    elif original == "sunday":
        return "Sun"


def console_log(message: str = None, mode: str = "info"):
    now = str(datetime.now())
    col_now = ""

    for element in range(0, len(now)):
        if now[element].isnumeric():
            col_now += fg.cyan + now[element]
        else:
            col_now += fg.yellow + now[element]

    col_message = ""
    string_type = False

    for element in range(0, len(message)):
        if message[element].isalpha():
            if string_type:
                col_message += fg.li_green + message[element]
            else:
                if mode == "info":
                    col_message += fg.li_blue + message[element]
                elif mode == "error":
                    col_message += fg.li_red + message[element]
                elif mode == "warn":
                    col_message += fg.yellow + message[element]
        elif message[element].isnumeric():
            col_message += fg.li_green + message[element]
        else:
            if message[element] == "'" or message[element] == '"':
                if string_type:
                    string_type = False
                else:
                    string_type = True

                col_message += fg.green + message[element]
            else:
                if string_type:
                    col_message += fg.green + message[element]
                else:
                    col_message += fg.white + message[element]

    if mode == "error":
        col_message = fg.red + "FATAL ERROR" + fg.white + ": " + col_message
    elif mode == "warn":
        col_message = fg.yellow + "WARN" + fg.white + ": " + col_message


    print(fg.white + "[" + col_now + fg.white + "]" + fg.magenta + ": " + col_message)
    del col_now, col_message

    if config.FileLogging:
        if mode == "error":
            CurrentLog.write(f"!!! [{now}] {message}\n")
            CurrentLog.close()
            os_move(f"logs/{CurrentLogName}.log", f"logs/fatal/{CurrentLogName}.log")
            exit(-1)
        elif mode == "warn":
            CurrentLog.write(f"??? [{now}] {message}\n")
        else:
            CurrentLog.write(f"    [{now}] {message}\n")
    del now, element, message, string_type


def ping(url: str, silent: bool = False):
    if silent:
        console_log("Attempting to ping website...")
    else:
        console_log("Attempting to ping %s..." % url)

    time_load_start = datetime.now()
    try:
        driver.get(url)

        if silent:
            console_log("Successfully pinged website!")
        else:
            console_log("Successfully pinged %s!" % url)

        console_log("Load time took %ss." % str((datetime.now() - time_load_start).total_seconds()))
    except:
        if silent:
            console_log("Failed to ping website!", "warn")
        else:
            console_log("Failed to ping %s!" % url, "warn")
        console_log("Attempt took %ss." % str((datetime.now() - time_load_start).total_seconds()))
    del time_load_start


def locate_datafile(url: str) -> str:
    if url.startswith("https://"):
        datafile = url[8:]
    elif url.startswith("http://"):
        datafile = url[7:]

    try:
        return datafile.split("/", 1)[0]
    except:
        return


def open_datafile(datafile: str):
    try:
        with open(f"auth/{datafile}.txt", mode="r") as f:
            return f.readlines()
    except FileNotFoundError:
        console_log("Authentication file not found!", "warn")
        if config.AllowAuthCreator:
            console_log("First time setup initiated...", "warn")
            from getpass import getpass
            with open(f"auth/{datafile}.txt", mode="x+") as f:
                f.write(str(authentication.encrypt(bytes(input("Username: "), "utf-8"), config.key), "utf-8"))
                f.write("\n")
                f.write(str(authentication.encrypt(bytes(getpass("Password: "), "utf-8"), config.key), "utf-8"))
            with open(f"auth/{datafile}.txt", mode="r") as f:
                return f.readlines()
        return


def authenticate(url: str):
    console_log("Locating fields...")

    datafile = locate_datafile(url)
    data = open_datafile(datafile)

    if not data:
        return

    console_log("Attempting authentication...")

    # USR
    for inputtype in ("username", "email", "text"):
        try:
            driver.find_element_by_css_selector(f"input[type={inputtype}]").send_keys(str(authentication.decrypt(bytes(data[0], "utf-8"), config.key), "utf-8"))
            break
        except NoSuchElementException:
            pass

    # PASS
    try:
        driver.find_element_by_css_selector("input[type='password']").send_keys(str(authentication.decrypt(bytes(data[1], "utf-8"), config.key), "utf-8"))
    except NoSuchElementException:
        pass

    # LOG IN
    try:
        driver.find_element_by_css_selector("input[type = 'submit']").click()
    except NoSuchElementException:
        pass

    for inputtype in ("a[title='Login']", "a[title='login']", "a[title='Log in']", "a[title='log in']", "a[title='Submit']", "a[title='submit']"):
        try:
            for e in driver.find_elements_by_css_selector(inputtype):
                if "http" not in e.get_attribute("href"):
                    e.click()
                    working_element = e
                    break
        except NoSuchElementException:
            pass

    try:
        driver.find_element_by_css_selector("input[type='password']")
        # TODO: BUG - Sometimes clunky and may recognise as not logged in
        console_log('Login information for user "%s" on website %s may be incorrect!' % (str(authentication.decrypt(bytes(data[0], "utf-8"), config.key), "utf-8"), url), "warn")
        return False
    except NoSuchElementException:
        console_log('Authenticated at %s as "%s"!' % (url, str(authentication.decrypt(bytes(data[0], "utf-8"), config.key), "utf-8")))
        return True


def isotime():
    for url in config.URLs:
        fileName = locate_datafile(url)

        # try:
        #     read_csv("data/%s.csv" % fileName)
        #     os_rm("data/%s.csv" % fileName) # TODO: Decide - Either delete the file and recreate it, or read the file and add onto it.
        #     df = DataFrame(columns=["title", "date", "start_time", "end_time", "extras", "disabled"])
        # except:
        #     df = DataFrame(columns=["title", "date", "start_time", "end_time", "extras", "disabled"])

        try:
            read_csv(f"data/{fileName}.csv")
            os_move(f"data/{fileName}.csv", f"data/{fileName}.old.csv")
        except:
            console_log("Did not find old file. Ignoring...", "warn")

        df = DataFrame(columns=["title", "date", "start_time", "end_time", "extras", "disabled"])

        for execution in config.URLs[url]:
            """Execution types: PRESENTWEEK, NEXTWEEK, PASTWEEK, NEXT30 (next 30 weeks) or PAST30 (past 30 weeks)."""
            Year, WeekYear, _ = datetime.today().isocalendar()

            if driver.current_url != url:
                ping(url)

            try:
                if config.loggedElement[fileName] is not None:
                    if driver.find_element_by_xpath(config.loggedElement[fileName]):
                        pass
            except KeyError:
                console_log("Incorrect logging element specified.", "warn")
                continue
            except NoSuchElementException:
                if authenticate(url):
                    pass
                else:
                    console_log("Failed to authenticate at %s!" % url, "warn")
                    continue

            if execution.lower() == "presentweek": # TODO: REDO COMPLETELY AGAIN
                console_log('Attempting to grab present week for profile "%s".' % config.titles[fileName])

                try:
                    console_log("Pulling data...")
                    _, week = driver.find_element_by_xpath('//*[@id="dnn_ctr454_ModuleContent"]/div/div[1]/div/h3').text.split(" - ")
                    if week.endswith(")"): week = week[:-1]
                    week = week.split(" ", 3)

                    weekdays = {}

                    for i in range(0, 7):
                        ending_time = driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_ThisWeekRepeater_weekRow_%i"]/td[3]' % i).text

                        if " " in ending_time:
                            weekdays[driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_ThisWeekRepeater_weekRow_%i"]/td[1]' % i).text] = \
                                [driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_ThisWeekRepeater_weekRow_%i"]/td[2]' % i).text,
                                 ending_time.split(" ")[0],
                                 ending_time.split(" ")[1]]
                        else:
                            weekdays[driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_ThisWeekRepeater_weekRow_%i"]/td[1]' % i).text] = \
                                [driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_ThisWeekRepeater_weekRow_%i"]/td[2]' % i).text,
                                 ending_time,
                                 None]

                    del ending_time
                    console_log("Successfully pulled data!")

                    try:
                        console_log("Pushing data...")

                        for (day, rel) in zip_longest(weekdays, range(len(weekdays))):
                            if monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1] >= int(week[0]) + rel:
                                date = datetime.strptime("%s %s %s" % ((int(week[0]) + rel), week[1], week[2]), "%d %b %Y")
                            else:
                                date = datetime.strptime("%s %s %s" % ((int(week[0]) + rel) - monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1], datetime.strptime(week[1], "%b").month + 1,
                                                                       week[2]), "%d %m %Y")

                            df = df.append(DataFrame([[config.titles[fileName], date, weekdays[day][0], weekdays[day][1], weekdays[day][2], 0]], columns=["title", "date", "start_time", "end_time", "extras", "disabled"]),
                                           ignore_index=True)

                            console_log('Successfully pushed "%s" for "%s"!' % ([date.year, date.month, date.day], config.titles[fileName]))
                    except:
                        console_log("Failed whilst pushing %s data!" % config.titles[fileName], "warn")
                except:
                    console_log("Failed whilst pulling data!", "warn")

            if execution.lower() == "nextweek":
                console_log('Attempting to grab next week for profile "%s".' % config.titles[fileName])

                try:
                    console_log("Pulling data...")
                    _, week = driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_NextWeekPanel"]/div[1]/div/h3').text.split(" - ")
                    if week.endswith(")"): week = week[:-1]
                    week = week.split(" ", 3)

                    weekdays = {}

                    for i in range(0, 7):
                        ending_time = driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_NextWeekRepeater_weekRow_%i"]/td[3]' % i).text

                        if " " in ending_time:
                            weekdays[driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_NextWeekRepeater_weekRow_%i"]/td[1]' % i).text] = \
                                [driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_NextWeekRepeater_weekRow_%i"]/td[2]' % i).text,
                                 ending_time.split(" ")[0],
                                 ending_time.split(" ")[1]]
                        else:
                            weekdays[driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_NextWeekRepeater_weekRow_%i"]/td[1]' % i).text] = \
                                [driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_NextWeekRepeater_weekRow_%i"]/td[2]' % i).text,
                                 ending_time,
                                 None]

                    del ending_time
                    console_log("Successfully pulled data!")

                    try:
                        console_log("Pushing data...")

                        for (day, rel) in zip_longest(weekdays, range(len(weekdays))):
                            if monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1] >= int(week[0]) + rel:
                                date = datetime.strptime("%s %s %s" % ((int(week[0]) + rel), week[1], week[2]), "%d %b %Y")
                            else:
                                date = datetime.strptime("%s %s %s" % ((int(week[0]) + rel) - monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1],
                                                                       datetime.strptime(week[1], "%b").month + 1, week[2]), "%d %m %Y")

                            df = df.append(DataFrame([[config.titles[fileName], date, weekdays[day][0], weekdays[day][1], weekdays[day][2], 0]], columns=["title", "date", "start_time", "end_time", "extras",
                                                                                                                              "disabled"]),
                                           ignore_index=True)

                            console_log('Successfully pushed "%s" for "%s"!' % ([date.year, date.month, date.day], config.titles[fileName]))
                    except:
                        console_log("Failed whilst pushing %s data!" % config.titles[fileName], "warn")
                except Exception:
                    console_log("Failed whilst pulling data!", "warn")

            elif execution.lower().startswith("next"):
                WeekYear += int(execution[-2:])
                # TODO: Next Execution type

            if execution.lower() == "pastweek":
                # TODO: Past week Execution type
                WeekYear -= 1
            elif execution.lower().startswith("past"):
                # TODO: Past weeks Execution types
                WeekYear -= int(execution[-2:])

        df.to_csv(f"data/{fileName}.csv", index=False, sep=";", na_rep="-")

        if len(config.SaveLocation) > 0:
            for sl in config.SaveLocation:
                sl_loc = sl + "/HTMLScrap/"

                os_fullpath(sl_loc).mkdir(parents=True,  exist_ok=True)

                if "data" in config.SavedInformation:
                    try:
                        os_cp(f"data/{fileName}.csv", sl_loc)
                    except FileNotFoundError:
                        console_log(f'Could not copy data file "{fileName}.csv" to "{sl_loc}"!', "warn")

if __name__ == "__main__":
    # CWD = os_getcwd()
    # print(CWD)

    # Startup

    if config.FileLogging:
        os_fullpath("logs/fatal").mkdir(parents=True, exist_ok=True)

        CurrentLogName = str(datetime.now().strftime('%m-%d-%Y %H%M%S'))

        open(r"logs/%s.log" % CurrentLogName, "x")
        CurrentLog = open(r"logs/%s.log" % CurrentLogName, "a")

        if config.FileLogLimit:
            for files in os_search(r"logs/"):
                while len(files[2]) > config.FileLogHistory - 1:
                    os_rm(min(["logs/{0}".format(f) for f in files[2]], key=os_path.getctime))
                    files[2].pop(0)

    if len(config.key) < 1:
        from getpass import getpass

        config.key = getpass("Key:")

    os_fullpath("data").mkdir(parents=True, exist_ok=True)

    if not os_path.exists("auth"):
        os_mkdir("auth")
        config.AllowAuthCreator = True
        console_log("Enabling first time setup. Automatic creation of authentication files enabled.", "warn")

    console_log('Running selentium version: "%s".' % webdriver.__version__)
    console_log('Running cryptography version: "%s".' % CryptVer)
    console_log('Running pandas version: "%s".' % PandasVer)

    if sysplatform() == "Windows":
        browser = os_path.realpath(os_getcwd() + "/chromedriver.exe")
    else:
        if config.SelectedBrowser:
            browser = os_path.realpath(config.SelectedBrowser)
        else:
            console_log("No browser has been setup!\nExit Code: -1", "error")
            raise WebDriverException()

    console_log('Selected browser at system path: "%s"' % browser)

    log = os_path.realpath("..\\.temp")

    if os_path.exists(browser):
        console_log('Located browser at "%s".' % browser)
    else:
        console_log("Unable to locate browser!\nExit Code: -1", "error")
        raise FileNotFoundError("Unable to locate browser!")

    console_log("Attempting to run browser...")

    time_start = datetime.now()

    try:
        driver = webdriver.Chrome(options=config.BrowserOptions, executable_path=browser)
        console_log("Browser successfully executed!")
    except WebDriverException as err:
        console_log(str(err), "warn")
        console_log("Browser window crashed or failed to open!\nTime elapsed: %fs.\nExit code: -1" % (datetime.now() - time_start).total_seconds(), "error")
        del time_start
        raise EnvironmentError("Browser has crashed!")

    try:
        driver.set_page_load_timeout(config.BrowserLoadTimeout)
        console_log(f"Set page load timeout to {config.BrowserLoadTimeout}s.")
    except:
        console_log("Failed to set page load timeout!", "warn")

    # Execution

    isotime()

    while not config.Crontab:
        if (datetime.now().minute == 0) and (datetime.now().second == 0):
            isotime()
        else:
            sleep(1)
    
    # Exit

    driver.quit()
    console_log("Finished")
    try:
        del CurrentLog
        CurrentLog.close()
    except NameError:
        pass

    if len(config.SaveLocation) > 0:
        if "logs" in config.SavedInformation:
            for sl in config.SaveLocation:
                sl_loc = sl + "/HTMLScrap/logs/"
                os_fullpath(sl_loc).mkdir(parents=True, exist_ok=True)

                os_dircp("logs", sl_loc, dirs_exist_ok=True)

            # try:
            # except FileNotFoundError:
            #     console_log(f'Could not copy data file "{fileName}.csv" to "{sl_loc}"!', "warn")