import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import random
import time
from undetected_chromedriver.webelement import WebElement
from dotenv import load_dotenv, set_key
import os

# Load or create .env file
env_file = ".env"
if not os.path.exists(env_file):
    open(env_file, "w").close()
load_dotenv(env_file)

# Function to type with delay
def type_with_delay(field: WebElement, text: str) -> None:
    for char in text:
        field.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # Delay between 50-200 ms per keystroke

# Constants
WAIT = 10
email_address = "alice.starfruit59965"
password = "5L'QT@JoobG"

# Set up browser
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-blink-features=AutomationControlled")

# Start driver
driver = uc.Chrome(options=options)
driver.delete_all_cookies()

# Save session details to .env
set_key(env_file, "SESSION_ID", driver.session_id)
set_key(env_file, "EXECUTOR_URL", driver.command_executor._url)

print("Saved session details to .env")

# Login to Google
print(f"##### Login Attempt #######")
driver.get(r"https://accounts.google.com/signin/v2/identifier?hl=tr&passive=true&continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dgoogle&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
time.sleep(random.choice([10, 8, 15]))

try:
    # Enter email
    login = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    type_with_delay(login, email_address)
    time.sleep(random.choice([10, 8, 15]))
    WebDriverWait(driver, WAIT).until(
        EC.element_to_be_clickable((By.ID, "identifierNext"))
    ).click()
    time.sleep(random.choice([10, 8, 15]))

    # Enter password
    password_tag = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )

    type_with_delay(password_tag, password)
    time.sleep(random.choice([10, 8, 15]))
    WebDriverWait(driver, WAIT).until(
        EC.element_to_be_clickable((By.ID, "passwordNext"))
    ).click()
    time.sleep(random.choice([10, 8, 15]))

    # Check if login is successful
    time.sleep(WAIT)
    if "search?q=google" in driver.current_url:
        print("########## Login passed ##########")
        input("Press Enter to close driver....")
    else:
        print("########## Login Failed ##########")
        quit()

except TimeoutException as e:
    print(f"Login process failed: {e}")
    driver.quit()
    quit()
