from itertools import permutations

def sl__string__s2h(args, **kwargs):
    try :
        string = ' '.join(args).strip()
        hex_string = ""
        for char in string:
            hex_string += "\\x" + char.encode('utf-8').hex()
        return f'<p> {hex_string} </p>'
    except Exception as e :
        return f'<p style="color : red;">[-] Error encoding string : {e}</p>'

def sl__string__h2s(args, **kwargs):
    try :
        hex_string = ' '.join(args).strip()
        bytes_list = hex_string.split("\\x")[1:]
        byte_values = [int(byte, 16) for byte in bytes_list]
        original_string = bytes(byte_values).decode('utf-8')
        return f'<p> {original_string} </p>'
    except Exception as e :
        return f'<p style="color : red;">[-] Error decoding string : {e}</p>'
    

def sl__string__fcomb(args, **kwargs):
    try :
        word = ' '.join(args).strip().replace(" ", '')
        unique_chars = set(word)
        all_combinations = [''.join(combination) for combination in set(permutations(word))]
        num_combinations = len(list(set(all_combinations)))
        s = ''
        s = s + f'<h4> All Possible Combinations : {num_combinations}</h4>'
        _ = len(s)
        s = s + "="*_
        for wor in list(set(all_combinations)) :
            s = s + f'<p> {wor} </p>'
        return s
    except Exception as e :
        return f'<p style="color : red;">[-] Error processing string : {e}</p>'
    