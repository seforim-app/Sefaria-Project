from selenium import webdriver
import os
import requests

# Use environment variables for tests

# Arguments
# * Selenium Server Hostname
# * Application Hostname

CAPABILITIES = [
    {'browser': 'Firefox'},
]

def ensureEnvVars():
    if 'SELENIUM_SERVER_URL' in os.environ:
        seleniumServerUrl = os.environ['SELENIUM_SERVER_URL']
    else:
        print("Please set the SELENIUM_SERVER_HOSTNAME environment variable and rerun.")
        exit(1)

    if 'APPLICATION_HOSTNAME' in os.environ:
        applicationUrl = os.environ['APPLICATION_HOSTNAME'] # maybe add trailing slash if missing
    else:
        print("Please set the APPLICATION_HOSTNAME environment variable and rerun.")
        exit(1)

def ensureServerReachability():
    # Check reachability of named servers
    for site in [applicationUrl, seleniumServerUrl]:
        resp = requests.get(site).status_code
        if resp > 399:
            print("Site {} not reachable. Please make sure it is running and rerun this script".format(site))
            exit(1)
        else:
            print("Site {} is reachable.".format(site))

def ensureSeleniumCapabilities():
    """
    Make sure the target Selenium server has the capabilities we need. 
    """
    return

def ensureDriverFunctionality(driver):
    """
    Make sure the webdriver can make requests
    """

    try:
        driver.get("https://google.com")
        assert driver.title == "Google"
    except Exception as e:
        print(e)
        print("Driver could not make a web request. Please check its functionality")
        exit(1)
    else: 
        print("The driver successfullly made a web request. Proceeding.")



def createFirefoxDriver(seleniumServerUrl="http://localhost:4444/wd/hub",):
    """
    createFirefoxDriver creates a firefox driver

    For now, doesn't require credentials
    """
    fopt = webdriver.FirefoxOptions()
    fopt.add_argument('--headless')
    return webdriver.Remote(command_executor=seleniumServerUrl, options=fopt)

if __name__ == "__main__":
    """
    Script entrypoint

    Example invocation:
    SELENIUM_SERVER_URL="http://localhost:4444/wd/hub" APPLICATION_HOSTNAME="https://vecino.cauldron.sefaria.org/" python3 ./run_test.py
    """

    if 'SELENIUM_SERVER_URL' in os.environ:
        seleniumServerUrl = os.environ['SELENIUM_SERVER_URL']
    else:
        print("Please set the SELENIUM_SERVER_HOSTNAME environment variable and rerun.")
        exit(1)

    if 'APPLICATION_HOSTNAME' in os.environ:
        applicationUrl = os.environ['APPLICATION_HOSTNAME'] # maybe add trailing slash if missing
    else:
        print("Please set the APPLICATION_HOSTNAME environment variable and rerun.")
        exit(1)

    # Make sure the tests are ready to go
    #args = ensureEnvVars()
    ensureServerReachability()
    ensureSeleniumCapabilities()

    # Create Driver
    driver = createFirefoxDriver(seleniumServerUrl=seleniumServerUrl)
    ensureDriverFunctionality(driver)

    
    # get homepage and get title, and test
    driver.get(applicationUrl)
    print("Current URL: {}".format(driver.current_url))
    print("Current title: {}".format(driver.title))


    assert driver.current_url == applicationUrl
    assert driver.title == "Sefaria: a Living Library of Jewish Texts Online"

    print("Preliminary tests finishedTests finished")