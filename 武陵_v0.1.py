#by Guizhi

import time
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import msvcrt


def start_program(): #開始的輸出
    print("#Made by EEGuizhi")
    print("=========================================================================")
    print(">> Program has started ",time.strftime(" %I:%M:%S %p", time.localtime()))
    print('>> 此程式之功能為「在早上8:30到時，自動至武陵農場官網訂房"賓館四人房"」 請注意程式執行時仍需人為操作謝謝。')

def end_program(): #結束的輸出
    try:
        driver.quit()
    finally:
        print('\n>> Program has ended ',time.strftime(" %I:%M:%S %p", time.localtime()))
        print('=========================================================================')
        input()
        exit()


def xpath_soup(element): #code from https://stackoverflow.com/questions/37979644/parse-beautifulsoup-element-into-selenium
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def waiting(M, h, m): #等待至某時刻的迴圈
    if M == 'a' or M == 'A' or M == 'am' or M == 'AM':
        M = 'AM'
    else:
        M = 'PM'
    if h == 12:
        h = 0
    while True:
        meridiem = time.strftime("%p", time.localtime())
        hr = time.strftime("%I", time.localtime())
        if int(hr) == 12:
            hr = 0
        min = time.strftime("%M", time.localtime())
        if meridiem == M:
            if int(hr) == int(h):
                if int(min) >= int(m):
                    return 0
            elif int(hr) > int(h):
                return 0


def selectDate():
    print("")
    
    year = input(">> 請輸入想選擇的年份(Ex: 2023) : ")
    while year > 2030 or year < 2022:
        year = input(">> 無效的輸入 請輸入西元年份(Ex: 2023) : ")
        
    month = input(">> 請輸入想選擇的月份(Ex: 11) : ")
    while month > 12 or month < 1:
        month = input(">> 無效的輸入 請輸入數字月份(Ex: 11) : ")
    
    date = input(">> 請輸入想選擇的日期(Ex: 28) : ")
    while date < 1 or date > 31:
        month = input(">> 無效的輸入 請輸入數字日期(Ex: 28) : ")
    
    return year, month, date


if __name__ == "__main__" :
    start_program()
    
    select_year, select_month, select_date = selectDate()
    
    options = webdriver.ChromeOptions()  # background execute webdriver
    try:
        driver = webdriver.Chrome()  # start chrome
    except:
        print('\n>> 開啟webdriver失敗  請將chromedriver.exe放置與此程式同資料夾位置, 或者版本過舊需要更新')
        end_program()
    
    driver.get("https://wulingfarm.ezhotel.com.tw/user/login")  # 進入武陵國民賓館網頁
    time.sleep(5)
    input("\n\n>> 請您先手動進行登入  登入完畢後回來此視窗按下Enter以繼續執行... ")
    driver.get("https://wulingfarm.ezhotel.com.tw/1/room/list")  # 進入訂房網頁
    
    ## 等待至8:30 ==========
    try:
        pass
    except:
        pass
    
    ## 選擇房間部分 ==========
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        element = soup.find("h2", string="賓館四人房(二大床或一大床＋二小床)").find_parent().find_parent().find("a", string=" 訂 房 ")  # 用文字搜尋房間種類
        driver.find_element("xpath",value=xpath_soup(element)).click()
    except:
        print("\n\n>> Wrong: 選擇入住房間失敗")
        end_program()
    
    ## 選擇日期部分 ==========
    try:
        i = 0
        while i < 12:
        #     soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
            
        #     month = soup.find("select", {"class": "pika-select-month"}).find_parent()
        #     year = soup.find("select", {"class": "pika-select-year"}).find_parent()
            
        #     flag = True
        #     for n in range(len(select_month)):
        #         if month.text[n] != select_month[n] or year.text[3] != select_year[3]:
        #             flag = False
        #             break
            
        #     if flag:
        #         break
            
        #     element = soup.find("button", string="下個月")
        #     element = driver.find_element("xpath",value=xpath_soup(element)).click()
            i += 1
        
        # soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        # element = soup.find("button", {"class": "pika-day", "data-pika-year": select_year, "data-pika-day": str(select_date)})
        # element = driver.find_element("xpath",value=xpath_soup(element)).click()
        
        # driver.find_element("id", value="fast-booking-form-submit").click()
    except:
        print("\n\n>> Wrong: 選擇入住日期失敗")
        end_program()


    input("\n\n>> 請按下3次Enter以關閉Webdriver瀏覽器...")
    input()
    input()
    end_program()

# element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("id", "datepicker-check-in")))
        # try:
        #     time.sleep(0.5)
        #     element.click()
        # except:
        #     time.sleep(0.25)
        #     element.click()
