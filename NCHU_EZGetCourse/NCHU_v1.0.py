#by EEGuizhi (未修正驗證碼部分)

import time
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
import msvcrt
from selenium.webdriver.support.ui import Select

def start_program():
    print('#by EEGuizhi')
    print('=========================================================================')
    print('>> Program has started ',time.strftime(" %I:%M:%S %p", time.localtime()))
    print('\n註: 此程式除"體育"以外之搶課功能皆僅為特定人服務, 請見諒\n\n ')

def end_program():
    print('\n>> Program has ended ',time.strftime(" %I:%M:%S %p", time.localtime()))
    print('=========================================================================')
    try:
        driver.quit()
    finally:
        input()
        exit()

def result(failed):
    if failed:
        print('\n>> END: 很抱歉這什麼破程式, 請將問題回報作者')
    else:
        print('\n>> END: 感謝使用, 如搶課未成功請見諒')

def sendback(soup, str, checkbox):
    try:
        element = soup.find('span', string=str).find_parent().find_parent().find_parent() #用文字搜尋
        element = element.find('div', role="radio")
        element = driver.find_element_by_xpath(xpath_soup(element))
        element.click()
    except:
        return 1
    try:
        for i in checkbox:
            element = soup.find('span', string=i).find_parent().find_parent().find_parent() #用文字搜尋
            element = element.find('div', role="checkbox")
            element = driver.find_element_by_xpath(xpath_soup(element))
            element.click()
    except:
        return 1
    try:
        element = soup.find('span', string='提交') #用文字搜尋
        element = driver.find_element_by_xpath(xpath_soup(element))
        element.click()
    except:
        return 1
    return 0

def pw_input():
    chars = []
    while True:
        newChar = msvcrt.getche().decode(encoding="utf-8")
        if newChar in '\r\n': # 如果是換行，則輸入結束
            break
        elif newChar == '\b': # 如果是退格，則刪除密碼末尾一位並且刪除一個星號
            if chars:
                del chars[-1]
                print(' ', end='', flush=True)
                print('\b', end='', flush=True)
        else:
            chars.append(newChar)
    print('>> 請輸入興大入口密碼: ', end='', flush=True)
    for i in range(0, len(''.join(chars))):
        print('*', end='', flush=True)
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

def click_checkbox(str, soup):
    checkbox = soup.find('td', string=str).find_parent()
    checkbox = checkbox.find('input', type="checkbox")
    element = driver.find_element_by_xpath(xpath_soup(checkbox))
    element.click()

def connect_nchu():
    print('\n>> 正在連線興大入口..')
    count = 0 #連線興大入口
    while count < 3:
        try:
            driver.get("https://portal.nchu.edu.tw/portal/") #進入興大入口網頁
        except:
            print('>> 連線興大入口失敗...')
            time.sleep(3)
            count = count+1
        else:
            break
    if count >= 3:
        return 1
    return 0

def login(user_id, password):
    print('\n>> 輸入帳號密碼並登入', time.strftime(" %I:%M:%S %p", time.localtime()))
    try:
        element = driver.find_element_by_name("Ecom_User_ID") #帳號輸入
        element.send_keys(user_id)
        element = driver.find_element_by_name("Ecom_Password") #密碼輸入
        element.send_keys(password)
    except:
        return 1
    try:
        verify_code = "console.log(code);"
        verify_code = driver.execute_script(verify_code)
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
            element = driver.find_element_by_xpath(xpath_soup(element))
        except:
            return 1
    element.click()
    return 0

def waiting(M, h, m):
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
            if int(min) >= int(m):
                if int(hr) >= int(h):
                    break

def choosing():
    print('\n\n>> 請問您想執行以下哪一功能?')
    print('>> (1) 程式測試執行')
    print('>> (2) 一般通識 ---自動搶課')
    print('>> (3) 微型通識 ---自動搶課')
    print('>> (4) 體育課程 ---自動搶課')
    print('>> (5) 系所課程 ---自動搶課')
    print('>> (6) 外系課程 ---自動搶課')
    print('>> (7) 結束程式')
    option = 0
    while (option < 1) or (option > 7):
        option = int(input('請輸入選項(數字): '))
    return option

def confirm_name():
    namelist = ['姓名：陳柏翔', '姓名：黃鈺雯', '姓名：詹皓暐', '姓名：陳昱翰', '姓名：張宸']
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    soup = soup.find('ul', id="profile")
    username = soup.find('li').getText()
    i = 1
    for user in namelist:
        if user == username:
            break
        i += 1
    if i == len(namelist)+1:
        return 0
    return i

def check_time():
    print('\n>> 確認選課時間...')
    driver.get("https://docs.google.com/forms/d/1SyBdPDQHheTE1NkGFfnNAj-_k-salY5MFlGlHnNQ7tI/viewform?edit_requested=true")
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    text = soup.find('meta', itemprop='description')
    edtion = []
    i = 0
    for char in text["content"]: #確認版本
        if i == 8 or i == 9 or i == 18:
            edtion.append(char)
        if i == 18:
            break
        i += 1
    if edtion[0] != '0' or edtion[1] != '1': #版本不正確
        print('>> 此版本已無法使用')
        return 1
    if edtion[2] != 'T':
        print('>> [提醒] 最近不是選課時間哦(作者有設置正確的話) 您仍可繼續執行但結果可能會錯誤')
        input('\n>> 按Enter繼續執行')
    print('>> 已確認')
    return 0
#------------------------------------------------------------------------------------------------------------------

def test_program():
    failed = connect_nchu()
    if failed == 1:
        return 1
    print('>> 連線興大入口成功')
    login(user_id, password)
    try:
        driver.find_element_by_link_text("選課") #找到選課網址
    except:
        print('\n>> 登入錯誤')
        return 1
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    soup = soup.find('ul', id="profile")
    username = soup.find('li').getText()
    print('\n>> 使用者'+username)
    UserID = confirm_name()
    if UserID == 0:
        print('>> 您不屬於服務範圍內, 但仍可使用體育搶課功能')
    else:
        print('>> 您在服務範圍內')
    try:
        print('\n>> 回報測試')
        driver.get("https://docs.google.com/forms/d/1SyBdPDQHheTE1NkGFfnNAj-_k-salY5MFlGlHnNQ7tI/viewform?edit_requested=true")
    except:
        return 1
    checkboxlist = ['選項 1', '選項 7'] #1 0001 010
    if UserID >= 8:
        UserID -= 8
        checkboxlist.append('選項 2')
    if UserID >= 4:
        UserID -= 4
        checkboxlist.append('選項 3')
    if UserID >= 2:
        UserID -= 2
        checkboxlist.append('選項 4')
    if UserID >= 1:
        UserID -= 1
        checkboxlist.append('選項 5')
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    failed = sendback(soup, 'Success', checkboxlist)
    return failed

def main_general(amount, num):
    try:
        print('\n>> 連到通識選課主畫面') #直接跳到通識選課主畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/gned_main')
    except:
        print('\n>> 連到通識選課主畫面錯誤...')
        return 1
    print('\n>> 等待10:00:00 AM 刷新頁面') #10:00:00 AM 刷新頁面
    waiting('a', 10, 0)
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 跳到通識加選的頁面')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        option = soup.find('span', string='Course Add')
        element = driver.find_element_by_xpath(xpath_soup(option))
        element.click()
    except:
        print('\n>> 按下 跳到通識加選的頁面錯誤...')
        return 1
    try:
        print('\n>> 按下 勾選加選課程')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        button = soup.find('input', value="勾選加選課程")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下勾選加選課程 錯誤...')
        return 1
    try:
        print('\n>> 將要選的課程打勾')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        for i in range(0, amount):
            click_checkbox(num[i], soup)
    except:
        print('\n>> 打勾要選的課程錯誤...')
        return 1
    try:
        print('\n>> 按下 下一步 ： 加選確認')
        button = soup.find('input', value="下一步 ： 加選確認")
    except:
        print('\n>> 按下 下一步 ： 加選確認錯誤...')
        return 1
    element = driver.find_element_by_xpath(xpath_soup(button))
    element.click()
    try:
        print('\n>> 按下 是，確定加選')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下 是，確定加選錯誤...')
        return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    print('\n\n>> 選課結果:')
    for i in range(0, amount):
        text = soup.find('td', string=num[i]).find_parent().select('td')
        print('\n      選課號碼: ', text[0].getText())
        print('      109前入學 領域/學群: ', text[1].getText(), '/', text[2].getText())
        print('      110後入學 領域/學群: ', text[3].getText(), '/', text[4].getText())
        print('      課程名稱: ', text[5].getText())
        print('      學分: ', text[6].getText())
        print('      授課教師: ', text[7].getText())
        print('      開課人數: ', text[10].getText())
        print('      選課人數: ', text[11].getText())
        print('      候補人數: ', text[12].getText())
        print('      選課結果說明: ', text[13].getText())
    return 0

def main_micro(amount, num):
    try:
        print('\n>> 連到微型通識選課主畫面') #直接跳到微型通識選課畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/cah_main')
    except:
        print('\n>> 連到微型通識選課主畫面錯誤..')
        return 1
    print('\n>> 等待至12:30:00 PM 刷新頁面') #12:30:00 PM 刷新頁面
    waiting('p', 12, 30)
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 跳到微型課程加選畫面')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        option = soup.find('font', string='課程加選')
        option = option.find_parent().find_parent()
        driver.get('https://onepiece2-sso.nchu.edu.tw'+option["href"]) #連到微型課程加選畫面
    except:
        option = soup.find('font', string='課程加選')
        element = driver.find_element_by_xpath(xpath_soup(option))
        element.click()
    try:
        print('\n>> 將要選的課程打勾 並按下"確認選取"')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        for i in range(0, amount):
            click_checkbox(num[i], soup)
        button = soup.find('input', value="確認選取")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 課程打勾並按下"確認選取" 錯誤..')
        return 1
    try:
        print('\n>> 按下 "是，確認加選"')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        button = soup.find('input', value="是，確認加選")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下"是，確認加選" 錯誤..')
        return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    print('\n\n>> 選課結果:')
    for i in range(0, amount):
        try:
            text = soup.find('td', string=num[i]).find_parent().select('td')
        except:
            print('\n      找不到選課編號: ', num[i], ' (可能為搶課失敗, 請登入確認)')
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

def main_PE(num):
    try:
        print('\n>> 連到一般課程加選頁面') #直接跳到一般課程加選畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_nomo1_list')
    except:
        print('\n>> 連到一般課程加選頁面錯誤...')
        return 1
    print('\n>> 等待10:00:00 AM 刷新頁面') #10:00:00 AM 刷新頁面
    waiting('a', 10, 0)
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 跳到選體育課程的頁面')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        option = soup.find('font', string='體育課程')
        option = option.find_parent().find_parent()
        driver.get('https://onepiece2-sso.nchu.edu.tw'+option["href"]) #連到體育課選課頁面
    except:
        print('\n>> 跳到選體育課程的頁面錯誤...')
        return 1
    try:
        print('\n>> 勾選體育課程') #打勾checkboxes
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        click_checkbox(num, soup)
    except:
        print('\n>> 勾選體育課程錯誤...')
        return 1
    try:
        print('\n>> 按下加選確定送出')
        button = soup.find('input', value="加選確定送出")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下加選確定送出錯誤...')
        return 1
    try:
        print('\n>> 按下是，確定加選')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下是，確定加選錯誤...')
        return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    text = soup.find('td', string=num).find_parent().select('td')
    print('\n\n>> 選課結果:')
    print('\n      選課號碼: ', text[0].getText())
    print('      課程名稱: ', text[1].getText())
    print('      必選修系所: ', text[2].getText())
    print('      全/半: ', text[3].getText())
    print('      學分: ', text[4].getText())
    print('      必/選: ', text[5].getText())
    print('      授課教師: ', text[6].getText())
    print('      選課結果: ', text[7].getText())
    return 0

def main_department(amount, num):
    try:
        print('\n>> 連到一般課程加選頁面') #直接跳到一般課程加選畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_nomo1_list')
    except:
        print('\n>> 連到一般課程加選頁面錯誤...')
        return 1
    print('\n>> 等待10:00:00 AM 刷新頁面') #10:00:00 AM 刷新頁面
    waiting('a', 10, 0)
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 跳到選系所課程的頁面')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        option = soup.find('font', string='系所必選修課程')
        option = option.find_parent().find_parent()
        driver.get('https://onepiece2-sso.nchu.edu.tw'+option["href"]) #連到選課頁面
    except:
        print('\n>> 跳到選系所課程的頁面錯誤...')
        return 1
    try:
        print('\n>> 勾選系所課程') #打勾checkboxes
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        for i in range(0, amount):
            click_checkbox(num[i], soup)
    except:
        print('\n>> 勾選系所課程錯誤...')
        return 1
    try:
        print('\n>> 按下加選確定送出')
        button = soup.find('input', value="加選確定送出")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下加選確定送出錯誤...')
        return 1
    try:
        print('\n>> 按下是，確定加選')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下"是，確定加選"錯誤...')
        return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    for i in range(0, amount):
        text = soup.find('td', string=num[i]).find_parent().select('td')
        print('\n\n>> 選課結果:')
        print('\n      選課號碼: ', text[0].getText())
        print('      課程名稱: ', text[1].getText())
        print('      必選修系所: ', text[2].getText())
        print('      全/半: ', text[3].getText())
        print('      學分: ', text[4].getText())
        print('      必/選: ', text[5].getText())
        print('      授課教師: ', text[6].getText())
        print('      選課結果: ', text[7].getText())
    return 0

def other_department(depart, num):
    try:
        print('\n>> 連到一般課程加選頁面') #直接跳到一般課程加選畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_nomo1_list')
    except:
        print('\n>> 連到一般課程加選頁面錯誤...')
        return 1
    print('\n>> 等待10:00:00 AM 刷新頁面') #10:00:00 AM 刷新頁面
    waiting('a', 10, 0)
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 選擇系所')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        select = Select(driver.find_element_by_name('v_sdept'))
        select.select_by_value(depart) #選擇系所
    except:
        print('\n>> 選擇系所錯誤...')
        return 1
    try:
        print('\n>> 勾選課程') #打勾checkboxes
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        click_checkbox(num)
    except:
        print('\n>> 勾選課程錯誤...')
        return 1
    try:
        print('\n>> 按下加選確定送出')
        button = soup.find('input', value="加選確定送出")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下加選確定送出錯誤...')
        return 1
    try:
        print('\n>> 按下是，確定加選')
        soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element_by_xpath(xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下"是，確定加選"錯誤...')
        return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser') #取得當前網頁原始碼
    text = soup.find('td', string=num).find_parent().select('td')
    print('\n\n>> 選課結果:')
    print('\n      選課號碼: ', text[0].getText())
    print('      課程名稱: ', text[1].getText())
    print('      必選修系所: ', text[2].getText())
    print('      全/半: ', text[3].getText())
    print('      學分: ', text[4].getText())
    print('      必/選: ', text[5].getText())
    print('      授課教師: ', text[6].getText())
    print('      選課結果: ', text[7].getText())
    return 0

def main(user_id, password):
    option = choosing()
    num = ['', '', '', '', '', ''] #課號
    amount = 0
    if option == 1: #測試程式
        print('\n>> 開始執行測試')
        failed = test_program()
        if failed:
            print('\n>> 測試執行失敗')
        else:
            print('\n>> 測試執行成功')
        return 0
    elif option == 2: #輸入通識課號
        while (amount < 1) or (amount > 4):
            amount = int(input('\n>> 請問您想選幾堂一般通識課(1~4)(註:超過4堂會無法加選): '))
        for i in range(0, amount):
            tmp = '>> 請輸入第 ' + str(i+1) + ' 門通識課程課號: '
            num[i] = input(tmp)
    elif option == 3: #輸入微型通識課號
        while (amount < 1) or (amount > 3):
            amount = int(input('\n>> 請問您想選幾堂微型通識課(1~3)(註:每學期至多3堂): '))
        for i in range(0, amount):
            tmp = '>> 請輸入第 ' + str(i+1) + ' 門通識課程課號: '
            num[i] = input(tmp)
    elif option == 4: #輸入體育課號
        num[0] = input('\n>> 請輸入想選的體育課程號碼: ')
    elif option == 5: #輸入系所課號
        while (amount < 1) or (amount > 6):
            amount = int(input('\n>> 請問您想選幾堂系所課程(1~6): '))
        for i in range(0, amount):
            tmp = '>> 請輸入第 ' + str(i+1) + ' 門系所課程課號: '
            num[i] = input(tmp)
    elif option == 6:
        depart = input("\n>> 請輸入該課程所屬的系所代號(ex:U64F):")
        num[0] = input("\n>> 請輸入想選的課程號碼:")
    elif option == 7: #跳出main func的迴圈
        return 1

    failed = connect_nchu() #連到興大入口
    if failed == 1:
        return 0

    if option == 2 or option == 4 or option == 5 or option == 6:
        print('>> 連線興大入口成功 待至9:58分登入') #等待到上午9:58分以後
        waiting('a', 9, 58)
    elif option == 3:
        print('>> 連線興大入口成功 待至12:28分以後登入') #等待到下午12:28分以後
        waiting('p', 12, 28)

    driver.refresh()
    login(user_id, password) #登入興大入口 (執行失敗基本上就是已登入)
    try:
        link = driver.find_element_by_link_text("選課") #找到選課網址
    except:
        print('\n>> 登入錯誤') #登入失敗(找不到'選課'按鈕)
        return 0
    success = confirm_name()
    if (option == 2 and success == 0) or (option == 3 and success == 0):
        print('\n>> 此功能不在服務範圍內')
        return 0
    driver.get(link.get_attribute('href')) #連到選課網址

    if option == 2:
        failed = main_general(amount, num)
    elif option == 3:
        failed = main_micro(amount, num)
    elif option == 4:
        failed = main_PE(num[0])
    elif option == 5:
        failed = main_department(amount, num)
    elif option == 6:
        failed = other_department(depart, num[0])
    result(failed)
    return 0

# MAIN
if __name__ == "__main__":
    start_program()

    options = webdriver.ChromeOptions() #背景執行webdriver
    options.add_argument('--headless')
    try:
        #driver = webdriver.Chrome(chrome_options=options) #啟動chrome 背景執行
        driver = webdriver.Chrome() #啟動chrome
    except:
        print('\n>> 開啟webdriver失敗, 請安裝或更新ChromeDriver並與此程式放置於同個資料夾')
        end_program()

    time.sleep(3)
    user_id = input('\n\n>> 請輸入興大入口帳號(學號): ') #使用者輸入帳號、密碼
    print('>> 請輸入興大入口密碼: ', end='', flush=True)
    password = pw_input()
    print('')

    end = 0
    end = check_time() #確認版本與時間
    while end == 0:
        end = main(user_id, password)

    end_program()
