# EEGuizhi
from misc import *

class SyntaxChecker:
    def __init__(self, data: dict):
        self.init_skip, self.end_skip = get_init_end_words(data["skip"])
        self.init_define, self.end_define = get_init_end_words(data["define"])

    def remove_comment(self, code: str) -> str:
        new_code = ""
        rd = 0
        stage = [""]
        while rd < len(code):
            if stage[-1] != "skip":  # reading code
                for i in range(len(self.init_skip)):
                    if code[rd:rd+len(self.init_skip[i])] == self.init_skip[i]:
                        stage.append("skip")
                        rd += len(self.init_skip[i]) - 1
                        end_word = self.end_skip[i]
                        break
                new_code += code[rd] if stage[-1] != "skip" else ''
                rd += 1
            elif code[rd:rd+len(end_word)] == end_word:  # reading comment (end)
                stage.pop()
                rd += len(end_word) if end_word != '\n' else 0
            else:  # reading comment (hasn't end)
                rd += 1
        return new_code

    def replace_define(self, code: str) -> dict:
        new_code = ""
        define_dict = {}

        rd, st = 0, 0
        stage = [""]
        while rd < len(code):
            if stage[-1] != "define":  # not doing define
                for i in range(len(self.init_define)):
                    if code[rd:rd+len(word)] == word:  # init
                        st = rd + len(word)
                        stage.append("define")
                        rd += len(word) - 1
            else:
                for word in self.end_define:
                    if code[rd:rd+len(word)] == word:  # end
                        # Extract
                        e = extract_words(code[st:rd-1])
                        define_dict[e[0]] = e[1]

                        doing_define = False
                        rd += len(word) - 1

