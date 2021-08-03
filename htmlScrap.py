import os

import selenium.common.exceptions

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken

from torch import cuda
from platform import system as sysplatform
from itertools import zip_longest
from os import path as os_path, mkdir as os_mkdir, getcwd as os_getcwd, remove as os_rm
from pandas import DataFrame, read_csv
from sty import fg
from time import sleep
from datetime import datetime, timedelta
from calendar import monthrange
from secrets import token_bytes
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

backend = default_backend()
iterations = 100_000
monthsShort = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthsLong = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


# Directory of your browser.
# Note: Windows is already supported out of box.
SelectedBrowser = ""

# Options of how the browser is executed.
BrowserOptions = ChromeOptions()

BrowserOptions.add_argument("--headless")
BrowserOptions.add_argument("--disable-gpu")

# A set of URLs the program executes and the type of execution..
URLs = {"http://memployees.sportsdirectservices.com/Working-Hours": ["PresentWeek", "NextWeek"],
        "https://extranet.barnetsouthgate.ac.uk/": ["Past30", "PresentWeek", "Next30"]}

# Setting this value will determine if you use Linux Crontab for running your task.
#           True - Disables while loop for grabbing data every set time
#           False - Enables while loop, that will grab data every set time
Crontab = True

# Setting this value will determine if a log file is created for every run.
FileLogging = True

# Setting this value will determine how many log files will be kept.
# Oldest log files will be deleted. Fatal crashes will be kept separately.
FileLogHistory = 24

# Setting these values determine the *.csv file titles (names), which can then be imported elsewhere such as a website.
titles = {
    "extranet.barnetsouthgate.ac.uk": "college",
    "memployees.sportsdirectservices.com": "work",
    "*": "other"
}

# Set this value to the xpath of where the data is pulled from
loggedElement = {"extranet.barnetsouthgate.ac.uk": None,
                 "memployees.sportsdirectservices.com": '//*[@id="dnn_ctr454_ModuleContent"]/div/div[1]/div/h3'
                 }

# Setting the key to a value will read the key and use it for decryption.
# If a key is not specified, a key will be asked on every startup.
# WARNING: SETTING A PERMANENT KEY IS A SAFETY VULNERABILITY!
key = ""



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

    if FileLogging:
        if mode == "error":
            CurrentLog.write(f"!!! [{now}] {message}\n")
        elif mode == "warn":
            CurrentLog.write(f"??? [{now}] {message}\n")
        else:
            CurrentLog.write(f"    [{now}] {message}\n")
    del now, element, message, string_type


def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))


def password_encrypt(password: bytes, key: str, iterations: int = iterations) -> bytes:
    salt = token_bytes(16)
    key = _derive_key(key.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(password)),
        )
    )


def password_decrypt(token: bytes, key: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(key.encode(), salt, iterations)
    return Fernet(key).decrypt(token)


def ping(url: str, silent: bool = False):
    if silent:
        console_log("Attempting to ping website...")
    else:
        console_log("Attempting to ping %s..." % url)

    try:
        time_load_start = datetime.now()
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

    datafile, _ = datafile.split("/", 1)
    return datafile


# TODO: Make datafile creator
def open_datafile(datafile: str):
    # if datafile.startswith("extranet"):
    #     with open(f"auth\{datafile}.txt", mode="w") as f:
    #         f.write(str(password_encrypt(bytes("username", "utf-8"), key), "utf-8"))
    #         f.write("\n")
    #         f.write(str(password_encrypt(bytes("password", "utf-8"), key), "utf-8"))

    try:
        with open(f"auth\{datafile}.txt", mode="r") as f:
            return f.readlines()
    except FileNotFoundError:
        console_log("Authentication file not found! Continuing...", "warn")
        return


def locate_login(url: str):
    console_log("Locating fields...")

    datafile = locate_datafile(url)
    data = open_datafile(datafile)

    if not data:
        return
    # TODO: Redo in the form of an option menu.
    if datafile == "memployees.sportsdirectservices.com":
        try:
            driver.find_element_by_id("dnn_ctr462_Login_Login_DNN_txtUsername").send_keys(str(password_decrypt(bytes(data[0], "utf-8"), key), "utf-8"))
            driver.find_element_by_id("dnn_ctr462_Login_Login_DNN_txtPassword").send_keys(str(password_decrypt(bytes(data[1], "utf-8"), key), "utf-8"))

            console_log("Successfully located fields!")

            return authenticate(url, str(password_decrypt(bytes(data[0], "utf-8"), key), "utf-8"))
        except InvalidToken:
            console_log("Cryptography key for authentication is invalid!\nContinuing...", "warn")
        except:
            console_log("Failed to locate fields for website %s!" % url, "warn")

    elif datafile == "extranet.barnetsouthgate.ac.uk":
        try:
            _, week_num, _ = datetime.today().isocalendar()
            week_num += 22
            if week_num > 52:
                return False

            ping(f"https://%s:%s@extranet.barnetsouthgate.ac.uk/registers/timetable/user/week/{week_num}" % (str(password_decrypt(bytes(data[0], "utf-8"), key), "utf-8"),
                                                                                                                  str(password_decrypt(bytes(data[1], "utf-8"), key), "utf-8")), True)
            return True
        except InvalidToken:
            console_log("Cryptography key for authentication is invalid!\nContinuing...", "warn")
            return False
        except:
            console_log("Failed to login to website %s!" % url, "warn")
            return False


def authenticate(url: str, username: str):
    try:
        console_log("Attempting authentication...")

        driver.find_element_by_id("dnn_ctr462_Login_Login_DNN_cmdLogin").click()
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'dnn_ctr454_ModuleContent')))

        console_log("Authenticated at %s as %s!" % (url, username))
        return True
    except:
        console_log('Login information for user "%s" on website %s may be incorrect!' % (username, url), "warn")


def shortToLongDayName(original):
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


# def isotime():
    # TODO: Open or create datafile


def isotime():
    print(URLs)

    for url in URLs:
        fileName = locate_datafile(url)

        try:
            read_csv("data/%s.csv" % fileName)
            os_rm("data/%s.csv" % fileName) # TODO: Maybe update
            df = DataFrame(columns=["title", "date", "start_time", "end_time", "extras", "disabled"])
        except:
            df = DataFrame(columns=["title", "date", "start_time", "end_time", "extras", "disabled"])

        for execution in URLs[url]:
            """Execution types: PRESENTWEEK, NEXTWEEK, PASTWEEK, NEXT30 (next 30 weeks) or PAST30 (past 30 weeks)."""
            Year, WeekYear, _ = datetime.today().isocalendar()

            if driver.current_url != url:
                ping(url)

            try:
                if loggedElement[fileName] is not None:
                    if driver.find_element_by_xpath(loggedElement[fileName]):
                        continue
            except selenium.common.exceptions.NoSuchElementException:
                if locate_login(url):
                    continue
                else:
                    console_log("Failed to authenticate at %s!" % url, "warn")
            finally:
                if execution.lower() == "presentweek":
                    console_log('Attempting to grab present week for profile "%s".' % titles[fileName])

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
                            console_log("Pushing data.")

                            for (day, rel) in zip_longest(weekdays, range(len(weekdays))):
                                if monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1] >= int(week[0]) + rel:
                                    date = datetime.strptime("%s %s %s" % ((int(week[0]) + rel), week[1], week[2]), "%d %b %Y")
                                else:
                                    date = datetime.strptime("%s %s %s" % ((int(week[0]) + rel) - monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1],
                                                                           datetime.strptime(week[1], "%b").month + 1, week[2]), "%d %m %Y")

                                df = df.append(DataFrame([[titles[fileName], date, weekdays[day][0], weekdays[day][1], weekdays[day][2], 0]], columns=["title", "date", "start_time",
                                                                                                                                                       "end_time", "extras", "disabled"]),
                                               ignore_index=True)

                                console_log('Successfully pushed "%s" for "%s"!' % ([date.year, date.month, date.day], titles[fileName]))
                        except:
                            console_log("Failed whilst pushing %s data!" % titles[fileName], "warn")
                    except:
                        console_log("Failed whilst pulling data!", "warn")

                if execution.lower() == "nextweek":
                    console_log('Attempting to grab next week for profile "%s".' % titles[fileName])

                    try:
                        console_log("Pulling data...")
                        _, week = driver.find_element_by_xpath('//*[@id="dnn_ctr454_WorkingHoursView_NextWeekPanel"]/div[1]/div/h3').text.split(" - ")
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
                            console_log("Pushing data.")

                            for (day, rel) in zip_longest(weekdays, range(len(weekdays))):
                                if monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1] >= int(week[0]) + rel:
                                    date = datetime.strptime("%s %s %s" % ((int(week[0]) + rel), week[1], week[2]), "%d %b %Y")
                                else:
                                    date = datetime.strptime("%s %s %s" % ((int(week[0]) + rel) - monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1],
                                                                           datetime.strptime(week[1], "%b").month + 1, week[2]), "%d %m %Y")

                                df = df.append(DataFrame([[titles[fileName], date, weekdays[day][0], weekdays[day][1], weekdays[day][2], 0]], columns=["title", "date", "start_time", "end_time", "extras",
                                                                                                                                  "disabled"]),
                                               ignore_index=True)

                                console_log('Successfully pushed "%s" for "%s"!' % ([date.year, date.month, date.day], titles[fileName]))
                        except:
                            console_log("Failed whilst pushing %s data!" % titles[fileName], "warn")
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

        df.to_csv("data/%s.csv" % fileName, index=False, sep=";", na_rep="---")



if len(key) < 1:
    from getpass import getpass
    key = getpass("Key:")

if not os_path.exists("data"):
    os_mkdir("data")

if not os_path.exists("auth"):
    os_mkdir("auth")

if FileLogging:
    if not os_path.exists("logs"):
        os_mkdir("logs")
        os_mkdir("logs/fatal")

    now = str(datetime.now().strftime('%m-%d-%Y %Hh %Mm %Ss'))

    open(r"logs/%s.txt" % now, "x")
    CurrentLog = open(r"logs/%s.txt" % now, "a")
    # TODO: Enforce limit
    # TODO: Movement to fatal error storage.


console_log('Running selentium version: "%s".' % webdriver.__version__)


if sysplatform() == "Windows":
    browser = os_path.realpath(os_getcwd() + "/chromedriver.exe")
else:
    if SelectedBrowser:
        browser = os_path.realpath(SelectedBrowser)
    else:
        console_log("No browser has been setup!\n Exit Code: -1", "error")
        raise selenium.common.exceptions.WebDriverException()

console_log('Selected browser at system path: "%s"' % browser)

log = os_path.realpath("..\\.temp")

if os_path.exists(browser):
    console_log('Located browser at "%s".' % browser)
else:
    console_log("Unable to locate browser!\n Exit Code: -1", "error")
    raise FileNotFoundError("Unable to locate browser!")

console_log("Attempting to run browser...")

try:
    time_start = datetime.now()
    driver = webdriver.Chrome(options=BrowserOptions, executable_path=browser)
    console_log("Browser successfully executed!")
except:
    console_log("Browser window crashed or failed to open!", "error")
    console_log("Time elapsed: %fs.\n Exit code: -1" % (datetime.now() - time_start).total_seconds())
    del time_start
    raise EnvironmentError("Browser has crashed!")

try:
    driver.set_page_load_timeout(30)
    console_log("Set page load timeout to 30s.")
except:
    console_log("Failed to set page load timeout!", "warn")


if __name__ == "__main__":
    isotime()

    while not Crontab:
        if (datetime.now().minute == 0) and (datetime.now().second == 0):
            isotime()
        else:
            sleep(1)

driver.quit()
console_log("Finished")
CurrentLog.close()