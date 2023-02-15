#by EEGuizhi

import time
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
import msvcrt
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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


def start_program():
    print('=========================================================================')
    print('# by EEGuizhi')
    print('>> Program has started ',time.strftime(" %I:%M:%S %p", time.localtime()))
    print('\n註: 此程式每間隔1秒會刷新一次頁面，重複確認您想選的課程是否有名額可選，並在可選時自動加選。\n\n')


def end_program(msg: str):
    if msg:
        print("\n>>", msg)
    print('\n>> Program has ended ',time.strftime(" %I:%M:%S %p", time.localtime()))
    print('=========================================================================')
    try:
        driver.quit()
    finally:
        input()
        exit()


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


def connect_nchu():
    print('\n>> 正在連線興大入口..')
    count = 0  # 計次
    while count < 3:
        try:
            driver.get("https://portal.nchu.edu.tw/portal/")  # 進入興大入口網頁
        except:
            print('>> 連線興大入口失敗...')
            time.sleep(3)
            count = count + 1
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
            element = driver.find_element("xpath",value=xpath_soup(element))
        except:
            return 1
    element.click()
    return 0

def final_step(num):
    try:
        print('\n>> 連到直接輸入課號加選畫面')  # 跳到直接輸入課號加選畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_direct1_list')
    except:
        print('\n>>連到直接輸入課號加選畫面錯誤...')
        return 1
    try:
        print('\n>> 輸入課號')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        option = soup.find('input', type="text")
        element = driver.find_element("xpath",value=xpath_soup(option))
        element.send_keys(num)
    except:
        print('\n>>輸入課號錯誤...')
        return 1
    try:
        print('\n>> 按下 確定送出')
        button = soup.find('input', value="確定送出")
        element = driver.find_element("xpath",value=xpath_soup(button))
        element.click()
    except:
        print('\n>>按下確定送出 錯誤...')
        return 1
    try:
        print('\n>> 將課程打勾')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        checkbox = soup.find('input', type="checkbox")
        element = driver.find_element("xpath",value=xpath_soup(checkbox))
        element.click()
    except:
        print('\n>>打勾課程錯誤...')
        return 1
    try:
        print('\n>> 按下"是，確定加選"')
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element("xpath",value=xpath_soup(button))
        element.click()
    except:
        print('\n>>按下「是，確定加選」錯誤...')
        return 1
    return 0

def main_class(num, user_id, password):
    try:
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=enro_main')
    except:
        try:
            driver.get("https://portal.nchu.edu.tw/portal/")  # 進入興大入口網頁
            driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=enro_main')
            # link = driver.find_element_by_link_text("選課")  # 找到選課網址
            # driver.get(link.get_attribute('href'))  # 連到選課網址
        except:
            print('\n>> 登入錯誤或無法連線至選課頁面')

    test = True
    try:
        element = driver.find_element("name",value="Ecom_User_ID")  # 帳號輸入
        element.send_keys(user_id)
        element = driver.find_element("name",value="Ecom_Password")  # 密碼輸入
        element.send_keys(password)
    except:
        test = False
    
    if test:
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
                element = driver.find_element("xpath",value=xpath_soup(element))
            except:
                return 1
        element.click()
        
    failed = final_step(num)
    if failed:
        failed_2 = final_step(num)
        if failed_2:
            end_program('很遺憾 程式出錯')

    print('\n>> 選課完畢 取得最後結果..')
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
    print('\n\n>> 選課結果:')
    try:
        text = soup.find('td', string=num).find_parent().select('td')
        print('\n      選課號碼: ', text[0].getText())
        print('      課程名稱: ', text[1].getText())
        print('      學分: ', text[4].getText())
        print('      授課教師: ', text[6].getText())
        print('      選課結果說明: ', text[7].getText())
    except:
        print('>> 很抱歉，加選錯誤或失敗。')
    end_program('')


def check_til_choose_able(group, num):
    try:
        print('\n>> 連到通識選課查詢畫面')  # 跳到通識查詢畫面
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/crseqry_gene_now')
    except:
        end_program('ERROR：連到通識選課查詢畫面錯誤...')
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        if group == 1:
            option = soup.find('option', string='人文領域')
        elif group == 2:
            option = soup.find('option', string='社會領域')
        elif group == 3:
            option = soup.find('option', string='自然領域')
        elif group == 4:
            option = soup.find('option', string='統合領域')
        element = driver.find_element("xpath",value=xpath_soup(option))
        element.click()
        button = soup.find('input', value='開始查詢')
        element = driver.find_element("xpath",value=xpath_soup(button))
        element.click()
    except:
        end_program('ERROR：選擇通識領域錯誤...')
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
        tmp = soup.find('a', string=num).find_parent().find_parent().select('td')
        print('\n>> 課程名稱:', tmp[5].getText())
    except:
        end_program('ERROR：找尋課程錯誤...')
    
    for i in range(25):  # 避免while Loop達到保護的上限而自動停止
        while True:
            time.sleep(1)  # 每隔1秒刷新一次頁面
            driver.refresh()
            soup = BeautifulSoup(driver.page_source, 'html.parser')  # 取得當前網頁原始碼
            try:
                tmp = soup.find('a', string=num).find_parent().find_parent().select('td')
                print('\r>> 開課人數:', tmp[12].getText(), '  目前人數:', tmp[13].getText(), end='')
                tmp = int(tmp[12].getText()) - int(tmp[13].getText())
                if tmp > 0:
                    print('\n>> 發現剩餘名額！ 即刻切換至選課頁面')
                    return 0
            except:
                return 1
            print('   time:', time.strftime(" %I:%M:%S %p", time.localtime()), end='')


if __name__ == "__main__":
    start_program()

    backgraound = None
    while backgraound!='Y' and backgraound!='N':
        backgraound = input(">> 請問您希望「是」在背景執行，還是「不是」在背景執行此程式呢？(輸入:Y/N) (註：兩者皆不會影響到你平常使用的瀏覽器):")

    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'browser':'ALL'}

    options = webdriver.ChromeOptions()
    if backgraound == 'Y':
        options.add_argument('--headless')  # 此行會背景執行webdriver
    try:
        driver = webdriver.Chrome(chrome_options=options, desired_capabilities=d)  # 啟動chrome webdriver
    except:
        print('\n>> 開啟webdriver失敗, 請先安裝或更新Chrome Webdriver並與此程式放置在同個資料夾')
        end_program('')
    time.sleep(3)
    print("\n")

    # 使用者輸入帳號、密碼
    user_id = input('\n\n>> 請輸入興大入口帳號(學號): ')
    print('>> 請輸入興大入口密碼: ', end='', flush=True)
    password = pw_input()
    print('')

    # 課號
    num = input('>> 請輸入通識課程課號: ')
    print('>> 輸入課號為"' + num + '"\n')
    group = 0
    while group < 1 or group > 4:
        group = int(input('>> 請問該課程的領域屬於 1.人文 2.社會 3.自然 4.統合 ?(輸入1~4):'))


    # 登入
    login(user_id, password)  # 登入興大入口 (執行失敗基本上就是已登入)
    try:
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=enro_main')
    except:
        end_program('ERROR：登入錯誤或無法連線至"選課"頁面')
    try:
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=crseqry_home')
    except:
        end_program('ERROR：無法連線至"課程查詢"頁面')


    check_til_choose_able(group, num)
    main_class(num, user_id, password)
    end_program('很遺憾 程式出錯..')
