# EEGuizhi
import os
from misc import *
from verilog_parser import VerilogParser

PARSER_FILE = "Verilog_Debug/config.json"

if __name__ == "__main__":
    while True:
        # Read code
        code = input(">> Paste ur \"verilog code\" or file path of code here (\"exit\" to leave): \n")
        if code == "exit" or code == "Exit":
            end_program()
        elif os.path.exists(code):
            with open(code) as f:
                code = f.read()

        # Start parsing
        print("")
        parser = VerilogParser(PARSER_FILE)
        parser.parse_verilog_code(code)
        print("")
