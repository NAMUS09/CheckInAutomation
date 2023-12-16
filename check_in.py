import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def should_check_in():
    week_day = datetime.datetime.now().weekday()
    current_time = datetime.datetime.now().time()

    is_time_9_to_11 = datetime.time(9, 0) <= current_time <= datetime.time(11, 0)

    return is_time_9_to_11 and week_day != 5 and week_day != 6


def check_in():
    url = "https://timesheet.cetastech.com/"
    user_name = 'CIT288'
    password = 'CIT288'

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

        time.sleep(2)

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


