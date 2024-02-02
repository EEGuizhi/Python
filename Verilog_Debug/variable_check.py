# EEGuizhi
from misc import *

class VariableChecker:
    def __init__(self, data: dict):
        self.init_define, self.end_define = get_init_end_words(data["define"])
        self.init_para, self.end_para = get_init_end_words(data["para"])
        self.init_wire, self.end_wire = get_init_end_words(data["wire"])
        self.init_reg, self.end_reg = get_init_end_words(data["reg"])


    def get_parameter(self, code: str) -> dict:
        pass


    def get_nonused_var(self) -> dict:
        pass


    def get_reg(self) -> dict:
        pass


    def get_wire(self) -> dict:
        pass


class Variable:
    def __init__(
            self, name: str, var_type: str, IO: str = "internal",
            width: int = None, signed: bool = False
        ):
        self.name = name      # variable name
        self.type = var_type  # "parameter", "wire", "reg", 
        self.IO = IO          # "input", "output", "internal"
        self.width = width    # bit width
        self.signed = signed  # signed
        self.former = []
        self.behind = []
