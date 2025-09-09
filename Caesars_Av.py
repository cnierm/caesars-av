
#    ____                           _     
#  / ___|__ _  ___  ___  __ _ _ __( )___ 
# | |   / _` |/ _ \/ __|/ _` | '__|// __|
# | |__| (_| |  __/\__ \ (_| | |    \__ \
#  \____\__,_|\___||___/\__,_|_|    |___/
                                       
#     _             _                  _          
#    / \__   ____ _| | __ _ _ __   ___| |__   ___ 
#   / _ \ \ / / _` | |/ _` | '_ \ / __| '_ \ / _ \
#  / ___ \ V / (_| | | (_| | | | | (__| | | |  __/
# /_/   \_\_/ \__,_|_|\__,_|_| |_|\___|_| |_|\___|
#
# Created by Caleb Nierman in 2024
# Part of CSC1001's Final Capstone

from os import path
import math
import sys
import argparse
import colorama
from datetime import datetime

colorama.init()

ap = argparse.ArgumentParser(prog='Caesar\'s Avalanche', description='Caeser\'s Avalanche is an attempted incorporation of the Avalanche Effect with a Shift Cipher.')

ap.add_argument('-d', '--decode', help='File to decode')
ap.add_argument('-e', '--encode', help='File to encode')
args = ap.parse_args()

if args.encode and args.decode:
    print('An error occured. Please select whether to encode or decode, not both.')
    sys.exit(1)

# Determines whether to run the program in shell mode of file mode

direction = 0
if args.encode:
    direction = 1
    file_in = args.encode
elif args.decode:
    direction = -1
    file_in = args.decode


def ordify(list, lrange):
    ord_list = []
    for i in lrange:
        ord_list.append(ord(list[i]))
    return ord_list

def unwrap(olist, lrange):
    for i in lrange:
        if olist[i] > 1114102:
            olist[i] -= 1114112
    return olist

def wrap(olist, lrange):
    for i in lrange:
        if olist[i] > 1114102:
            return 1
        elif olist[i] < -9:
            return 1
        elif olist[i] < 0:
            olist[i] += 1114112
    return olist

            

# predictable randomness algorithm... sort of. It computes very quickly but is not flawless.
def find_seed(olist, lrange):
    sum = 0
    for i in lrange:
        sum += olist[i]
    seed = int(10*math.sin(sum))
    if seed == 0:
        seed = int(3*math.cos(sum))
    return seed

# this will perform a oscillate caesar cipher by the amount seed.
# The seed is maintained in the encoded result.
def caesar(olist, num, sign, llen, lrange):
    if llen % 2 == 0:
        for i in lrange[::2]:
            olist[i] += num * sign
            olist[i+1] -= num * sign
    else:
        olist[1] += num * sign
        for i in lrange[::2]:
            olist[i] -= num * sign
        for i in lrange[1::2]:
            olist[i] += num * sign
    return olist

def chrify(olist, lrange):
    for i in lrange:
        olist[i] = chr(olist[i])
    return olist

def gen_file_name(name, chrtoadd, chrtodelete):
    filelist = list(name)
    completion = False
    for i in range(len(filelist)):
        if (filelist[i] == '.') and (filelist[i+1] == chrtodelete) and (filelist[i] == '.'):
            filelist.pop(i)
            filelist.pop(i)
            completion = True
            break
    if completion == False:
        for i in range(len(filelist)):
            if filelist[i] == '.':
                filelist.insert(i, chrtoadd)
                filelist.insert(i, '.')
                completion = True
                break
    if completion == False:
        filelist.append(f'.{chrtoadd}')
        completion = True 

    return ''.join(filelist)

def cipher(str, sign):
    tlen = len(str)
    tlist = list(str)
    trange = range(tlen)

    if tlen <= 1:
            return 1
    ordlist = ordify(tlist, trange)
    ordlist = unwrap(ordlist, trange)
    seed = find_seed(ordlist, trange)
    clist = caesar(ordlist, seed, sign, tlen, trange)
    clist = wrap(clist, trange)
    if clist == 1:
        return 2
    etext = ''.join(chrify(clist, trange))
    
    return etext


####################################    ###
#####     End of functions     #####    ###
#####    Begin main program    #####   
#####                          #####    ###
####################################    ###
def main_file(file):

    # Ensure file exists

    if direction == 1:
        efile = gen_file_name(file, 'e', 'd')
        prefix = 'en'
    else: 
        efile = gen_file_name(file, 'd', 'e')
        prefix = 'de'
    
    ### Overwrite protection ###

    if path.exists(efile):
        valid_response = False
        while valid_response == False:
            override_response = input(f'{colorama.Fore.YELLOW}File {efile} already exists. Overwrite? [y/N]: {colorama.Fore.WHITE}')
            if override_response.lower() == 'n' or override_response.lower() == 'no' or override_response.lower() == '':
                
                efile_new = input('Enter the desired name of the output file: ')
                if efile_new:
                    efile = efile_new
                    valid_response = True
                else:
                    print(f'{colorama.Fore.Red}Please input a Real File.{colorama.Fore.WHITE}')
            elif override_response.lower() == 'y' or override_response.lower() == 'yes':
                valid_response = True
                break
            else:
                print('Invalid Response. Please input the letter "y" or "n".')
    if not path.exists(file):
        print(f'{colorama.Fore.RED}An Error Occured. File {file} does not exist.{colorama.Fore.WHITE}')
        sys.exit(1)

    text = (open(file)).read()
    #file.close()

    etext = cipher(text, direction)
    
    if etext == 1:
        print(f'{colorama.Fore.RED}Error: You must have a minumum of 2 characters to encode or decode{colorama.Fore.WHITE}')
        sys.exit(1)
    elif etext == 2:
        print(f'{colorama.Fore.RED}Error: avoid using the final 18 unicodes (0x10ffee - 0x10ffff){colorama.Fore.WHITE}')
        sys.exit(2)
    file_out = open(efile, 'w') 
    file_out.write(etext)
    print(f'{file_in} has successfully been {prefix}coded into {efile}.')

def main_shell():
    print('Entering shell mode. For files, use the -e and -d flags.')
    print('Switch from encode/decode with \\e and \\d. \\q to quit.')
    print(f'{colorama.Fore.YELLOW}Note: Non-printable characters may not display correctly, but they will be in the log file.{colorama.Fore.WHITE}')
    logfile = open('Caesars_Av.log', 'a')
    direction = 1
    symbol = 'e'
    skip = False
    

    while True:
        text = input(f'[{symbol}]: ')
        if not text:
            skip = True
            pass
        elif text[0] == '\\':
            if text[1] == 'e':
                direction = 1
                symbol = 'e'
                skip = True
                print(f'{colorama.Fore.GREEN}Now encoding. Use \'\\\\\' at the beginning if this wasn\'t desired{colorama.Fore.WHITE}')
            elif text[1] == 'd':
                direction = -1
                symbol = 'd'
                skip = True
                print(f'{colorama.Fore.GREEN}Now decoding. Use \'\\\\\' at the beginning if this wasn\'t desired{colorama.Fore.WHITE}')
            elif text[1] == 'q':
                logfile.close()
                sys.exit()
            elif text[1] == '\\':
                text.pop(0)
        if not skip:
            etext = cipher(text, direction)

            if etext == 1:
                etext = f'{colorama.Fore.RED}Error: You must have a minumum of 2 characters to encode or decode{colorama.Fore.WHITE}'
            elif etext == 2:
                etext = f'{colorama.Fore.RED}Error: avoid using the final 18 unicodes (0x10ffee - 0x10ffff){colorama.Fore.WHITE}'
            
            logfile.write(f'[{datetime.now().replace(microsecond=0)}] [{symbol}] [{text}]\n{etext}\n\n')
            print(etext)
        else:
            skip = False


if direction != 0:
    main_file(file_in)
else:
    main_shell()