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

USERNAME_XPATH = '/html/body/div/table/tbody/tr/td/form/table[2]/tbody/tr/td[1]/table[1]/tbody/tr/td/table[1]/tbody/tr[4]/td[3]/input'
PASSWORD_XPATH = '/html/body/div/table/tbody/tr/td/form/table[2]/tbody/tr/td[1]/table[1]/tbody/tr/td/table[1]/tbody/tr[6]/td[3]/input'
COMPANY_XPATH = '/html/body/div/table/tbody/tr/td/form/table[2]/tbody/tr/td[1]/table[1]/tbody/tr/td/table[1]/tbody/tr[2]/td[3]/input'
LOGIN_XPATH = '/html/body/div/table/tbody/tr/td/form/table[2]/tbody/tr/td[1]/table[1]/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/a/img'

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
driver.get("https://timecard2.e-staffing.ne.jp/000_002.cfm")
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

# HTML解析
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
tables = soup.findChildren('table', class_='cmTableDetail cmWidthP90 cmCenter')
# tables[0]
tbody = tables[0].find_all('tbody', recursive=False)
rows = tbody[0].find_all('tr', recursive=False)
# メンバー数は、len(rows) - 1

for i in range(len(rows)-1):
    # 承認ページへ。承認したものからなくなるため、最初のXPATHは固定
    MEMBER_XPATH = '/html/body/div[1]/div/form[1]/table[4]/tbody/tr[2]/td[9]/input'
    driver.find_element_by_xpath(MEMBER_XPATH).click()
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_is_loaded)

    # メンバーページ内HTML解析
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    tables = soup.findChildren('table', class_='cmTableDetail cmWidthP90')
    # tables[0]
    tbody = tables[0].find_all('tbody', recursive=False)
    rows = tbody[0].find_all('tr', recursive=False)

    for j in range(2, len(rows)+1):
        APPROVE_XAPTH = '/html/body/div[1]/table[8]/tbody/tr[' + str(j) + ']/td[13]/table/tbody/tr/td[1]/input'
        try:
            driver.find_element_by_xpath(APPROVE_XAPTH).click()
            # 承認するとポップアップが発生
            alert_obj = driver.switch_to.alert
            time.sleep(SLEEP_TIME)
            alert_obj.accept()
            time.sleep(SLEEP_TIME)
        except:
            print('Line ' + str(j) + ' failed.')

    APPROVE_CLOSE_XPATH = '/html/body/div[1]/form[2]/table[1]/tbody/tr[2]/td[9]/table/tbody/tr/td[1]/input'
    driver.find_element_by_xpath(APPROVE_CLOSE_XPATH).click()
    time.sleep(SLEEP_TIME)
    alert_obj.accept()
    time.sleep(SLEEP_TIME)

    RETURN_XPATH = '/html/body/div[1]/form[5]/table/tbody/tr/th/input'
    driver.find_element_by_xpath(RETURN_XPATH).click()
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_is_loaded)
