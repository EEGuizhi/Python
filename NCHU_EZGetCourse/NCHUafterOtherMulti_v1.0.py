# EEGuizhi

import time
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
import msvcrt
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.request


def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False


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


def click_checkbox(class_id, soup:BeautifulSoup):
    try:
        checkbox = soup.find('td', string=class_id).find_parent()
        checkbox = checkbox.find('input', type="checkbox")
        element = driver.find_element("xpath", value=xpath_soup(checkbox))
        element.click()
    except:
        print(f">> 勾選課號 {class_id} 失敗")


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
        print('\n>> 連到直接輸入課號加選畫面')
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_direct1_list')
    except:
        print('\n>> 連到直接輸入課號加選畫面錯誤..')
        return 1
    try:
        print('\n>> 輸入課號')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        option = soup.find('input', type="text")
        element = driver.find_element("xpath",value=xpath_soup(option))
        element.send_keys(num)
    except:
        print('\n>>輸入課號錯誤..')
        return 1
    try:
        print('\n>> 按下 確定送出')
        button = soup.find('input', value="確定送出")
        element = driver.find_element("xpath",value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下確定送出 錯誤..')
        return 1
    try:
        print('\n>> 將課程打勾')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        checkbox = soup.find('input', type="checkbox")
        element = driver.find_element("xpath",value=xpath_soup(checkbox))
        element.click()
    except:
        print('\n>> 打勾課程錯誤..')
        return 1
    try:
        print('\n>> 按下"是，確定加選"')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        button = soup.find('input', value="是，確定加選")
        element = driver.find_element("xpath",value=xpath_soup(button))
        element.click()
    except:
        print('\n>> 按下「是，確定加選」錯誤..')
        return 1
    return 0


def main_class(num, user_id, password):
    try:
        driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=enro_main')
    except:
        try:
            driver.get("https://portal.nchu.edu.tw/portal/")  # 進入興大入口網頁
            driver.get('https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=enro_main')
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


def check_til_choose_able(class_id):
    try: driver.get("https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=enro_main")
    except: end_program("ERROR：登入錯誤或無法連線至\"選課\"頁面")

    try: driver.get("https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/acad_subpasschk1?v_subname=crseqry_home")
    except: end_program("ERROR：無法連線至\"課程查詢\"頁面")

    try: driver.get("https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/crseqry_all")
    except: end_program("ERROR：連到綜合課程查詢畫面錯誤...")

    print("")
    for iter in range(42):  # Advoid "while loop" reach auto protect upper bound then stop program, but Im not sure if this is working
        while True:
            time.sleep(0.5)
            for id in class_id:
                try:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    element = driver.find_element("name", value="v_crseno")
                    element.send_keys(id)
                    button = soup.find("input", value="開始查詢")
                    element = driver.find_element("xpath",value=xpath_soup(button))
                    element.click()
                except:
                    end_program("ERROR：選擇綜合課程錯誤...")

                try:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    tmp = soup.find('a', string=id).find_parent().find_parent().select('td')
                    print(f"\r>> 課程名稱: {tmp[2].getText()}  ", end='')
                except:
                    end_program(f"ERROR：找尋課程{id}錯誤...")

                try:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    tmp = soup.find('a', string=id).find_parent().find_parent().select('td')
                    print(f"開課人數: {tmp[15].getText()}  剩餘名額: {tmp[17].getText()}", end='')
                    tmp = int(tmp[17].getText())
                    if tmp > 0:
                        print(f"\n>> 發現課號{id}有剩餘名額！ 即刻切換至選課頁面")
                        return id
                except:
                    if connect():
                        end_program("ERROR：無法查詢課程名額")
                    else:
                        print("\n>> 網路斷線 等待網路恢復..")
                        while True:
                            time.sleep(2)
                            if connect():
                                login(user_id, password)
                                id = check_til_choose_able(class_id)
                                return id
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
        options.add_argument('--headless')
    options.add_argument("--log-level=3")
    try:
        driver = webdriver.Chrome(chrome_options=options, desired_capabilities=d)  # 啟動chrome webdriver
    except:
        print('\n>> 開啟webdriver失敗, 請先安裝或更新Chrome Webdriver並與此程式放置在同個資料夾')
        end_program('')
    time.sleep(3)
    print("\n")

    # 使用者輸入帳號、密碼
    user_id = input("\n\n>> 請輸入興大入口帳號(學號): ")
    print(">> 請輸入興大入口密碼: ", end='', flush=True)
    password = pw_input()
    print('')

    # 課號
    class_id = []
    print(f">> 以下可以輸入多堂課程編號進行搶課(or \"exit\" to leave)")
    while True:
        num = input(">> 請輸入課程課號: ")
        if num == "exit": break
        class_id.append(num)
    print(f'>> 輸入課號為 {class_id} \n')


    # 登入
    login(user_id, password)  # 登入興大入口 (執行失敗基本上就是已登入)

    class_id = check_til_choose_able(class_id)
    main_class(class_id, user_id, password)
