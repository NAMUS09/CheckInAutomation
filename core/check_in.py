import time as timeSleep

from selenium import webdriver
from UI.showMessage import show_message_edit_config
from datetime import datetime, time
from selenium.webdriver.common.by import By
from utils.common import url_reachable, show_message
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckInConditon:
    def __init__(self, start_time: str, end_time: str, weekdays: set()):
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
    


def check_in(self):
    url = "https://timesheet.cetastech.com/"

    if not url_reachable(url):
        ##show_message("Error", "Timesheet url is not reachable at the moment!!")
        return {'status': "error", 'message':"Timesheet url is not reachable at the moment!!", 'retry': True}
    

    user_name = self.username
    password = self.password

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)

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
            ##show_message("Alert", "Couldn't login. Please check your username and password")
            return {'status': "error", 'message': "Couldn't login. Please check your username and password"}

        print("😍😍 SUCCESS 😍😍 - Logged in for user:", user_name)

        check_in_time = get_check_in_time(driver)

        if check_in_time != None and check_in_time != '':
            print("Already checked in for user:", user_name)
            return {'status': "success", 'message':f"User {user_name} has already checked in at {check_in_time}"}
            
        check_in_button = driver.find_elements(By.ID, 'btnCheckIn')[0]

        if not check_in_button:
            print("User logged in but couldn't check in")
            return {'status': "error", 'message': f"User {user_name} is logged in but couldn't complete the check-in process"}

        check_in_button.click()
        print("😍😍 SUCCESS 😍😍 - Checked in for user:", user_name)

        # get element with the 'onclick' attribute set to 'openAttendance()'
        attendance_icon = driver.find_elements(By.CSS_SELECTOR, "[onclick='openAttendance()']")[0]
        attendance_icon.click()

        timeSleep.sleep(1);

        check_in_time = get_check_in_time(driver)
        
        return {'status': "success", 'message': f"User {user_name} successfully checked in at {check_in_time}" }

    except Exception as e:
        print('😭😭 FAILED 😭😭 - Error:', str(e))
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

        # Show message
        perform_check_in = show_message_edit_config(title, message, show_retry_button)



