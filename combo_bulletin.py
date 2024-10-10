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
from datetime import datetime

load_dotenv()
ASPEN_URL=os.getenv("ASPEN_URL")
LOGIN_ID = os.getenv("LOGIN_ID")
PASSWORD = os.getenv("PASSWORD")

download_dir = os.path.join(os.getcwd(), "downloads/combo")  # Downloads to the "downloads" folder in your project
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,  # Set the download directory
    "download.prompt_for_download": False,       # Disable download prompts
    "plugins.always_open_pdf_externally": True   # Download PDFs instead of opening in the browser
}
chrome_options.add_experimental_option("prefs", prefs)

# Instantiate the driver with the defined options
driver = webdriver.Chrome(options=chrome_options)
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

# ATTENDANCE BULLET REPORT
# ATTENDANCE BULLETIN HOUSE SORT #
combo_absence_report = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[2]/td/div/table[2]/tbody/tr[1]/td[2]/table[1]/tbody/tr/td[3]/div[2]/table/tbody/tr[7]/td[3]/div/table/tbody/tr[2]")
combo_absence_report.click()
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
# DEFAULT DATE IS TODAY, SO NO NEED TO CHANGE
# DEFAULT END DATE IS TODAY, SO NO NEED TO CHANGE

# NEED TO CHANGE SORING OPTION TO YOG
sorting_operator = driver.find_element(By.NAME, "parametersAsStrings(sort)")
Select(sorting_operator).select_by_value("1") # 1 = YOG

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

time.sleep(60)  # Increase the wait time if the PDF takes longer to download
# this "job" takes a while to run, so we need to wait for it to finish
# we can check if the "job" is done by checking if the URL is still the same
# if the URL changes, then the "job" is done
# if the URL is still the same, then the "job" is not done
# we can use a while loop to check if the URL is still the same

# Navigate to the "current jobs" page
driver.get("https://ma-swansea.myfollett.com/aspen/personalToolQueue.do")

try:
    # Wait for the table to show up with the jobs
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "jobGrid")))

    # Wait for the report status to change to "Finished (click to view)"
    finished_link = WebDriverWait(driver, 900).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Finished (click to view)')]"))
    )

    # Click the link to open the PDF in a new tab
    finished_link.click()

    # Wait for the new tab to open
    time.sleep(2)  # Allow some time for the new tab to open

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    # Wait for the PDF to load (or download, if automatic)
    time.sleep(5)  # Adjust this timing based on how long the PDF takes to load

    # At this point, the PDF is opened in the new tab.
    # You can now automate the download of the PDF depending on your environment
    # For example, save the PDF by interacting with the browser's download prompts (if necessary).
    pdf_url = driver.current_url

    # Check if URL is pointing to a PDF file
    if pdf_url.endswith(".pdf"):
        response = requests.get(pdf_url)
        if response.status_code == 200:
            # Save the PDF to a file
            with open("output.pdf", "wb") as f:
                f.write(response.content)
            print("PDF saved as output.pdf")
    print("PDF opened in new tab successfully!")
except TimeoutException:
    print("The operation timed out while waiting for the report to finish.")
except Exception as e:
    print(f"An error occurred: {e}")

# pdf_url = driver.current_url

# # Check if URL is pointing to a PDF file
# if pdf_url.endswith(".pdf"):
#     response = requests.get(pdf_url)
#     if response.status_code == 200:
#         # Save the PDF to a file
#         with open("output.pdf", "wb") as f:
#             f.write(response.content)
#         print("PDF saved as output.pdf")



print(f"PDF should be downloaded to: {download_dir}")

driver.quit()
