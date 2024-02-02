# EEGuizhi

def end_program():
    print(f"\n>> Program ended.")
    exit()

def get_init_end_words(word_dict: dict) -> tuple:
    """
    Parameter:
    ---
        `word_dict` : keywords dictionary with `{init: end}` structure

    Return:
    ---
        `init_words, end_words` : lists of "init. keywords" & "end keywords"
    """
    return list(word_dict.keys()), list(word_dict.values())

def make_init_char_string(word_list: list) -> str:
    init_ch = ""
    for word in word_list:
        init_ch += word[0]
    return init_ch

def extract_words(string: str) -> list:
    """
    ignore space char, and save the words in string to list.

    Parameter
    ---
        `string` : input string

    Return:
    ---
        `list`: the words in string
    """
    split_words, words = string.split(' '), []
    for i in split_words:
        if i != '': words.append(i)
    return words

def get_longest_len(word_list: list) -> int:
    max = 0
    for word in word_list:
        max = len(word) if len(word) > max else max
    return max

def check_start_stage(
        pattern: str, stage: list,
        init_words: list, end_words: list,
        rd: int, st: int = 0
    ) -> tuple:
    for idx in range(len(init_words)):
        if pattern[0:len(init_words[idx])] == init_words[idx]:
            stage.append(init_words[idx])
            st = rd + len(init_words[idx])
            rd += len(init_words[idx]) - 1
            break
    return stage, rd, st, end_words[idx]

def check_end_stage():
    pass
