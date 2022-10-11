import pikepdf

print('=' * 80)
print(">> 此為PDF密碼解除程式(需密碼)")
password = input(">> 請輸入接下來的PDF檔案密碼: ")
while True:
    filename = input("\n>> 請輸入完整PDF檔案路徑與名稱(找不到檔案將結束程式): ")
    try:
        file = pikepdf.open(filename, password=password, allow_overwriting_input=True)
    except:
        break
    file.save(filename)
    print(">> Success")

input(">> 按下Enter鍵結束程式...")
print('=' * 80)
exit()
