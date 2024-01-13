import random
import time

ANS_PRON = False  # True: 顯示假名答案為發音, False: 顯示發音答案為假名
INTERVAL = 2.5  # seconds

if __name__ == "__main__":
    while True:
        katakana = {
            # "ア": "a",
            # "イ": "i",
            # "ウ": "u",
            # "エ": "e",
            # "オ": "o",
            # "カ": "ka",
            # "キ": "ki",
            "ク": "ku",
            "ケ": "ke",
            "サ": "sa",
            "シ": "shi",
            "ス": "su",
            "セ": "se",
            "ソ": "so",
            # "タ": "ta",
            "チ": "chi",
            # "ツ": "tsu",
            "テ": "te",
            "ト": "to",
            # "ナ": "na",
            "ニ": "ni",
            "ヌ": "nu",
            "ネ": "ne",
            # "ノ": "no",
            "ハ": "ha",
            "ヒ": "hi",
            "フ": "fu",
            # "ヘ": "he",
            "ホ": "ho",
            "マ": "ma",
            "ミ": "mi",
            "ム": "mu",
            # "メ": "me",
            "モ": "mo",
            # "ヤ": "ya",
            # "ユ": "yu",
            "ヨ": "yo",
            "ラ": "ra",
            # "ル": "ru",
            "レ": "re",
            "ロ": "ro",
            "ワ": "wa",
            "ヲ": "wo",
            # "ン": "n",
        }

        katakana_flipped = {v: k for k, v in katakana.items()}
        if not ANS_PRON:
            katakana = katakana_flipped

        keys = list(katakana.keys())
        random.shuffle(keys)

        print(">> 開始練習！")
        for i in range(len(keys)):
            current_key = keys[i]
            print(f"片假名: {current_key}")
            time.sleep(INTERVAL)  # 等待一點時間
            print(f"答案: {katakana[current_key]}\n")
        print("已顯示完所有片假名。\n")
