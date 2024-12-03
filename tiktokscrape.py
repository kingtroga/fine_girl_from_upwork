import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import random
import time
from undetected_chromedriver.webelement import WebElement
from fake_useragent import UserAgent
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve session details
session_id = os.getenv("SESSION_ID")
executor_url = os.getenv("EXECUTOR_URL")


def type_with_delay(field: WebElement, text:str) -> None:
    for char in text:
        field.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # Delay between 50-200 ms per keystroke

if not session_id or not executor_url:
    raise EnvironmentError("SESSION_ID and EXECUTOR_URL must be set in the .env file")







WAIT = 10
email_address = "alice.starfruit59965"
password = "5L'QT@JoobG"
api_key = "sk-proj-2y0Am-zGhlgEZuknRY_AW-hT3XaA_F7Lk-OC6SbRvnPCnaLYx9pGR4oxFh-fpceuB7nY_86C4jT3BlbkFJ1rNkjPWrri-N3oFoQsjLgI_s7guD5KNo3QBOoW08vqWHgXlWFEtrtRQBdgHqJCdemopwCLvbMA"
# Endpoint for OpenAI Whisper
url = "https://api.openai.com/v1/audio/transcriptions"

# Set up browser
user_agent = UserAgent(fallback="Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36").random
options = Options()
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--disable-notifications")
driver = webdriver.Remote(command_executor=executor_url, options=options)
driver.session_id = session_id


# Login to TikTok
try:
    driver.get("https://www.tiktok.com/login")
    time.sleep(random.choice([10, 15, 12]))
    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Continue with Google']"))).click()
    main_window = driver.current_window_handle
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    popup_window = [handle for handle in driver.window_handles if handle != main_window][0]
    driver.switch_to.window(popup_window)
    account_xpath = f"//div[contains(@data-identifier, '{email_address}@gmail.com')]"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, account_xpath))).click()
    time.sleep(random.choice([2,8,5]))
    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Continue']"))).click()
    time.sleep(random.choice([2,8,5]))
    driver.switch_to.window(main_window)
    time.sleep(random.choice([10,8,15]))
except Exception as e:
    print("You are probably already logged in")
    pass
else:
    # Handling Robot check
    max_robot_fight = 30
    i = 0
    try:
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Audio']"))).click()
        while i < max_robot_fight:
            try:
                time.sleep(random.choice([10, 15, 12]))
                play_button = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Play']")))
                audio_element = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "audio")))
                audio_src = audio_element.get_attribute("src")
                audio_file_path = "audio.mp3"
                response = requests.get(audio_src)
                if response.status_code == 200:
                    with open(audio_file_path, "wb") as file:
                        file.write(response.content)
                    print("Audio file downloaded successfully.")
                else:
                    raise Exception(f"Failed to download audio. Status code: {response.status_code}")
                # Open the audio file and make a POST request
                with open(audio_file_path, "rb") as audio_file:
                    files = {"file": audio_file,}
                    data = {"model": "whisper-1","language": "en",}   
                    headers = {"Authorization": f"Bearer {api_key}"}
                    # Send the request to OpenAI API
                    response = requests.post(url, headers=headers, files=files, data=data)
                if response.status_code == 200:
                    transcription = response.json().get("text")
                    first_5_letters = ''.join(filter(str.isalpha, transcription))[:5].lower()
                else:
                    raise Exception(f"Error {response.status_code}: {response.text}")
                input_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter what you hear']")))
                play_button.click()
                time.sleep(random.choice([10, 15, 12]))
                play_button.click()
                time.sleep(random.choice([10, 15, 12]))
                type_with_delay(input_tag, first_5_letters)
                play_button.click()
                time.sleep(random.choice([10, 15, 12]))
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Verify']"))).click()
                time.sleep(random.choice([10, 15, 12]))

                try:
                    time.sleep(random.choice([10, 15, 12]))
                    search_box = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search']")))
                    print("TikTok didn't find out that we are bot😭🫱🏾‍🫲🏾")
                    break
                except:
                    time.sleep(random.choice([10, 15, 12]))
                    print("Trying to beat TikTok's robot check again")
                    i = i + 1
                    continue
            except Exception as e:
                print(f"Error Occured: {e}")
                print("Trying to beat TikTok's robot check again")
                i = i + 1
                continue
    except TimeoutException:
        print("TikTok didn't find out that we are bot😭🫱🏾‍🫲🏾")



# Assumming TikTok didn't flag us as a bot Get commentors
driver.get("https://www.tiktok.com/search?q=finance")
time.sleep(random.choice([10,15,8]))
time.sleep(WAIT * 6)
WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='search_top-item']"))).click()
time.sleep(WAIT * 6)
# Set to hold unique profile links
profile_links = set()
output_file = "profile_links.txt"
while True:
    # Find all currently loaded commenter profile links
    comments = driver.find_elements(By.XPATH, "//a[starts-with(@href, '/@') and .//span[starts-with(@data-e2e, 'comment-username-')]]")
    # Add profile links to the set
    for comment in comments:
        profile_links.add(comment.get_attribute("href"))
    
    # Scroll to the last comment to trigger loading more
    if comments:
        last_comment = comments[-1]
        ActionChains(driver).move_to_element(last_comment).perform()
        time.sleep(2)  # Allow time for new comments to load
    else:
        # Break if no comments are found (end of comments)
        break
    # Check if we have loaded 100 comments
    print(f"{len(comments)} Comments gotten")
    if len(profile_links) >= 100:  # 100 comments loaded
        break

with open(output_file, "w") as file:
    for link in profile_links:
        file.write(link + "\n")
print(f"Extracted {len(profile_links)} profile links and saved to '{output_file}'.")

# Go to commentors profiles
for profile_link in list(profile_links):
    driver.get(profile_link)
    time.sleep(random.choice([20, 15, 25]))


    operation = random.choice([1, 2])
    if operation == 1:
        driver.execute_script("window.scrollTo(0, 800)")
        time.sleep(random.choice([2,3,5]))
        driver.execute_script("window.scrollTo(0, 900)")
        time.sleep(random.choice([2,3,5]))
        driver.execute_script("window.scrollTo(0, 1000)")
        time.sleep(random.choice([2,3,5]))
        driver.execute_script("window.scrollTo(0, 1200)")
        time.sleep(random.choice([2,3,5]))
    else:
        driver.execute_script("window.scrollTo(0, 1000)")
        time.sleep(random.choice([2,3,5]))
        driver.execute_script("window.scrollTo(0, 0)")


print("Successfully Gone through 100 comments")