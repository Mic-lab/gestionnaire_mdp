import os
import json
from .encrypt import encrypt
from pathlib import Path
from scripts.constant_matrices import S_BOX, MLP_MATRIX
from time import sleep
from random import shuffle

path: Path = Path(__file__)
data_path = path.parent.parent / 'data.txt'

mode = 'password'
keys = ''
password_exist = ''
password_length_error = False
decryption_error = False
prompt = True
password = True
show_emails = False
text_added = 'enter title'
new_account_length_error = False
text_added_info = {}
delete_length_error = False
delete_num_error = False
delete_data_size_error = False
delete_num_size_error = False
deleted_num = None
success_del = False
view_length_error = False
view_num_error = False
view_data_size_error = False
view_num_size_error = False
view_num = None
view_pass = False
succces_creation = False
WAIT_TIME = 2
wait = True
FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSdDQnxUSJAD9Kl7JFeQ1rNJp7LKD5qcxKJIMEX66iodJG-kjw/viewform?usp=sharing'

def clear():
    os.system('cls')
    
def set_title(text):
    os.system(f'title {text}')

# import sys
# def print(text, end='\n', delay=0.0005):
#     for c in text:
#         sys.stdout.write(c)
#         sleep(delay)
#     sys.stdout.write(end)
    
def print_possible_commands(mode):
    if mode == 'menu':
        print('Commandes possible:')
        print('(Q) - Quitter')
        print('(D) - Déconnecter')
        print('(V) - Voir tous les comptes')
        print('(M) <Numéro du compte> - Voir le mot de passe d\'un compte (ex: "m 2")')
        print('(A) - Ajouter un nouveau compte')
        print('(S) <Numéro du compte> - Supprimer un compte (ex: "s 2")')
        print('(O) - Ouvrir le formulaire\n')

def print_title_screen():
    print(f'''
█▀▀ █▀▀ █▀ ▀█▀ █ █▀█ █▄░█ █▄░█ ▄▀█ █ █▀█ █▀▀
█▄█ ██▄ ▄█ ░█░ █ █▄█ █░▀█ █░▀█ █▀█ █ █▀▄ ██▄

█▀▄ █▀▀   █▀▄▀█ █▀█ ▀█▀ █▀   █▀▄ █▀▀   █▀█ ▄▀█ █▀ █▀ █▀▀
█▄▀ ██▄   █░▀░█ █▄█ ░█░ ▄█   █▄▀ ██▄   █▀▀ █▀█ ▄█ ▄█ ██▄

               Fait avec le cryptage AES
                  Par: Michael Labib

SVP remplissez ce formulaire après avoir utilisé le programme:
{FORM_LINK}
''')

def valid_password(password):
    return len(password) > 4 and len(password) <= 16

def display_accounts(accounts):
    # NOTE: This code can be probably be optimized
    if len(accounts) > 1:
    
        INFO = [[None, 'ID'],
                ['title', 'Titre'], 
                ['email', 'Courriel'],
                ['other', 'Commentaire'],
                ['date', 'Date ajouté']]
            
        max_sizes = []
        
        len_longest_id = len(str(len(accounts)))
        if len_longest_id > len(INFO[1]):
            max_sizes.append(longest_id)
        else:
            max_sizes.append(len(INFO[1]))
        
        for info in INFO[1:]:
            values = []
            for acc in accounts[1:]:
                if info[0] in acc:
                    values.append(acc[info[0]])
            values.append(info[1])
            max_sizes.append(len(max(values, key=len)))  
            
        lines = []
            
        for i, account in enumerate(accounts):
            if i == 0:
                for j, info in enumerate(INFO):
                    print(info[1], end='')
                    print(' ' * (max_sizes[j] - len(info[1]) + 2), end='')
                print()
                for max_size in max_sizes:
                    print('─'*max_size, end='  ')
                print()
            else:
                for j, info in enumerate(INFO):
                    if j == 0:
                        print(i, end='')
                        print(' ' * (max_sizes[0] - len(str(i)) + 2), end='')
                    else:
                        if info[0] in account:
                            account_info = account[info[0]]
                            print(account_info, end='')
                        else:
                            account_info = ''
                        print(' ' * (max_sizes[j] - len(account_info) + 2), end='')
                print()
        print()
        
    else:
        print('Il y a aucune compte de sauvegardé.\n')
        
def save_changes(data, keys):
    # The seperators removes extra white space
    data = json.dumps(data, separators=(',', ':'))
    data = encrypt(data, keys, S_BOX, MLP_MATRIX)

    with open(data_path, 'wb') as f:
        f.write(data)
        
def delete_data_file():
    if os.path.isfile(data_path):
        os.remove(data_path)