import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--mute-audio")

#_______________________________________________________________________________
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#_______________________________________________________________________________
DiscordEmail = "Put your email in here"                                  # Leave the quotes
DiscordPassword = "Put your DISCORD, not email, password in here"        # Leave the quotes
#_______________________________________________________________________________
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#_______________________________________________________________________________

urlInspire = "https://inspirobot.me/mindfulnessmode"
urlDiscord = 'https://discord.com/login'

driver = webdriver.Chrome(options=chrome_options)
driver.get(urlInspire)
main = driver.current_window_handle
driver.execute_script("window.open('about:blank', 'discord');")
driver.switch_to.window('discord')
driver.get(urlDiscord)


def WebWait(xpath, method,textInput=''):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    if method == 'click' :
        driver.find_element(By.XPATH, xpath).click()
    elif method == 'send_keys' :
        driver.find_element(By.XPATH, xpath).send_keys(textInput)
    
WebWait('/html/body/div[2]/div[2]/div/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/input', 'send_keys', DiscordEmail) # Put in Email
WebWait('/html/body/div[2]/div[2]/div/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[2]/div/input', 'send_keys', DiscordPassword) # Put in Password
WebWait('/html/body/div[2]/div[2]/div/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]', 'click') # Click Login

def changeStatus(newStatus):
    driver.switch_to.window('discord')

    WebWait('/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/section/div[2]/div[1]', 'click') # Click on Account Widget
    try: #Already a status
        WebWait('/html/body/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[3]/div[5]/div/div[1]/div[3]', 'click') # Open Status Window
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[2]/input')))
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[2]/input').clear()
    except: #No Status
        WebWait('/html/body/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[3]/div[4]/div/div[1]/div[3]', 'click')
        pass
    
    WebWait('/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[2]/input', 'send_keys', newStatus) # Set Status
    WebWait('/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div/div[3]/button[1]', 'click') # Confirm Status
    driver.switch_to.window(main)

driver.switch_to.window(main)

driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div').click()

block1 = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]')
block2 = driver.find_element(By.XPATH, '/html/body/div[2]/div[6]')

quote1 = block1.get_attribute('textContent').replace("\n", "") 
quote2 = block2.get_attribute('textContent').replace("\n", "") 

print(block1.value_of_css_property('display'))

counter1 = 1
counter2 = 1

time.sleep(5)
while(True):
    if  block1.value_of_css_property('display') != "block" and counter1 == 0:
        quote1 = block1.get_attribute('textContent').replace("\n", "")
        print(quote1)
        if len(quote1) <= 128: changeStatus(quote1)
        counter1 += 1
    elif block2.value_of_css_property('display') != "block" and counter2 == 0:
        quote2 = block2.get_attribute('textContent').replace("\n", "")
        print(quote2)
        if len(quote2) <= 128: changeStatus(quote2)
        counter2 += 1
    elif block1.value_of_css_property('display') != "none":
        counter1 = 0
    elif block2.value_of_css_property('display') != "none":
        counter2 = 0
    time.sleep(15)
    pass
