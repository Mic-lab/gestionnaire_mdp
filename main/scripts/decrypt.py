from .config_encryption import *

def block_decrypt(block, keys, s_box, mlt_matrix):
    
    dprint('')
    for i in range(ROUNDS + 1):
        rount_count = i
        i = ROUNDS - i
        dprint(f'round [{rount_count}].start        {block.hex()}')
        dprint(f'round [{rount_count}].key          {keys[i].hex()}')
        block = xor(block, keys[i])
        dprint(f'round [{rount_count}].xor          {block.hex()}')
        if rount_count != (ROUNDS):
            block = convert_to_matrix(block)
            
            if rount_count != 0:
                block = mix_columns(block, mlt_matrix)
                dprint(f'round [{rount_count}].mix          {convert_to_bytes(block).hex()}')
            
            block = shift_rows(block, -1)
            block = convert_to_bytes(block)
            dprint(f'round [{rount_count}].shift        {block.hex()}')
            
            block = sub_bytes(block, s_box)
            dprint(f'round [{rount_count}].sub          {block.hex()}')

    dprint(f'output {block.hex()}')
    print_idle_matrix(block)
    return block

def decrypt(raw_text, keys, s_box, mlt_matrix):
    output = b''
    for i in range(len(raw_text))[::16]:
        block = raw_text[i:i+16]
        decrypted_block = block_decrypt(block, keys, s_box, mlt_matrix)
        if output:
            decrypted_block = xor(raw_text[i-16:i], decrypted_block)
        output += decrypted_block
    return output