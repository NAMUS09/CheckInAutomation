import os
import platform
import shutil
import time as timeSleep

from selenium import webdriver
from UI.showMessage import show_message_edit_config
from datetime import datetime, time
from selenium.webdriver.common.by import By
from utils.common import url_reachable
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from utils.logging import log_error, log_info


class CheckInConditon:
    def __init__(self, start_time: str, end_time: str, weekdays: set()): # type: ignore
        self.start_time = start_time
        self.end_time = end_time
        self.weekdays = weekdays



def should_check_in(checkIn: CheckInConditon):
    # get user preference time
    start_time_obj = datetime.strptime(checkIn.start_time, "%H:%M").time()
    start_time_hour = start_time_obj.hour
    start_time_min = start_time_obj.minute

    end_time_obj = datetime.strptime(checkIn.end_time, "%H:%M").time()
    end_time_hour = end_time_obj.hour
    end_time_min = end_time_obj.minute

    
    # current 
    current_date_time = datetime.now()
    today = current_date_time.weekday()
    current_time = current_date_time.time()

    within_time_interval = time(start_time_hour, start_time_min) <= current_time <= time(end_time_hour, end_time_min)

    return within_time_interval and today in checkIn.weekdays



def get_check_in_time(driver: webdriver):
    date_time_element = driver.find_elements(By.ID, 'spanInDateTime')[0]
    return date_time_element.get_attribute('innerHTML')


def is_today(check_in_time_str):
    # Define the format of the date string
    date_format = '%d/%m/%Y %I:%M %p'
    
    # Parse the check-in time string into a datetime object
    check_in_time = datetime.strptime(check_in_time_str, date_format)
    
    # Get today's date
    today = datetime.now()
    
    # Compare the date part of the check-in time with today's date
    return check_in_time.date() == today.date()


def check_out(driver: webdriver):
    check_out_id = driver.find_elements(By.ID, 'btnCheckOut')[0]
    check_out_id.click()
    timeSleep.sleep(1)



def get_browser():
    system = platform.system()

    chrome_paths = []
    edge_paths = []

    # Windows specific paths for Chrome and Edge
    if system == "Windows":
        chrome_paths = [
            shutil.which("chrome"),
            shutil.which("chrome.exe"),
            os.path.join(os.getenv('ProgramFiles(x86)'), "Google/Chrome/Application/chrome.exe"),
            os.path.join(os.getenv('ProgramFiles'), "Google/Chrome/Application/chrome.exe")
        ]
        edge_paths = [
            shutil.which("msedge"),
            shutil.which("msedge.exe"),
            os.path.join(os.getenv('ProgramFiles(x86)'), "Microsoft/Edge/Application/msedge.exe"),
            os.path.join(os.getenv('ProgramFiles'), "Microsoft/Edge/Application/msedge.exe")
        ]

    # Linux specific paths for Chrome and Edge
    elif system == "Linux":
        chrome_paths = [
            shutil.which("google-chrome"),
            shutil.which("chrome"),
            "/usr/bin/google-chrome",
            "/usr/local/bin/google-chrome"
        ]
        edge_paths = [
            shutil.which("microsoft-edge"),
            "/usr/bin/microsoft-edge",
            "/usr/local/bin/microsoft-edge"
        ]

    # macOS specific paths for Chrome and Edge
    elif system == "Darwin":
        chrome_paths = [
            shutil.which("chrome"),
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ]
        edge_paths = [
            shutil.which("msedge"),
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
        ]

    # Check for Chrome installation
    for path in chrome_paths:
        if path and os.path.exists(path):
            return "Chrome"

    # Check for Edge installation
    for path in edge_paths:
        if path and os.path.exists(path):
            return "Edge"

    return None  # Return None if neither browser is found


def get_chrome_driver() -> webdriver:
    # Use Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)

    return driver

def get_edge_driver()-> webdriver:
    # Use Microsoft Edge
    edge_options = EdgeOptions()
    edge_options.add_argument('--headless')

    driver = webdriver.Edge(options=edge_options)

    return driver


def check_in(self):
    message = "";
    url = "https://timesheet.cetastech.com/"

    log_info(f"Url: {url}")

    if not url_reachable(url):
        message = "Timesheet url is not reachable at the moment!!"
        log_error(message)

        ##show_message("Error", "Timesheet url is not reachable at the moment!!")
        return {'status': "error", 'message': message, 'retry': True}
    

    user_name = self.username
    password = self.password
    # status_type = self.status_type
    # session_type = self.session_type

    browser = get_browser()

    if(browser is None):
        message = "Couldn't initate the check in. Neither Chrome nor Edge is installed!!"
        log_error(message)
        return {'status': "error", 'message': message}

    driver =  get_chrome_driver() if browser == "Chrome" else get_edge_driver()

    try:
        driver.get(url)

        user_name_input = driver.find_element(By.NAME, 'textBoxUserName')
        password_input = driver.find_element(By.NAME, 'textBoxPassword')
        login_button = driver.find_element(By.NAME, 'Login')

        user_name_input.send_keys(user_name)
        password_input.send_keys(password)
        driver.execute_script("arguments[0].click();", login_button)

        timeSleep.sleep(2)

        check_id = driver.find_elements(By.ID, 'myid')

        if not check_id:
            message = "Couldn't login. Please check your username and password"
            log_error(message)
            ##show_message("Alert", "Couldn't login. Please check your username and password")
            return {'status': "error", 'message': message}

        message =f"😍😍 SUCCESS 😍😍 - Logged in for user: {user_name}"
        log_info(message)
        print(message)

        check_in_time = get_check_in_time(driver)

        if check_in_time:
            log_info("User already checked-in")
            status = "success"
            if is_today(check_in_time):
                message = f"User {user_name} has already checked in today at {check_in_time}"
            else:
                log_info("Check out starts..")
                check_out(driver)
                log_info("Check out ends..")
                status = "error"
                message = f"User {user_name} has not checked out at {check_in_time}.User successfully checked out."
            
            log_info(message)
            print(message)
            return {'status': status, 'message': message}
    
        log_info("User not checked-in")

        timeSleep.sleep(1)
        
        check_in_button = driver.find_elements(By.ID, 'btnCheckIn')[0]

        if not check_in_button:
            print("User logged in but couldn't check in")
            return {'status': "error", 'message': f"User {user_name} is logged in but couldn't complete the check-in process"}
        
        # check dropdown before check button click
        # status_type_dropdown = driver.find_element(By.NAME,"WorkType_input")
        # status_type_dropdown.send_keys(status_type)
        # timeSleep.sleep(1)
        # status_type_dropdown.send_keys(Keys.RETURN)
        # status_type_dropdown.send_keys(Keys.TAB)

        # sesstion_type_dropdown = driver.find_element(By.NAME,"Session_input")
        # sesstion_type_dropdown.send_keys(session_type)
        # timeSleep.sleep(1)
        # sesstion_type_dropdown.send_keys(Keys.RETURN)
        # sesstion_type_dropdown.send_keys(Keys.TAB)
        
        check_in_button.click()
        timeSleep.sleep(1)

        message = f"😍😍 SUCCESS 😍😍 - Checked in for user: {user_name}"
        log_info(message)
        print(message)

        # get element with the 'onclick' attribute set to 'openAttendance()'
        attendance_icon = driver.find_elements(By.CSS_SELECTOR, "[onclick='openAttendance()']")[0]
        attendance_icon.click()

        timeSleep.sleep(1);

        check_in_time = get_check_in_time(driver)

        message = f"User {user_name} successfully checked in at {check_in_time}"
        log_info(message)
        print(message)
        
        return {'status': "success", 'message':  message}

    except Exception as e:
        print('😭😭 FAILED 😭😭 - Error:', str(e))
        log_error("Check-in failed!! Please try again later.")
        return { 'status': "error", 'message':  "Check-in failed!! Please try again later.", "retry": True }

    finally:
        driver.quit()



def check_in_thread(self):
    perform_check_in = True
    retry_limit = 3
    title = "Check-In Status"
    message = ""
    show_retry_button = False

    
    while perform_check_in:
        if should_check_in(self):
            retry_attempt = 1
            log_info(f"Check-in attempt {retry_attempt}")

            while retry_attempt <= retry_limit:
                status = check_in(self)
                if not status.get('retry'):
                    break
                retry_attempt += 1

            message = status.get('message')
            show_retry_button = status.get('status') == 'error'

        elif datetime.now().weekday() not in self.weekdays:
            message = "Check-in not triggered - Today is not a configured weekday"

        else:
            message = "Check-in not triggered - Not within the configured time frame"

        log_info(message)
        # Show message
        perform_check_in = show_message_edit_config(title, message, show_retry_button)



