import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import random
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--mute-audio")

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

twoFA = False
signin = True

def twoFAFunc(INPUT):
    twoFA = INPUT
    if twoFA == True:
        code = ''

        root = tk.Tk()
        root.title('Please input a 2FA Authentication Code')
        canvas1 = tk.Canvas(root, width=400, height=300)
        canvas1.pack()
        codeElement = tk.Entry(root)
        canvas1.create_window(200, 140, window=codeElement)
        def Enter():
            code = codeElement.get()
            WebWait('/html/body/div[2]/div[2]/div/div[1]/div/div/div/form/div[2]/div[2]/div/div/input', 'send_keys', code)
            WebWait('/html/body/div[2]/div[2]/div/div[1]/div/div/div/form/div[2]/div[2]/button[1]', 'click')
            root.destroy()
            twoFA = False

        button1 = tk.Button(text='Enter', command = Enter)
        canvas1.create_window(200, 180, window=button1)
        root.mainloop()

        while not driver.current_url == 'https://discord.com/channels/@me' and twoFA:
            time.sleep(0.5)
            pass

config = tk.Tk()
config.title('Config')
config.geometry('250x200')

Check = tk.BooleanVar()
DiscordEmail = tk.StringVar()
DiscordPassword = tk.StringVar()

def SignIn():
    WebWait('/html/body/div[2]/div[2]/div/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/input', 'send_keys', DiscordEmail.get()) # Put in Email
    WebWait('/html/body/div[2]/div[2]/div/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[2]/div/input', 'send_keys', DiscordPassword.get()) # Put in Password
    WebWait('/html/body/div[2]/div[2]/div/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]', 'click') # Click Login
    twoFA = Check.get()
    config.destroy()
    signin = False
    twoFAFunc(twoFA)

checkBox = tk.Checkbutton(config, text="Two Factor Authentication", onvalue = True, offvalue = False, variable = Check)
checkBox.pack()
L1 = tk.Label(config, text="Discord Account Email: ")
L1.pack()
email = tk.Entry(config, textvariable = DiscordEmail)
email.pack()
L2 = tk.Label(config, text="Discord Account Password: ")
L2.pack()
password = tk.Entry(config, textvariable = DiscordPassword)
password.pack()
Enter = tk.Button(config, text="Enter", command = SignIn)
Enter.pack()

config.mainloop()


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
    time.sleep(30 + random.randint(-15,15))

driver.switch_to.window(main)

driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div').click()

block1 = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]')
block2 = driver.find_element(By.XPATH, '/html/body/div[2]/div[6]')

quote1 = block1.get_attribute('textContent').replace("\n", "") 
quote2 = block2.get_attribute('textContent').replace("\n", "") 

counter1 = 1
counter2 = 1

time.sleep(5)
while(True):
    if  block1.value_of_css_property('display') != "block" and counter1 == 0:
        quote1 = block1.get_attribute('textContent').replace("\n", "")
        print(f"{quote1} ||| at {time.localtime().tm_mon}/{time.localtime().tm_mday}  {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}")
        if len(quote1) <= 128: changeStatus(quote1)
        counter1 += 1
    elif block2.value_of_css_property('display') != "block" and counter2 == 0:
        quote2 = block2.get_attribute('textContent').replace("\n", "")
        print(f"{quote2} ||| at {time.localtime().tm_mon}/{time.localtime().tm_mday}  {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}")
        if len(quote2) <= 128: changeStatus(quote2)
        counter2 += 1
    elif block1.value_of_css_property('display') != "none":
        counter1 = 0
    elif block2.value_of_css_property('display') != "none":
        counter2 = 0
    pass
