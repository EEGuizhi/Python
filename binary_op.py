# EEGuizhi
"""
This is a simple tool for binary operations in Python,
and binary number will be implemented with integer numpy array.
"""
import numpy as np

# Defualt settings
WIDTH = 16

class binary:
    def __init__(self, value = None, width = WIDTH, signed = True, fixed_point = 0) -> None:
        """Declare a binary variable.

        Parameters :
        ---
            `value` : the value of the variable, the type of this can be `float`, `int` for setting
                the value in decimal format, or `np.ndarray` in binary, `str` in hexadecimal.
            `width` : the width of the variable.
            `signed` : `True` for signed, `False` for unsigned.
            `fixed_point` : the index of 2^0 digit in binary format.
        """
        self.width = width
        self.signed = signed
        self.fixed_point = fixed_point
        if value == None:
            self.dec, self.bin = None, None
        else:
            self.__eq__(value)


    def __call__(self, format = "bin") -> np.array:
        """return the value of variable in binary format (numpy array).
        
        Parameter :
        ---
        `format` : must be "bin" or "dec"
        """
        if format == "bin":
            return self.bin
        elif format == "dec":
            return self.dec
        else:
            raise ValueError("The format must be \"bin\" (binary) or \"dec\" (decimal). ")


    def __eq__(self, __value) -> bool:
        if type(__value) == float or type(__value) == int:
            self.bin = dec2bin(__value, width=self.width, fixed_point=self.fixed_point, signed=self.signed)
            self.dec = bin2dec(self.bin, fixed_point=self.fixed_point, signed=self.signed)
        elif type(__value) == np.ndarray:
            self.bin = __value
            self.dec = bin2dec(__value, fixed_point=self.fixed_point, signed=self.signed)
        elif type(__value) == str:
            self.dec = hex2dec(__value, width=self.width, signed=self.signed)
            self.bin = hex2bin(__value, width=self.width)
        else:
            return False
        return True


    def __str__(self) -> str:
        return binary_string(self.bin)


    def __round__(self, width) -> float:
        return binary_round(self.bin, width=width)


def full_add(a: bool, b: bool, c: bool) -> tuple:
    """Act like a full adder, need intput (1bit)`a`, (1bit)`b` and (1bit)`c`.
    
    Returns:
    ---
        tuple: (carry: bool, sum: bool)
    """
    return (a&b | c&(b|a), a ^ b ^ c)


def binary_add(num1: np.ndarray, num2:np.ndarray, width: int = None) -> np.ndarray:
    if width == None: width = num1.shape[0]
    carry, sum = 0, np.zeros(width, dtype=int)
    for i in range(width):
        carry, sum[i] = full_add(num1[i], num2[i], carry)
    return sum


def binary_mult(num1: np.ndarray, num2: np.ndarray, width: int = WIDTH) -> np.ndarray:
    # init
    a = np.zeros(width, dtype=int) if num1[-1] == 0 else np.ones(width, dtype=int)
    b = np.zeros(width, dtype=int) if num2[-1] == 0 else np.ones(width, dtype=int)
    a[:num1.shape[0]] = num1
    b[:num2.shape[0]] = num2

    # mult
    sum = np.zeros(width, dtype=int)
    for i in range(width):
        if b[i] == 1:
            tmp = np.zeros(width, dtype=int)
            tmp[i:] = a[:width - i] if i != width - 1 else binary_2s_comp(a[:width - i])
            sum = binary_add(sum, tmp)

    return sum


def binary_2s_comp(num: np.ndarray) -> np.ndarray:
    return binary_add(binary_inv(num), dec2bin(1, num.shape[0]), num.shape[0])


def binary_inv(num: np.ndarray) -> np.ndarray:
    val = num.copy()
    for i in range(val.shape[0]):
        val[i] = 0 if val[i] == 1 else 1
    return val


def binary_round(num: np.ndarray, width: int) -> np.ndarray:
    """`width`: new width of the number"""
    binary = num[width - 1:].copy()
    return binary_add(binary, dec2bin(1, width)) if num[width] == 1 else binary


def dec2bin(num: float, width: int = WIDTH, fixed_point: int = 0, signed = True) -> np.ndarray:
    if num < 0 and not signed: raise ValueError("num cannot be a negative value")
    val, binary = abs(num), np.zeros(width, dtype=int)
    idx = width - 2 if signed else width - 1
    while idx >= 0:
        power = idx - fixed_point
        if val >= 2**power:
            binary[idx] = 1
            val -= 2**power
        idx -= 1
    return binary if num > 0 else binary_2s_comp(binary)


def bin2dec(num: np.ndarray, fixed_point: int = 0, signed: bool = True) -> float:
    width = num.shape[0]
    binary = binary_2s_comp(num) if num[width - 1] == 1 and signed else num
    value = 0
    for i in range(binary.shape[0]):
        value += 2**(i - fixed_point) if binary[i] == 1 else 0
    return (-1) * value if num[width - 1] == 1 and signed else value


def hex2bin(hex_str: str, width: int = WIDTH) -> np.ndarray:
    """Turn a hexadecimal(0~F) string into binary number np array"""
    length, binary = len(hex_str), np.zeros(width, dtype=int)
    if width < length * 4: raise ValueError("width is not match with the hex_str")
    for i in range(length):
        if hex_str[length - i - 1] == '0':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 0, 0, 0, 0
        elif hex_str[length - i - 1] == '1':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 0, 0, 0, 1
        elif hex_str[length - i - 1] == '2':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 0, 0, 1, 0
        elif hex_str[length - i - 1] == '3':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 0, 0, 1, 1
        elif hex_str[length - i - 1] == '4':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 0, 1, 0, 0
        elif hex_str[length - i - 1] == '5':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 0, 1, 0, 1
        elif hex_str[length - i - 1] == '6':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 0, 1, 1, 0
        elif hex_str[length - i - 1] == '7':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 0, 1, 1, 1
        elif hex_str[length - i - 1] == '8':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 1, 0, 0, 0
        elif hex_str[length - i - 1] == '9':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 1, 0, 0, 1
        elif hex_str[length - i - 1] in 'Aa':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 1, 0, 1, 0
        elif hex_str[length - i - 1] in 'Bb':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 1, 0, 1, 1
        elif hex_str[length - i - 1] in 'Cc':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 1, 1, 0, 0
        elif hex_str[length - i - 1] in 'Dd':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 1, 1, 0, 1
        elif hex_str[length - i - 1] in 'Ee':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 1, 1, 1, 0
        elif hex_str[length - i - 1] in 'Ff':
            binary[i*4 + 3], binary[i*4 + 2], binary[i*4 + 1], binary[i*4] = 1, 1, 1, 1
        else:
            print(f"hex_str[{length} - {i} - 1] = '{hex_str[length - i - 1]}'", end='')
            raise ValueError("Not a hexadecimal number")
    return binary


def hex2dec(hex_str: str, width: int = WIDTH, fixed_point: int = 0, signed: bool = True) -> int:
    return bin2dec(hex2bin(hex_str, width), fixed_point=fixed_point, signed=signed)


def print_bin(num: np.ndarray, end: str = '\n'):
    """Print a binary number"""
    print(binary_string(num), end=end)


def binary_string(num: np.ndarray):
    """Turn a binary number np array into a string"""
    string = ""
    for i in range(num.shape[0]):
        if i % 4 == 0 and i != 0: string = '_' + string
        string = '1' + string if num[i] else '0' + string
    return string
