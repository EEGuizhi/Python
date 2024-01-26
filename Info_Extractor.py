# EEGuizhi
import os
import pandas as pd


CATCH_DATA = [  # 白落工作室白單
    "遊戲名稱",
    "購買商品",
    "推薦代理",
    "支付方式/時間",
    "總金額",
    "代儲 / 送"
]
STOP_CHAR = "▸\n"
MAX_LENGTH = 32
IGNORE_CHAR = " $："
IGNORE_STRING = [
    "（超代請自行+25手續費）",
    "（若無可不填寫）",
    "（限光遇）"
]
FILE = "result.csv"


def get_init_dict(fill_none:bool=True) -> dict:
    # Get new empty dictionary. (initialize according to "CATCH_DATA")
    d = {}
    if fill_none:
        for i in CATCH_DATA: d[i] = [None]
    else:
        for i in CATCH_DATA: d[i] = []
    return d


def write_data(dataframe:pd.DataFrame, data:dict, file_path:str=FILE) -> pd.DataFrame:
    # Concatenate "data" to "dataframe", save the dataframe as csv file & return new dataframe.
    dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)
    dataframe.to_csv(file_path, index=False, encoding='utf-8-sig')
    return dataframe


if __name__ == "__main__":
    # Initialization
    if os.path.exists(FILE):
        reply = None
        while(reply != "Y" and reply != "N"):
            reply = input(">> 目前已經存在 result.csv ，是否覆寫原本的檔案?(Y/N)：")
        if reply == "N":
            print(">> 程式已終止執行。")
            exit()
    dataframe = pd.DataFrame(get_init_dict(False))
    start_chars = [s[0] for s in CATCH_DATA]

    # Msg processing
    while(True):
        msg = input(">> 請輸入文字訊息：")
        data = get_init_dict()

        print("資料擷取中..")
        for read_idx in range(len(msg)):
            # Find
            if msg[read_idx] in start_chars:
                for key_str in CATCH_DATA:
                    if msg[read_idx] == key_str[0]:
                        if len(msg) - read_idx >= len(key_str) and msg[read_idx:read_idx+len(key_str)] == key_str:
                            stop_idx = read_idx + len(key_str)
                            while(stop_idx < len(msg) and stop_idx - read_idx <= MAX_LENGTH and msg[stop_idx] not in STOP_CHAR):
                                stop_idx += 1
                            save_str = msg[read_idx+len(key_str):stop_idx]
                            for c in IGNORE_CHAR:
                                save_str = save_str.replace(c, '')
                            for s in IGNORE_STRING:
                                save_str = save_str.replace(s, '')
                            data[key_str] = [save_str]
        print("資料擷取完畢..\n")

        # Write & Append
        dataframe = write_data(dataframe, data)
