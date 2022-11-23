# NOTE: Key expansion is not functional for rounds abouve 10
ROUNDS = 10
DEBUG = False

def dprint(text, end='\n'):
    if DEBUG:
        print(f'{text}', end=end)
        
def expand_string(string: str, length=16) -> str:
    return string + ' ' * (16 - len(string))

def convert_to_matrix(bytes_: bytes) -> list:
    """
                   1 4 7
    1 2 3 ... 9 -> 2 5 8
                   3 6 9
    NOTE: Matrix has to be 4x4
    """
    matrix = []
    for i in range(4):
        matrix.append(bytearray())
        for j in range(4):
            matrix[i].append(bytes_[i + j * 4])
    return matrix

def convert_to_bytes(matrix: list) -> bytes:
    """Inverse of convert to matrix"""
    bytes_ = bytes()
    for i in range(4):
        for j in range(4):
            bytes_ += matrix[j][i: i+1]
    return bytes_

def print_matrix(matrix: list) -> None:
    for i in matrix:
        dprint(i.hex())
        
def print_idle_matrix(bytes_: bytes) -> None:
    """Prints flat, unconverted matrix as 4x4 matrix"""
    for i in range(4):
        for j in range(4):
            dprint(bytes_[i + j * 4: i + j * 4 + 1].hex(), '')
        dprint('')

def xor(byte_1: bytes, byte_2: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(byte_1, byte_2))

def galois_mult(a: int, b: int, r: int=0b100011011) -> int:
    # Multiplication
    c = 0
    for i in range(8):
        # Right bit
        bit_b = (b >> i) & 1
        if bit_b:
            added_num = a << i
            c ^= added_num
                       
    # Modulo   
    c_length = c.bit_length()
    for i in range(c_length):
        # Left bit
        bit_c = (c>>c_length-i-1) & 1
        if bit_c:
            if c_length-i-1 > 7:
                shift_quantity =  c_length-i-9
                substracted_num = r << shift_quantity
                c ^= substracted_num
    return c
                
def sub_byte(byte: bytes, table: list) -> bytes:
    byte = byte.hex()
    x = int(byte[1], 16)
    y = int(byte[0], 16)
    return table[y][x:x+1]

def sub_bytes(all_bytes: bytes, table: list) -> bytes:
    for i in range(len(all_bytes)):
        byte = all_bytes[i:i+1]
        byte = sub_byte(byte, table)
        # Equivalent to all_bytes[i] = byte
        all_bytes = all_bytes[0:i] + byte + all_bytes[i+1:]
    return all_bytes

def shift(list_: list, quantity: int) -> list:
    return list_[quantity:] + list_[:quantity]

def shift_rows(matrix: list, direction: int) -> list:
    """direction is rather 1 or -1. 
    1: shift rows to the left (used to encryption)
    -1: shift rows to the right (used for decryption)"""
    # TODO: test function
    for i in range(4):
        matrix[i] = shift(matrix[i], i*direction)
    return matrix

def mix_columns(matrix_1: list, matrix_2: list) -> list:
    output = [bytearray(),
              bytearray(),
              bytearray(),
              bytearray()]
    
    for i in range(4):
        # dprint('')
        for j in range(4):
            # dprint(f'   {i=} {j=}')
            value = 0
            for k in range(4):
                a = matrix_1[k][j]
                b = matrix_2[i][k]
                value ^= galois_mult(a, b)
                # dprint(f'   a={hex(a)} b={hex(b)} product={hex(galois_mult(a, b))}')
            # dprint(f'value={hex(value)}')
            output[i].append(value)
            
    return output

def get_r_con(i: int) -> bytes:
    return ((2**i) % 229).to_bytes(4, byteorder='little')

def g(word: bytearray, rcon: bytes, table: list) -> bytes:
    word = shift(word, 1)
    dprint(f'after rotation {word.hex()}')
    word = sub_bytes(word, table)
    dprint(f'after sub {word.hex()}')
    new_first_byte = xor(word[0:1], rcon)
    word = new_first_byte + word[1:]
    dprint(f'rcon {rcon.hex()}')
    dprint(f'after rcon {word.hex()}')
    return word
        
def key_expansion(key: str, table: list) -> bytearray:
    key = expand_string(key)
    key = bytearray(key, encoding='utf-8')
    # key = bytearray.fromhex('2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c')
    # key = bytearray.fromhex('000102030405060708090a0b0c0d0e0f')
    
    count = 0
    while len(key) < 16 * (ROUNDS + 1):
        for i in range(4):
            last_word = key[-4:]
            dprint(f'temp {last_word.hex()}')
            if i == 0:
                last_word = g(last_word, get_r_con(count), table)
                count += 1
            first_word = key[-16:][:4]
            dprint(f'w[i-Nk] {first_word.hex()}')
            dprint(f'xor {xor(first_word, last_word).hex()}')
            key += xor(first_word, last_word)
            
    if DEBUG:
        for i in range(ROUNDS + 1):
            print(key[i*16:(i+1)*16].hex())
    return [key[i*16:(i+1)*16] for i in range(ROUNDS + 1)]