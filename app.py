import sys
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By          # ★追加
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService  # ★追加

# ユーザー名とパスワード
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
    return driver.find_element(By.TAG_NAME, "body") is not None  # ★変更

# ★ ドライバのログを非表示にする設定（新しい書き方）
service = ChromeService(log_output=os.path.devnull)

chrome_options = Options()
# chrome_options.add_argument("--headless")

# ★ executable_path は不要。Selenium Managerが自動でChromeDriverを取得します
driver = webdriver.Chrome(service=service, options=chrome_options)

# 対象ページを読み込ませる。まずはログインページ。
driver.get("https://portal.e-staffing.ne.jp/client/mnu/creload/ja")
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# ★ find_element_by_xpath → find_element(By.XPATH, ...) に変更
username_field = driver.find_element(By.XPATH, USERNAME_XPATH)
username_field.send_keys(username)

password_field = driver.find_element(By.XPATH, PASSWORD_XPATH)
password_field.send_keys(password)

company_field = driver.find_element(By.XPATH, COMPANY_XPATH)
company_field.send_keys(company)

# 全部入力したら、画面遷移
driver.find_element(By.XPATH, LOGIN_XPATH).click()
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# 月次承認
time.sleep(SLEEP_TIME)
driver.find_element(By.XPATH, MONTHLY_APPROVAL).click()
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# 承認
driver.switch_to.window(driver.window_handles[1])
time.sleep(SLEEP_TIME)
driver.find_element(By.XPATH, ALL_CHECK).click()
driver.find_element(By.XPATH, APPROVAL).click()
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# 各自承認
time.sleep(SLEEP_TIME)
for i in range(20):
    CHECKBOX = '//*[@id="closestatus"]/div[1]/div[2]/div[' \
               + str(i + 1) + ']/div[1]/span/label/span[1]'
    try:
        driver.find_element(By.XPATH, CHECKBOX).click()
    except:
        break

if driver.find_element(By.XPATH, APPROVAL_ALL).is_enabled():
    driver.find_element(By.XPATH, APPROVAL_ALL).click()