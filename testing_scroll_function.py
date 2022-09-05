from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.action_chains import ActionChains


browser = webdriver.Firefox()

browser.get("https://wienerhaus.it/coupon-newsletter")


actions = ActionChains(browser)
# for _ in range(20):  # Adjust for how far down the page you want
#     actions.send_keys(Keys.ARROW_DOWN).perform()

actions.send_keys(Keys.END).perform()


input("Press Enter to continue...")
