#by EEGuizhi

import time
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
import msvcrt
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def start_program(): #開始的輸出
    print('#by EEGuizhi')
    print('=========================================================================')
    print('>> Program has started ',time.strftime(" %I:%M:%S %p", time.localtime()))

def end_program(): #結束的輸出
    try:
        driver.quit()
    finally:
        print('\n>> Program has ended ',time.strftime(" %I:%M:%S %p", time.localtime()))
        print('=========================================================================')
        input()
        exit()

def pw_input(): #密碼輸入, 輸入完會變為'*'
    chars = []
    while True:
        newChar = msvcrt.getch().decode(encoding="utf-8")
        if newChar in '\r\n': # 如果是換行，則輸入結束
            break
        elif newChar == '\b': # 如果是退格，則刪除密碼末尾一位並且刪除一個星號
            if chars:
                del chars[-1]
                print('\b', end='', flush=True)
                print(' ', end='', flush=True)
                print('\b', end='', flush=True)
        else:
            print(newChar,end='',flush=True)
            # print('*',end='',flush=True)
            chars.append(newChar)
    return (''.join(chars))

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

def connect_nchu(): #進入興大入口網頁
    print('\n>> 正在連線興大入口..')
    try:
        driver.get("https://portal.nchu.edu.tw/portal/")
    except:
        print('>> 連線興大入口失敗...')
        return 1
    return 0

def login(user_id, password): #在興大入口網頁進行登入動作
    print('\n>> 輸入帳號密碼並登入', time.strftime(" %I:%M:%S %p", time.localtime()))
    try:
        element = driver.find_element("name",value="Ecom_User_ID")
        element.send_keys(user_id)
        element = driver.find_element("name",value="Ecom_Password")
        element.send_keys(password)
    except:
        return 1
    try:
        driver.execute_script("console.log(code);")
        for entry in driver.get_log('browser'):
            if entry['level'] == "INFO":  # ex: {'level': 'INFO', 'message': 'console-api 2:32 "6LYE"'}
                verify_code = entry['message'][-5:-1]
        element = driver.find_element("id",value="inputCode")
        element.send_keys(verify_code)
    except:
        return 1
    try:
        element = driver.find_element("id",value="login_btn") #點擊登入
    except:
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
            element = soup.find('button', string='登入') #用文字搜尋
            element = driver.find_element("xpath",value=xpath_soup(element))
        except:
            return 1
    element.click()
    return 0

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

def main(user_id, password, class_id, amount): #微型通識主要部分
    failed = connect_nchu() #連到興大入口
    if failed == 1:
        return 1
    print('>> 連線興大入口成功 待至12:28分後登入') #待至12:28 PM
    print('>> 開始時間:', time.strftime(" %I:%M:%S %p", time.localtime()))
    waiting('p', 12, 28)

    login(user_id, password) #登入興大入口(失敗的話就是已登入)
    try:
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=enro_main')
        # link = driver.find_element_by_link_text("選課") #找到選課網址
        # driver.get(link.get_attribute('href')) #連到選課網址
    except:
        print('\n>> 登入錯誤') #無法找到'選課'按鈕
        return 1
    try:
        print('\n>> 連到微型通識選課主畫面') #跳到微型通識選課畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/cah_main')
    except:
        print('\n>> 連到微型通識選課主畫面錯誤..')
        return 1
    print('\n>> 等待12:30:00 PM 刷新頁面') 
    waiting('p', 12, 30) #待至12:30:00 PM
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 跳到微型課程加選畫面')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        option = soup.find('font', string='課程加選')
        option = option.find_parent().find_parent()
        driver.get('https://onepiece2-sso.nchu.edu.tw'+option["href"]) #連到微型課程加選畫面
    except:
        try:
            option = soup.find('font', string='課程加選')
            element = driver.find_element("xpath",value=xpath_soup(option))
            element.click()
        except:
            try:
                driver.refresh()
                soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
                option = soup.find('font', string='課程加選')
                element = driver.find_element("xpath",value=xpath_soup(option))
                element.click()
            except:
                print('>> 跳到微型課程加選畫面錯誤..')
                return 1
    try:
        print('\n>> 將要選的課程打勾 並按下 "確認選取"')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        for i in range(0, amount):
            print('>> class id =', class_id[i])
            try:
                checkbox = soup.find('td', string=class_id[i]).find_parent()
                checkbox = checkbox.find('input', type="checkbox")
                element = driver.find_element("xpath",value=xpath_soup(checkbox))
                element.click()
            except:
                print('>> 找尋不到此課程課號')
        try:
            button = soup.find('input', value="確認選取")
            element = driver.find_element("xpath",value=xpath_soup(button))
            element.click()
        except:
            print('>> exe button = soup.find(\'input\', value="確認選取") failed')
            button = soup.find('input', type="submit")
            element = driver.find_element("xpath",value=xpath_soup(button))
            element.click()
    except:
        print('>> 課程打勾並按下"確認選取" 錯誤..')
        return 1
    try:
        print('\n>> 按下 "是，確認加選"')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        button = soup.find('input', value="是，確認加選")
        element = driver.find_element("xpath",value=xpath_soup(button))
        element.click()
    except:
        try:
            print('>> exe button = soup.find(\'input\', value="是，確認加選") failed')
            button = soup.find('input', type="submit")
            element = driver.find_element("xpath",value=xpath_soup(button))
            element.click()
        except:
            print('>> 按下"是，確認加選" 錯誤..')
            return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    print('\n\n>> 選課結果:')
    for i in range(0, amount):
        try:
            text = soup.find('td', string=class_id[i]).find_parent().select('td')
        except:
            print('\n      找不到選課編號: ', class_id[i], ' (可能為搶課失敗, 請登入確認)')
        else:
            print('\n      選課編號: ', text[0].getText())
            print('      主題系列: ', text[1].getText())
            print('      單元名稱: ', text[2].getText())
            print('      課程期間: ', text[3].getText())
            print('      節次: ', text[4].getText())
            print('      地點: ', text[5].getText())
            print('      學習時數: ', text[6].getText())
            print('      授課教師: ', text[7].getText())
            print('      教材費: ', text[8].getText())
            print('      備註: ', text[9].getText())
    return 0

if __name__ == "__main__":
    start_program()
    
    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = { 'browser':'ALL' }
    
    options = webdriver.ChromeOptions()  # background execute webdriver
    options.add_argument('--headless')
    try:
        driver = webdriver.Chrome(desired_capabilities=d)  # start chrome
    except:
        print('\n>> 開啟webdriver失敗  請將chromedriver.exe放置與此程式同資料夾位置, 或者版本過舊需要更新')
        end_program()

    user_id = input('\n\n>> 請輸入興大入口帳號(學號): ')
    print('>> 請輸入興大入口密碼: ', end='', flush=True)
    password = pw_input()
    print('')

    class_id = ['', '', '']
    amount = 0
    while (amount < 1) or (amount > 3):
        amount = int(input('\n>> 請問您想選幾堂微型通識課(1~3)(註:每學期至多3堂): '))
    for i in range(0, amount):
        tmp = '>> 請輸入第 ' + str(i+1) + ' 門通識課程課號: '
        class_id[i] = input(tmp)

    run = 1
    count = 0
    while run == 1 and count < 3:
        print('>> ---------------------------------------- 第'+str(count+1)+'次執行 ----------------------------------------')
        run = main(user_id, password, class_id, amount)
        count += 1
    if run == 1 and count == 3:
        print('\n>> 執行失敗, 很抱歉')
    end_program()
