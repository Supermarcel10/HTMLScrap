from selenium.webdriver.chrome.options import Options as ChromeOptions

# Directory of your browser.
# Note: Windows is already supported out of box.
SelectedBrowser = "/usr/bin/chromedriver"

# Options of how the browser is executed.
BrowserOptions = ChromeOptions()

BrowserOptions.add_argument("--headless")
BrowserOptions.add_argument("--disable-gpu")

BrowserLoadTimeout = 30

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
FileLogLimit = True
FileLogHistory = 24

# Setting these values determine the *.csv file titles (names), which can then be imported elsewhere such as a website.
titles = {
    "extranet.barnetsouthgate.ac.uk": "college",
    "memployees.sportsdirectservices.com": "work",
    "*": "other"
}

# Set this value to the xpath of where the login data is inserted
loggedElement = {"extranet.barnetsouthgate.ac.uk": None,
                 "memployees.sportsdirectservices.com": '//*[@id="dnn_ctr454_ModuleContent"]/div/div[1]/div/h3'
                 }

# Set this value to toggle the creation of auth files.
# Default: False
# False - Disable auth generation if no file is located (recommended)
# True - Prompt the user to input a username and password, which will be stored for auth.
AllowAuthCreator = False

# Setting the key to a value will read the key and use it for decryption.
# If a key is not specified, a key will be asked on every startup.
# WARNING: SETTING A PERMANENT KEY IS A SAFETY VULNERABILITY!
key = ""
