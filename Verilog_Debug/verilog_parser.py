# EEGuizhi
import json
from syntax_check import SyntaxChecker
from variable_check import VariableChecker
from synthesis_check import SynthesisChecker


class VerilogParser:
    def __init__(self, path: str):
        """
        Parameters
        ---
            `path`: the file path of "parse_verilog.json"
        """
        # read file
        with open(path) as f:
            config = json.load(f)

        # checker
        self.stx = SyntaxChecker(config)
        self.var = VariableChecker(config)
        self.syn = SynthesisChecker(config)

    def code_simplifier(self, code: str) -> str:
        # preprocess
        code = self.stx.remove_comment(code)
        code = self.stx.replace_define(code)
        
        return code

    def parse_verilog_code(self, code:str):
        """
        Parameters
        ---
            `code`: verilog code
        """
        code = self.code_simplifier(code)
        print(code)
