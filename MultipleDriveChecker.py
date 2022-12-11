#EEGuizhi (Unfinished)

def start_program():  # 開始的輸出
    print('#by EEGuizhi')
    print('=========================================================================')
    print('>> Program has started \n')

def end_program():  # 結束的輸出
    print('\n>> Program has ended')
    print('=========================================================================')
    input()
    exit()

def error(text: str):  # 錯誤的輸出
    print('\n>>', text, '執行錯誤')
    end_program()


# Main block
if __name__ == '__main__':
    # 開啟檔案
    file = input('>> 請輸入Verilog檔的完整檔案名稱(需在同資料夾內): ')
    try:
        f = open(file, "r", encoding='utf8')
    except:
        error('檔案開啟失敗')

    # Init
    inAlways = 0
    inIfElse = 0
    inBeginEnd = 0
    var = []

    # 讀取資料
    begin_flag = False
    end_flag = False
    always_flag = False
    comment_flag = False
    prev_ch = ''

    line = f.readline()
    while line:
        var_ptr = 0
        for i in len(line):
            ch = line[i]
            
            # comment detect
            if (prev_ch+ch) == "//":
                break
            elif (prev_ch+ch) == "/*":
                comment_flag = True
                break
            if comment_flag:
                if (line[len[line]-2]+line[len[line]-1]) == "*/":
                    comment_flag = False
            
            # variable detect
            if (prev_ch+ch) == "<=" and inIfElse == 0:
                
            
            # check "begin"
            if begin_flag:
                if (prev_ch+ch) in "begin":
                    if ch == 'n' and (line[i+1] in ' /\n'):
                        inBeginEnd += 1
                else:
                    begin_flag = False
            else:
                if ch == 'b':
                    begin_flag = True

            # check "end"
            if end_flag:
                if (prev_ch+ch) in "end":
                    if (ch == 'd') and (line[i+1] in ' /\n'):
                        inBeginEnd -= 1
                else:
                    end_flag = False
            else:
                if ch == 'e':
                    end_flag = True

            # check "always"
            if always_flag:
                if (prev_ch+ch) in "always":
                    if ch == 's' and (line[i+1] in ' /\n'):
                        inAlways += 1
                else:
                    always_flag = False
            else:
                if ch == 'a':
                    always_flag = True

            # check "( )"
            if ch == '(':
                inIfElse += 1
            if ch == ')':
                inIfElse -= 1
                
            
            prev_ch = ch
        line = f.readline()
    f.close()
