from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# other necessary ones
import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import time
import re
import datetime
import random

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

content_list = []
time_list = []
name_list = []
reaction_list = []
comment_list = []
share_list = []


browser = webdriver.Firefox()
browser.get("http://facebook.com")
browser.maximize_window()
wait = WebDriverWait(browser, 30)
email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
email_field.send_keys('959777459151')
pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
pass_field.send_keys('@@11542!')
pass_field.send_keys(Keys.RETURN)
time.sleep(30)

def click_see_more():
    retries = 0
    max_retries = 3  # Set a max retry limit to avoid infinite loops
    while retries < max_retries:
        try:
            see_more_buttons = browser.find_elements(By.XPATH, "//div[contains(text(), 'See more') and contains(@class, 'x1i10hfl')]")
            if not see_more_buttons:
                print("No more 'See More' buttons to click.")
                break  # Exit if no more "See More" buttons found

            for button in see_more_buttons:
                # Scroll the "See More" button into view
                browser.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(5)  # Allow time for scrolling and content to load

                # Attempt to click the button
                try:
                    browser.execute_script("arguments[0].click();", button)
                    time.sleep(5)  # Allow time for content to load after clicking
                    retries = 0  # Reset retries on success
                except Exception as e:
                    print(f"Error clicking a 'See More' button: {e}")
                    retries += 1
                    if retries >= max_retries:
                        print("Max retries reached for clicking 'See More'. Moving on.")
                        break  # Exit the function after max retries

        except Exception as e:
            print("Error finding 'See More' buttons:", e)
            break

def slow_scroll_page_mod():
    last_height = browser.execute_script("return document.body.scrollHeight")
    retries_scroll = 0
    max_retries_scroll = 10  # Number of retries to attempt if no new content is loaded

    while True:
        # Scroll by a smaller, possibly random value to more closely imitate normal user behavior
        scroll_distance =  100 # Random scroll distance between 100 and 500 pixels
        browser.execute_script(f"window.scrollBy(0, {scroll_distance});")
        
        # Randomize wait time to simulate more human-like pauses
        time.sleep(random.uniform(1.5, 3.5))

        click_see_more()  # Attempt to click "See More" buttons

        # Wait for any dynamic content to load
        time.sleep(10)  # Adjust sleep time based on observation of the site's load time

        new_height = browser.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            retries_scroll += 1
            if retries_scroll >= max_retries_scroll:
                print("Reached the bottom of the page or no new content loaded after several retries.")
                break  # Break the loop if we've retried the max number of times without new content
            else:
                print(f"No new content loaded, retrying... ({retries_scroll}/{max_retries_scroll})")
                # Wait a bit longer before retrying, with a slightly randomized wait time
                time.sleep(random.uniform(3, 5))
        else:
            last_height = new_height
            retries_scroll = 0 

browser.get('https://www.facebook.com/VoiceofMyanmarNews') # once logged in, free to open up any target page
time.sleep(5)
slow_scroll_page_mod()

soup = bs(browser.page_source,'html.parser')
all_posts = soup.find_all('div',{'class':'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z'})

for post in all_posts:
    try:
        name = post.find('a',{"class":"x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"}).text
    except:
        name = 'not_found'
            
    print(name)

    try:
        content = post.find('span',{"class":"x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"}).text
    except:
        content = 'not_found'
    print(content)

    try:
        date = post.find('a',{"class":"x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"}).text
    except:
        date = 'not_found'
    print(date)
    try:
        reaction = post.find('span',{'class':'xt0b8zv x2bj2ny xrbpyxo xl423tq'}).text
    except:
        reaction = 'not_found'
    print(reaction)
    try:
        comment_share = post.find_all('span', class_='x193iq5w')
        comment = "No comments found."
        share = "No shares found."

        # Process only if comment_share elements are found
        if comment_share:
            for element in comment_share:
                text = element.text.lower()
                if "comments" in text:
                    comment = element.text  # Found the comments
                elif "shares" in text:
                    share = element.text  # Found the shares

    except Exception as e:
        print(f'Failed processing post : {e}')
    print(comment)
    print(share)
    content_list.append(content)
    time_list.append(date)
    name_list.append(name)
    reaction_list.append(reaction)
    comment_list.append(comment)
    share_list.append(share)
    df = pd.DataFrame({"name":name_list,"content":content_list,"time":time_list,"reaction":reaction_list,"comment":comment_list,"share":share_list})
    df.drop_duplicates(subset="content",keep="first",inplace=True)
    df.to_csv("myanmar_voice2.csv")

