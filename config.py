from selenium.webdriver.chrome.options import Options as ChromeOptions

# Directory of your browser.
# Note: Windows is already supported out of box as long as chromedriver.exe is present in the files.
SelectedBrowser = "/usr/bin/chromedriver"

# Options of how the browser is executed.
# [Default: --headless --disable-gpu, 30]
BrowserOptions = ChromeOptions()

# BrowserOptions.add_argument("--headless")
# BrowserOptions.add_argument("--disable-gpu")

BrowserLoadTimeout = 30

# A set of URLs the program executes and the type of execution..
URLs = {"http://memployees.sportsdirectservices.com/Working-Hours/": ["PresentWeek", "NextWeek"],
        "https://secure.fourth.com/": ["PresentWeek", "NextWeek"],
        "https://extranet.barnetsouthgate.ac.uk/": ["Past30", "PresentWeek", "Next30"]}

# Setting this value will determine if you use Linux Crontab for running your task.
#           True - Disables while loop for grabbing data every set time.
#           False - Enables while loop, that will grab data every set time.
# [Default: True]
Crontab = True

# Setting this value will determine if data is stored in separate datafiles.
#           True - Stores all data into one file, which name can be set below.
#           False - Stores all data in separate files. TODO: Create combined data storing!
# [Default: True, "data"]
CombinedDatafiles = True

CombinedDatafileName = "data"

# Location where files are cloned to - for use in a web server, easier access or sharing.
# You may need to run the main python script as an escalated user in order to access specified location.
# Leave empty "[]" to disable saving.
# [Default: <empty>]
SaveLocation = ["C:/"]
# SaveLocation = ["/NETSHARE/General"]

# Setting this value will determine what data is saved with the cloned files.
# Available options: logs, data
# [Default: "data"] # TODO: Add log data saving
SavedInformation = ["data", "logs"]

# Setting this value will determine if a log file is created for every run.
# [Default: True]
FileLogging = True

# Setting this value will determine how many log files will be kept.
# Oldest log files will be deleted. Fatal crashes will be kept separately.
# [Default: True, 24]
FileLogLimit = True
FileLogHistory = 24

# Setting these values determine the *.csv file titles (names), which can then be imported elsewhere such as a website.
titles = {
    "extranet.barnetsouthgate.ac.uk": "college",
    "memployees.sportsdirectservices.com": "work",
    "secure.fourth.com": "work",
    "*": "other"
}

# Set this value to the xpath of where the login data is inserted
loggedElement = {"extranet.barnetsouthgate.ac.uk": None,
                 "secure.fourth.com": '/html/body/div[5]/div/div/div[2]/div[3]/div[1]/div[1]/div[2]/div/ul/li[6]/div[2]/span[1]/span',
                 "memployees.sportsdirectservices.com": '//*[@id="dnn_ctr454_ModuleContent"]/div/div[1]/div/h3'
                 }

# Set this value to toggle the creation of auth files.
# False - Disable auth generation if no file is located (recommended)
# True - Prompt the user to input a username and password, which will be stored for auth.
# [Default: False]
AllowAuthCreator = False # TODO: Fix toggle after first creation. User cannot add new website auths after first creation.

# Setting the key to a value will read the key and use it for decryption.
# If a key is not specified, a key will be asked on every startup.
# WARNING: SETTING A PERMANENT KEY IS A SAFETY VULNERABILITY!
key = ""
