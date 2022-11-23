from .config_encryption import *

def block_encrypt(block, keys, s_box, mlt_matrix):
    # text = bytes.fromhex('32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34')
    # block = bytes.fromhex('00112233445566778899aabbccddeeff')
    
    dprint('')
    for i in range(ROUNDS + 1):
        dprint(f'start of round')
        print_idle_matrix(block)
        dprint(f'round key value {keys[i].hex()}')
        block = xor(block, keys[i])
        
        if i != (ROUNDS):
            dprint(f'\nROUND {i}')
            block = sub_bytes(block, s_box)
            dprint(f'aftr sub_bytes')
            print_idle_matrix(block)
            
            block = convert_to_matrix(block)
            block = shift_rows(block, 1)
            dprint(f'aftr shift_rows')
            print_matrix(block)
                        
            if i != (ROUNDS - 1):
                block = mix_columns(block, mlt_matrix)
            dprint(f'aftr mix_columns')
            print_matrix(block)
            
            block = convert_to_bytes(block)
            
    dprint(f'output {block.hex()}')
    print_idle_matrix(block)
    return block
    
def encrypt(full_text, keys, s_box, mlt_matrix):
    output = b''
    for i in range(len(full_text))[::16]:
        block = full_text[i:i+16]
        block = expand_string(block, 'utf-8')
        if output:
            block = xor(output[-16:], bytes(block, encoding='utf-8'))
        else:
            block = bytes(block, encoding='utf-8')
        encrypted_block = block_encrypt(block, keys, s_box, mlt_matrix)
        output += encrypted_block
    return output