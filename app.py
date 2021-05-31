import sys
import os
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

# exeで配布するために、ユーザ名とパスワードは都度指定する形に
username = sys.argv[1]
password = sys.argv[2]
company = sys.argv[3]

USERNAME_XPATH = '//*[@id="userId"]'
PASSWORD_XPATH = '//*[@id="password"]'
COMPANY_XPATH = '//*[@id="companyId"]'
LOGIN_XPATH = '//*[@id="loginBtn"]'
MONTHLY_APPROVAL = '//*[@id="js-sort-task"]/li[2]/div/span/a'
ALL_CHECK = '//*[@id="paging"]/div[4]/ul/li[1]/label/span[1]'
APPROVAL = '//*[@id="approval-btn-top"]/a'
APPROVAL_ALL = '//*[@id="close-approval-btn-tooltip"]'

SLEEP_TIME = 5

def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


# ブラウザのドライバを読み込む。
# chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service_log_path=os.path.devnull,
                          executable_path='chromedriver.exe',)
                          # options=chrome_options)
# 対象ページを読み込ませる。まずはログインページ。
driver.get("https://portal.e-staffing.ne.jp/client/mnu/creload/ja")
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# 読み込んだら、find_element_by_xpathで指定して要素を取得し、入力を与える。
# あらかじめ、ブラウザにてwebページのソースを表示して、入力したいフォームなどのIDを探しておく。
username_field = driver.find_element_by_xpath(USERNAME_XPATH)
username_field.send_keys(username)

password_field = driver.find_element_by_xpath(PASSWORD_XPATH)
password_field.send_keys(password)

company_field = driver.find_element_by_xpath(COMPANY_XPATH)
company_field.send_keys(company)

# 全部入力したら、画面遷移
driver.find_element_by_xpath(LOGIN_XPATH).click()
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# 月次承認
time.sleep(SLEEP_TIME)
driver.find_element_by_xpath(MONTHLY_APPROVAL).click()
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# 承認
driver.switch_to.window(driver.window_handles[1])
time.sleep(SLEEP_TIME)
driver.find_element_by_xpath(ALL_CHECK).click()
driver.find_element_by_xpath(APPROVAL).click()
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# 各自承認
time.sleep(SLEEP_TIME)
for i in range(20):
    CHECKBOX = '//*[@id="closestatus"]/div[1]/div[2]/div[' + str(i + 1) + ']/div[1]/span/label/span[1]'
    try:
        driver.find_element_by_xpath(CHECKBOX).click()
    except:
        break

if driver.find_element_by_xpath(APPROVAL_ALL).is_enabled():
    driver.find_element_by_xpath(APPROVAL_ALL).click()

