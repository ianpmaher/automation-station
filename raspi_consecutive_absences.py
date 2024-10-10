from dotenv import load_dotenv
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime

load_dotenv()
ASPEN_URL=os.getenv("ASPEN_URL")
LOGIN_ID = os.getenv("LOGIN_ID")
PASSWORD = os.getenv("PASSWORD")

download_dir = os.path.join(os.getcwd(), "downloads/consecutive")  # Downloads to the "downloads" folder in your project
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Configure the path for the Chromium WebDriver
chromium_service = Service('/usr/bin/chromedriver')

chrome_options = webdriver.ChromeOptions()
# Set up options for Chromium (such as headless mode, which is optional)
chrome_options = Options()
chrome_options.binary_location = '/usr/bin/chromium-browser'
chrome_options.add_argument('--headless')  # Use headless mode (no UI)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

prefs = {
    "download.default_directory": download_dir,  # Set the download directory
    "download.prompt_for_download": False,       # Disable download prompts
    "plugins.always_open_pdf_externally": True   # Download PDFs instead of opening in the browser
}
chrome_options.add_experimental_option("prefs", prefs)

# Instantiate the driver with the defined options
driver = webdriver.Chrome(service=chromium_service, options=chrome_options)
driver.get(ASPEN_URL)
print(driver.current_url)

driver.implicitly_wait(5)

# Login
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
submit = driver.find_element(By.XPATH, '/html/body/go-root/go-login/go-login-container/div/div/div/go-default-login/form/div[4]/div/button')

username.send_keys(LOGIN_ID)
password.send_keys(PASSWORD)
submit.click()

# Wait for the page to load
#test
driver.implicitly_wait(10)
print(driver.current_url)
print("this worked")

# find attendance tab
attendance_tab = driver.find_element(By.LINK_TEXT, "Attendance")
attendance_tab.click()

# Wait for the page to load
driver.implicitly_wait(5)
# find the reports tab
reports_tab = driver.find_element(By.ID, "reportsMenu")
# click the reports tab
reports_tab.click()

# Wait for the page to load
driver.implicitly_wait(2)

# access submenus
# find the attendance tab
reports_menusub1 = driver.find_element(By.ID, "reportsMenuSub1")
reports_menusub1.click()

# consecutive absences report
consecutive_absence_report = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[2]/td/div/table[2]/tbody/tr[1]/td[2]/table[1]/tbody/tr/td[3]/div[2]/table/tbody/tr[7]/td[3]/div/table/tbody/tr[8]/td[2]")
consecutive_absence_report.click()
# Wait for the page to load
driver.implicitly_wait(5)

'''
==================== MODAL WINDOW ====================
'''
# Wait for the new window to appear
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

# Get all window handles
window_handles = driver.window_handles

# Switch to the new window (assuming it’s the second one)
driver.switch_to.window(window_handles[-1])

# Wait for the modal to be visible
WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, 'popupWindow'))
)
# wait for it to be clickable
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/table'))
)
# this opens a modal window with options
# element of table containing options
table = driver.find_element(By.CLASS_NAME, "detailContainer")
# start date
start_date = driver.find_element(By.ID, "parametersAsStrings(startDate)")
#start_date = driver.find(By.XPATH, "/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td/div/table/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input")
# remove the default date
start_date.clear()
# enter the date
start_date.send_keys("08/28/2024")
# end date
end_date = driver.find_element(By.ID, "parametersAsStrings(endDate)")
# remove the default date
end_date.clear()
# Get today's date in the required format
today_date = datetime.today().strftime('%m/%d/%Y')
end_date.send_keys(today_date)
print(today_date)

# absences options
absences_operator = driver.find_element(By.NAME, "parametersAsStrings(count)")
# remove the default value
absences_operator.clear()
# enter the value of num absences, putting 4
absences_operator.send_keys("4")
# print(absences_operator.text)
# print(absences_operator.get_attribute("value"))



'''
==================== OPTIONS ====================
can do TARDIES, etc. with CONNECTORS like AND & OR
can also output as csv rather than html or pdf
right now all this is set by default to all students
'''

'''
==================== SUBMIT ====================
'''
# run_button = driver.find_element(By.ID, "okButton")
# wait for it to be clickable

# print(driver.find_element(By.TAG_NAME, "button").find_element(By.CLASS_NAME, "button-text").outerHTML) 
ok_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@tabindex="99"]'))
)

ok_button.click()

time.sleep(40)  # Increase the wait time if the PDF takes longer to download

pdf_url = driver.current_url

# Check if URL is pointing to a PDF file
if pdf_url.endswith(".pdf"):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        # Save the PDF to a file
        with open("output.pdf", "wb") as f:
            f.write(response.content)
        print("PDF saved as output.pdf")



print(f"PDF should be downloaded to: {download_dir}")

driver.quit()
