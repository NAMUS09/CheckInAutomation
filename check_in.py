import time as timeSleep

from datetime import datetime, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from showMessage import MessageBox


class CheckInConditon:
    def __init__(self, start_time: str, end_time: str, weekdays: set()):
        self.start_time = start_time
        self.end_time = end_time
        self.weekDays = weekdays



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

    return within_time_interval and today in checkIn.weekDays


def check_in(self):
    url = "https://timesheet.cetastech.com/"
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

        print("😍😍 SUCCESS 😍😍 - Logged in for user:", user_name)

        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'myAttandanceModal'))
        )

        if not modal.value_of_css_property('display') == 'block':
            print("Already checked in for user:", user_name)
            return "Already checked in for user: {}".format(user_name)

        check_in_buttons = driver.find_elements(By.ID, 'btnCheckIn')

        if check_in_buttons:
            driver.execute_script("arguments[0].click();", check_in_buttons[0])
            print("😍😍 SUCCESS 😍😍 - Checked in for user:", user_name)
            return "Checked in successfully for user: {}".format(user_name)

    except Exception as e:
        print('😭😭 FAILED 😭😭 - Error:', str(e))
        return "Check-in failed"

    finally:
        driver.quit()



def check_in_thread(self):
    current_day = datetime.now().weekday()

    title = "Check-In Status"
    if should_check_in(self):
        status = check_in(self)
        MessageBox.show_message(title, status)

    elif current_day not in self.weekdays:
        MessageBox.show_message(title, "Check-in not triggered - Today is not a configured weekday")
        
    else:
        MessageBox.show_message(title, "Check-in not triggered - Not within the configured time frame")


