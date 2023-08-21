#by EEGuizhi

import time
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
import msvcrt
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def start_program():
    print('=========================================================================')
    print('#by EEGuizhi')
    print('>> Program has started ',time.strftime(" %I:%M:%S %p", time.localtime()))

def end_program(msg:str=None):
    if msg is not None:
        print("\n>>", msg)
    print('\n>> Program has ended ',time.strftime(" %I:%M:%S %p", time.localtime()))
    print('=========================================================================')
    try:
        driver.quit()
    finally:
        input()
        exit()


def result(failed):
    if failed:
        print("\n>> END: 很抱歉這什麼破程式, 請將遇到的問題回報給我")
    else:
        print("\n>> END: 感謝使用, 如搶課未成功請見諒")


def pw_input():
    chars = []
    while True:
        newChar = msvcrt.getch().decode(encoding="utf-8")
        if newChar in '\r\n':  # 如果是換行，則輸入結束
            break
        elif newChar == '\b':  # 如果是退格，則刪除密碼末尾一位並且刪除一個星號
            if chars:
                del chars[-1]
                print('\b', end='', flush=True)
                print(' ', end='', flush=True)
                print('\b', end='', flush=True)
        else:
            print('*',end='',flush=True)
            chars.append(newChar)
    return (''.join(chars))


def xpath_soup(element):  # code from https://stackoverflow.com/questions/37979644/parse-beautifulsoup-element-into-selenium
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


def click_checkbox(str, soup:BeautifulSoup):
    checkbox = soup.find('td', string=str).find_parent()
    checkbox = checkbox.find('input', type="checkbox")
    element = driver.find_element("xpath", value=xpath_soup(checkbox))
    element.click()


def connect_nchu():
    print('\n>> 正在連線興大入口..')
    count = 0  # 連線興大入口
    while count < 3:
        try:
            driver.get("https://portal.nchu.edu.tw/portal/")  # 進入興大入口網頁
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
    # 連到興大入口
    if connect_nchu():
        end_program("無法連至興大入口")
    # 輸入帳密
    print('\n>> 輸入帳號密碼並登入', time.strftime(" %I:%M:%S %p", time.localtime()))
    try:
        element = driver.find_element("name",value="Ecom_User_ID")  # 帳號輸入
        element.send_keys(user_id)
        element = driver.find_element("name",value="Ecom_Password")  # 密碼輸入
        element.send_keys(password)
    except:
        return 1
    # 驗證碼
    try:
        driver.execute_script("console.log(code);")
        for entry in driver.get_log('browser'):
            if entry['level'] == "INFO":  # ex: {'level': 'INFO', 'message': 'console-api 2:32 "6LYE"'}
                verify_code = entry['message'][-5:-1]
        element = driver.find_element("id",value="inputCode")
        element.send_keys(verify_code)
    except:
        return 1
    # 點擊登入
    try:
        element = driver.find_element("id",value="login_btn")  # 點擊登入
    except:
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
            element = soup.find('button', string='登入')  # 用文字搜尋
            element = driver.find_element("xpath", value=xpath_soup(element))
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
    print("\n\n>> 請問您想執行以下哪一功能?")
    print(">> (1) 程式測試執行")
    print(">> (2) 體育課程 ---自動搶課")
    print(">> (3) 系所課程 ---自動搶課")
    print(">> (4) 外系課程 ---自動搶課")
    print(">> (5) 綜合課程 ---自動搶課")
    print(">> (6) 結束程式")
    option = 0
    while (option < 1) or (option > 6):
        option = int(input("請輸入選項(數字): "))
    return option

#------------------------------------------------------------------------------------------------------------------

def test_program():
    failed = connect_nchu()
    if failed:
        return 1
    print('>> 連線興大入口成功')
    login(user_id, password)
    driver.get("https://portal.nchu.edu.tw/portal/")
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
    soup = soup.find('ul', id="profile")
    username = soup.find('li').getText()
    print(f"\n>> 使用者{username}\n")
    return 0


def main_PE(num):
    try:
        print('\n>> 連到一般課程加選頁面')  # 跳到一般課程加選畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_nomo1_list')
    except:
        print('\n>> 連到一般課程加選頁面錯誤...')
        return 1
    print('\n>> 等待10:00:00 AM 刷新頁面')  # 10:00:00 AM 刷新頁面
    waiting('a', 10, 0)
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 跳到選體育課程的頁面')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        option = soup.find('font', string='體育課程')
        option = option.find_parent().find_parent()
        driver.get('https://onepiece2-sso.nchu.edu.tw'+option["href"])  # 連到體育課選課頁面
    except:
        print('\n>> 跳到選體育課程的頁面錯誤...')
        return 1
    try:
        print('\n>> 勾選體育課程')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        click_checkbox(num, soup)
    except:
        print('\n>> 勾選體育課程錯誤...')
        return 1
    try:
        print('\n>> 按下加選確定送出')
        button = soup.find('input', value="加選確定送出")
        element = driver.find_element("xpath", value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下加選確定送出錯誤...')
        return 1
    try:
        print('\n>> 按下是，確定加選')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element("xpath", value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下是，確定加選錯誤...')
        return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
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
        print('\n>> 連到一般課程加選頁面')  # 跳到一般課程加選畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_nomo1_list')
    except:
        print('\n>> 連到一般課程加選頁面錯誤..')
        return 1
    print('\n>> 等待10:00:00 AM 刷新頁面')  # 10:00:00 AM 刷新頁面
    waiting('a', 10, 0)
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 跳到選系所課程的頁面')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        option = soup.find('font', string='系所必選修課程')
        option = option.find_parent().find_parent()
        driver.get('https://onepiece2-sso.nchu.edu.tw'+option["href"])  # 連到選課頁面
    except:
        print('\n>> 跳到選系所課程的頁面錯誤...')
        return 1
    try:
        print('\n>> 勾選系所課程')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        for i in range(0, amount):
            click_checkbox(num[i], soup)
    except:
        print('\n>> 勾選系所課程錯誤...')
        return 1
    try:
        print('\n>> 按下加選確定送出')
        button = soup.find('input', value="加選確定送出")
        element = driver.find_element("xpath", value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下加選確定送出錯誤...')
        return 1
    try:
        print('\n>> 按下是，確定加選')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element("xpath", value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下 "是，確定加選" 錯誤...')
        return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
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
        print('\n>> 連到一般課程加選頁面')  # 直接跳到一般課程加選畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_nomo1_list')
    except:
        print('\n>> 連到一般課程加選頁面錯誤...')
        return 1
    print('\n>> 等待10:00:00 AM 刷新頁面')  # 10:00:00 AM 刷新頁面
    waiting('a', 10, 0)
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 選擇系所')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        select = Select(driver.find_element("name", value="v_sdept"))
        select.select_by_value(depart)  # 選擇系所
    except:
        print('\n>> 選擇系所錯誤...')
        return 1
    try:
        print('\n>> 勾選課程')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        click_checkbox(num)
    except:
        print('\n>> 勾選課程錯誤...')
        return 1
    try:
        print('\n>> 按下加選確定送出')
        button = soup.find('input', value="加選確定送出")
        element = driver.find_element("xpath", value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下加選確定送出錯誤...')
        return 1
    try:
        print('\n>> 按下是，確定加選')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element("xpath", value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下"是，確定加選"錯誤...')
        return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
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


def others(num):
    try:
        print('\n>> 連到一般課程加選頁面')  # 跳到一般課程加選畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_nomo1_list')
    except:
        print('\n>> 連到一般課程加選頁面錯誤..')
        return 1
    print('\n>> 等待10:00:00 AM 刷新頁面')  # 10:00:00 AM 刷新頁面
    waiting('a', 10, 0)
    print('\n>> 重整頁面...')
    driver.refresh()
    try:
        print('\n>> 跳到選系所課程的頁面')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        option = soup.find('font', string='其他課程')
        option = option.find_parent().find_parent()
        driver.get('https://onepiece2-sso.nchu.edu.tw'+option["href"])  # 連到選課頁面
    except:
        print('\n>> 跳到選系所課程的頁面錯誤...')
        return 1
    try:
        print('\n>> 勾選系所課程')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        click_checkbox(num, soup)
    except:
        print('\n>> 勾選系所課程錯誤...')
        return 1
    try:
        print('\n>> 按下加選確定送出')
        button = soup.find('input', value="加選確定送出")
        element = driver.find_element("xpath", value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下加選確定送出錯誤...')
        return 1
    try:
        print('\n>> 按下是，確定加選')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element("xpath", value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下 "是，確定加選" 錯誤...')
        return 1
    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
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
    # 選擇功能
    option = choosing()

    num = ['', '', '', '', '', '']  # 課號
    amount = 0
    if option == 1:  # 測試
        print("\n>> 開始執行測試")
        print(">> 成功的話下方會顯示你的名字")
        failed = test_program()
    elif option == 2:  # 體育
        num[0] = input('\n>> 請輸入想選的體育課程號碼: ')
    elif option == 3:  # 系內
        while (amount < 1) or (amount > 6):
            amount = int(input('\n>> 請問您想選幾堂系所課程(1~6): '))
        for i in range(0, amount):
            tmp = f">> 請輸入第 {i+1} 門系所課程課號: "
            num[i] = input(tmp)
    elif option == 4:  # 外系
        depart = input("\n>> 請輸入該課程所屬的系所代號(ex:U64F):")
        num[0] = input("\n>> 請輸入想選的課程號碼:")
    elif option == 5:
        print(">> 尚未完成此功能")
        return 0
    elif option == 6:  # 跳出main func迴圈
        return 1

    failed = connect_nchu()  # 連到興大入口
    if failed == 1:
        return 0

    print('>> 連線興大入口成功 待至9:58分登入')  # 等待到上午9:58分以後
    waiting('a', 9, 58)

    driver.refresh()
    login(user_id, password)  # 登入興大入口 (執行失敗基本上就是已登入)
    try:
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=enro_main')
    except:
        try:
            driver.get("https://portal.nchu.edu.tw/portal/")  # 進入興大入口網頁
            driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=enro_main')
        except:
            print('\n>> 登入錯誤或無法連線至選課頁面')
            return 0

    if option == 2:
        failed = main_PE(num[0])
    elif option == 3:
        failed = main_department(amount, num)
    elif option == 4:
        failed = other_department(depart, num[0])
    result(failed)


if __name__ == "__main__":
    start_program()

    # Enable browser logging
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'browser':'ALL'}

    options = webdriver.ChromeOptions()  # 背景執行webdriver
    options.add_argument('--headless')
 
    try:
        driver = webdriver.Chrome(chrome_options=options, desired_capabilities=d)  # 啟動chrome webdriver
    except:
        print('\n>> 開啟webdriver失敗, 請先安裝或更新Chrome Webdriver並與此程式放置在同個資料夾')
        end_program('')
    time.sleep(3)
    print("\n")

    # 使用者輸帳號、密碼
    user_id = input('\n\n>> 請輸入興大入口帳號(學號): ')
    print('>> 請輸入興大入口密碼: ', end='', flush=True)
    password = pw_input()
    print('')

    end = 0
    while end == 0:
        end = main(user_id, password)

    end_program()
