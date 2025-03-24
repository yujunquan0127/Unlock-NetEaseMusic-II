# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00582E8CAA749E02DD56ABE4832556756981419391E96A40BB47CF5FF04A9042FBF4E6761A776B626418C8075B6B38DB6DA5D6E48BD56BA3CEE991E61AE14E58B2720AC540938ECA2FA0CB3642BB795689F121288829001C4E8B0DD7799E8548D35565195345CA0A605B795865C1F68824288B5FFCCDCEAC6149834B6D03C8F163A9BAD981D0F96B391023F70C816EAE627E92FC6581A6DD944FE60BC8469CF1B76CE90F0A3B240461330F629D1888EDFDCBD22787DE3CAD28B55A5E8A726D985076A170ED94B2AD46214ED1C724362BFC68DD5A0654CBD9C28854A8C721A063AB45730E433B5EA18D177C4553BA3443C7B5F8403C5A051B2CF264B3F409E88AC5C55992B20819C7303241CFD0560F3B053AC21A3F279277BED68BA5546D11D572064A44FF4E64C7F61D8EB43EDFE0CD26627A81D90F09B2151A19B55702DD7F99DE96AC09D960A06FB38750A297096B79721CAE687B7948B6A5AD53B3E3FB42BA"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
