# EEGuizhi
"""
This is a simple tool for binary operations in Python,
binary numbers are implemented with 1-dim integer numpy array.
"""
import numpy as np


class binary:
    def __init__(self, value = 0.0, width = 32, fixed_point = 0, signed = True, prefix = False) -> None:
        """Declare a binary variable.

        Parameters:
        ---
            `value`: the value of the variable, type can be `binary`, `float`, `int`, `numpy.ndarray`, or `str`(hexadecimal).
            `width`: the width of the variable.
            `fixed_point`: the index of 2^0 digit in binary format.
            `signed`: `True` for signed, `False` for unsigned.
            `prefix`: if the string has width & radix info prefix in front of the binary number.
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
    def hex(self) -> str:
        return bin2hex(self.__bin, self.prefix)

    @property
    def prefix(self) -> bool:
        return self.__prefix

    def __call__(
            self, value = 0.0, width: int = None, fixed_point: int = None,
            signed: bool = None, prefix: bool = None
        ) -> None:
        """Reset the binary variable.

        Parameters:
        ---
            `value`: the value of the variable, type can be `binary`, `float`, `int`, `numpy.ndarray`, or `str`(hexadecimal).
            `width`: the width of the variable.
            `signed`: `True` for signed, `False` for unsigned.
            `fixed_point`: the index of 2^0 digit in binary format.
            `prefix`: if there will be a width prefix in front of the binary number.
        """
        self.__width = self.__width if width == None else width
        self.__signed = self.__signed if signed == None else signed
        self.__fixed_point = self.__fixed_point if fixed_point == None else fixed_point
        self.__prefix = self.__prefix if prefix == None else prefix
        self.set_value(value)

    def __str__(self) -> str:
        return binary_string(self)

    def __round__(self, width: int) -> float:
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
        """Set the value of the binary variable.
        - the type of `value` can be `binary`, `float`, `int`, `numpy.ndarray`, or `str`(hexadecimal).

        Parameters:
        ---
            `value`: the value of the variable.
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


def full_add(a: bool, b: bool, c: bool) -> tuple[bool, bool]:
    """Act like a full adder, intput (1bit) `a`, `b`, `c` and return sum, carry.

    Returns:
    ---
        tuple: (carry: bool, sum: bool)
    """
    return (a&b | c&(b|a), a ^ b ^ c)


def add(num1: np.ndarray, num2: np.ndarray, width: int = None) -> np.ndarray:
    """Applying binary addition to sum two numbers.

    Parameters:
    ---
    `num1`: the first binary number
    `num2`: the second binary number
    `width`: the width of binary number after summing
    """
    if width == None: width = max(num1.shape[0], num2.shape[0])
    carry, sum = 0, np.zeros(width, dtype=int)
    for i in range(width):
        carry, sum[i] = full_add(num1[i], num2[i], carry)
    return sum


def twos_comp(num: np.ndarray) -> np.ndarray:
    return add(inv(num), dec2bin(1, num.shape[0]), num.shape[0])

def neg(num: np.ndarray) -> np.ndarray:  # same as 2s_comp
    return twos_comp(num)

def inv(num: np.ndarray) -> np.ndarray:
    val = num.copy()
    for i in range(val.shape[0]):
        val[i] = 0 if val[i] == 1 else 1
    return val


def mult(num1: np.ndarray, num2: np.ndarray, width: int) -> np.ndarray:
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
            tmp[i:] = a[:width - i] if i != width - 1 else twos_comp(a[:width - i])
            sum = add(sum, tmp)

    return sum


def resize(num: np.ndarray, width: int, lsb = 0, round = False):
    """"""


def binary_round(num: np.ndarray, width: int) -> np.ndarray:
    """`width`: new width of the number must less than original width"""
    if width >= num.shape[0]: raise ValueError("new width must less than original width")
    binary = num[width - 1:].copy()
    return add(binary, dec2bin(1, width)) if num[width] == 1 else binary


def dec2bin(num: float, width: int = 32, fixed_point: int = 0, signed = True) -> np.ndarray:
    if num < 0 and not signed: raise ValueError("num cannot be a negative value")
    val, binary = abs(num), np.zeros(width, dtype=int)
    idx = width - 2 if signed else width - 1
    while idx >= 0:
        power = idx - fixed_point
        if val >= 2**power:
            binary[idx] = 1
            val -= 2**power
        idx -= 1
    return binary if num > 0 else twos_comp(binary)


def bin2dec(num: np.ndarray, fixed_point: int = 0, signed: bool = True) -> float:
    width = num.shape[0]
    binary = twos_comp(num) if num[width - 1] == 1 and signed else num
    value = 0
    for i in range(binary.shape[0]):
        value += 2**(i - fixed_point) if binary[i] == 1 else 0
    return (-1) * value if num[width - 1] == 1 and signed else value


def hex2bin(hex_str: str, width: int = 32) -> np.ndarray:
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


def hex2dec(hex_str: str, width: int = 32, fixed_point: int = 0, signed: bool = True) -> int:
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
        if   dec <  10: hex = str(dec) + hex
        elif dec == 10: hex = 'A' + hex
        elif dec == 11: hex = 'B' + hex
        elif dec == 12: hex = 'C' + hex
        elif dec == 13: hex = 'D' + hex
        elif dec == 14: hex = 'E' + hex
        else:           hex = 'F' + hex
    return f"{num.shape[0]}'h" + hex if prefix else hex


def dec2hex(num: float, width: int, fixed_point: int):
    """"""



def str2bin(num: str, fixed_point = 0, signed = False, prefix = False) -> binary:
    """Turn a binary number (str) into a binary variable (binary)

    Parameters:
    ---
        `num`: binary string (must include prefix of width & radix)
        `fixed_point`: the index of 2^0 digit in binary format.
        `signed`: `True` for signed, `False` for unsigned.
        `prefix`: if the string has width & radix info prefix in front of the binary number.

    Returns:
    ---
        A binary variable (binary).
    """
    if type(num) != str: raise TypeError("Type of `num` must be `str`")

    prime = num.find("'")
    width = int(num[:prime])
    radix = num[prime + 1]
    num = num[prime + 2:].replace('_', '')

    if not width > 0 or radix not in "bhd":
        raise ValueError("The width of number must be set correctly")
    elif radix == 'b':
        for i in range(len(num) - 1, -1, -1):
            pass
    elif radix == 'h':
        pass
    else:
        pass


def binary_string(num: binary):
    """Turn a binary number (numpy.array) into a string (str)
    
    Parameters:
    ---
    `num`: binary variable
    
    Returns:
    ---
    binary number in string form
    """
    string = ""
    for i in range(num.bin.shape[0]):
        if i % 4 == 0 and i != 0: string = '_' + string
        string = '1' + string if num.bin[i] else '0' + string
    return f"{num.bin.shape[0]}'b" + string if num.prefix else string


def read_dat_file(dat_file: str, width = int, fixed_point = 0, signed = False) -> np.ndarray:
    """Read hexadecimal numbers in the `.dat` file and return as a numpy array
    
    Parameters:
    ---
    `dat_file`: the path of file to be read
    `width`: width of the numbers in the file
    `fixed_point`: the fixed point of the numbers in the file
    `signed`: if the numbers in the file are signed number or not
    
    Returns:
    ---
    `data`: 1-dim (decimal) integer numpy array
    """
    data = []
    with open(dat_file, 'r') as file:
        for line in file:
            remove = min(line.find(' '), line.find('/'))
            num = hex2dec(line[:remove], width, fixed_point, signed)
            data.append(num)
    return np.array(data)
