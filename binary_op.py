# EEGuizhi
"""
This is a simple tool for binary operations in Python,
and binary number will be implemented with integer numpy array.
"""
import numpy as np

# Defualt settings
WIDTH = 16

class binary:
    def __init__(self, value = None, width = WIDTH, signed = True, fixed_point = 0, prefix = False) -> None:
        """Declare a binary variable.

        Parameters :
        ---
            `value` : the value of the variable, type can be `binary`, `float`, `int`, `numpy.ndarray`, or `str`(hexadecimal).
            `width` : the width of the variable.
            `signed` : `True` for signed, `False` for unsigned.
            `fixed_point` : the index of 2^0 digit in binary format.
            `prefix` : if the string has the width prefix in front of the binary number.
        """
        self.__width = width
        self.__signed = signed
        self.__fixed_point = fixed_point
        self.__prefix = prefix
        if value == None:
            self.__dec, self.__bin = None, None
        else:
            self.set_value(value)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def signed(self) -> bool:
        return self.__signed

    @property
    def fixed_point(self) -> bool:
        return self.__fixed_point

    @property
    def dec(self) -> float:
        return self.__dec

    @property
    def bin(self) -> np.ndarray:
        return self.__bin

    @property
    def prefix(self) -> bool:
        return self.__prefix

    def __call__(self, format = "bin") -> np.array:
        """return the value of variable in binary format (numpy array).
        
        Parameter :
        ---
        `format` : must be "bin" or "dec"
        """
        if format == "bin":
            return self.__bin
        elif format == "dec":
            return self.__dec
        else:
            raise ValueError("The format must be `bin` (binary) or `dec` (decimal). ")

    def __str__(self) -> str:
        return binary_string(self.__bin, self.__prefix)

    def __round__(self, width: int) -> float:
        """Binary round, rounding the binary number into new"""
        return binary_round(self.__bin, width=width)


    @dec.setter
    def dec(self, value: float) -> None:
        if type(value) != float and type(value) != int: raise TypeError("Type of `dec` must be `float` or `int`")
        self.__bin = dec2bin(value, width=self.__width, fixed_point=self.__fixed_point, signed=self.__signed)
        self.__dec = bin2dec(self.__bin, fixed_point=self.__fixed_point, signed=self.__signed)

    @bin.setter
    def bin(self, value: np.ndarray) -> None:
        if type(value) != np.ndarray: raise TypeError("Type of `bin` must be `numpy.ndarray`")
        if value.shape[0] != self.__width: raise ValueError("The width of the binary number is not match")
        self.__bin = value
        self.__dec = bin2dec(self.__bin, fixed_point=self.__fixed_point, signed=self.__signed)

    @prefix.setter
    def prefix(self, value: bool) -> None:
        if type(value) != bool: raise TypeError("Type of `prefix` must be `bool`")
        self.__prefix = value


    def set_value(self, value) -> None:
        """Setting value of the binary variable.
        - the type of `value` can be `binary`, `float`, `int`, `numpy.ndarray`, or `str`(hexadecimal).

        Parameter :
        ---
            `value` : the value of the variable.
        """
        if type(value) == binary:
            if value.dec < 0 and not self.__signed: raise ValueError("Negative signed binary variable cannot be assigned to unsigned binary variable")
            self.__bin = dec2bin(value.dec, width=self.__width, fixed_point=self.__fixed_point, signed=self.__signed)
            self.__dec = bin2dec(self.__bin, fixed_point=self.__fixed_point, signed=self.__signed)
        elif type(value) == float or type(value) == int:
            self.__bin = dec2bin(value, width=self.__width, fixed_point=self.__fixed_point, signed=self.__signed)
            self.__dec = bin2dec(self.__bin, fixed_point=self.__fixed_point, signed=self.__signed)
        elif type(value) == np.ndarray:
            if value.shape[0] != self.__width: raise ValueError("The width of the binary number is not match")
            self.__bin = value
            self.__dec = bin2dec(value, fixed_point=self.__fixed_point, signed=self.__signed)
        elif type(value) == str:
            self.__bin = hex2bin(value, width=self.__width)
            self.__dec = bin2dec(value, fixed_point=self.__fixed_point, signed=self.__signed)
        else:
            raise ValueError("The type must be `float`, `int`, `np.ndarray` or `str`")


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


def bin2hex(num: np.ndarray, prefix = False) -> str:
    length = num.shape[0] // 4
    if num.shape[0] % 4 != 0:
        length += 1

    hex = ""
    for i in range(length):
        dec = 0
        for j in range(4):
            if i * 4 + j == num.shape[0]:
                break
            dec += 2**j if num[i * 4 + j] == 1 else 0
        if dec < 10:    hex = str(dec) + hex
        elif dec == 10: hex = 'A' + hex
        elif dec == 11: hex = 'B' + hex
        elif dec == 12: hex = 'C' + hex
        elif dec == 13: hex = 'D' + hex
        elif dec == 14: hex = 'E' + hex
        else:           hex = 'F' + hex
    return f"{num.shape[0]}'h" + hex if prefix else hex


def print_bin(num: np.ndarray, end: str = '\n'):
    """Print a binary number"""
    print(binary_string(num), end=end)


def binary_string(num: np.ndarray, prefix = False):
    """Turn a binary number (numpy.array) into a string (str)"""
    string = ""
    for i in range(num.shape[0]):
        if i % 4 == 0 and i != 0: string = '_' + string
        string = '1' + string if num[i] else '0' + string
    return f"{num.shape[0]}'b" + string if prefix else string


def read_dat_file(dat_file: str, width = WIDTH, fixed_point = 0, signed = False) -> np.ndarray:
    data = []
    with open(dat_file, 'r') as file:
        for line in file:
            remove = min(line.find(' '), line.find('/'))
            num = hex2dec(line[:remove], width, fixed_point, signed)
            data.append(num)
    return np.array(data)
