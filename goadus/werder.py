#!/usr/bin/python3

# A 2018 Python port of a 2008 PHP port of a 1998 C program.
#
# Original C header:
#
#     Snoof Generator v1.1
#
#     Dave Olszewski  4/25/1997
#     updated         8/12/1998
#
#     A relatively inefficient way
#      to make snoof

import random


def get_werder_werds(numwerd=0):
    vow = ['a', 'e', 'i', 'o', 'u', 'ee', 'ai', 'ie', 'io', 'oo', 'ea',
           'oi', 'oa', 'ou', 'a', 'e', 'i', 'o', 'u']
    beg = ['sn', 'sl', 'tr', 'l', 'bl', 'fl', 'cr', 'b', 'dr', 'wr', 'gr',
           'pl', 'squ', 'qu', 'cl', 'spl', 'fr', 'm', 'k']
    end = ['nd', 'ck', 'll', 'mn', 'w', 'ls', 'sk', 'rt', 'rd', 'zz', 'gh',
           'ght', 'ny', 'nct', 'ch', 'st', 'nt', 'm', 'ng', 'ly', 'd', 'ff',
           't']
    all = ['sn', 'd', 'sp', 's', 'th', 'r', 't', 'p', 'sh', 'ph',
           'ct', 'nk', 'str', 'f', 'h', 'c', 'm', 'n',
           'cr', 'x', 'st', 'b', 'g', 'k', 'l', 'v', 'w', 'z']

    if numwerd <= 0:
        numwerd = random.randint(5, 9)

    out = []
    for _ in range(numwerd):
        werd = ''
        numsyl = random.randint(3, 7)
        csyl = numsyl

        # start with consonant or vowel
        flip = random.randint(0, 2)
        if csyl % 2:
            flip = (not flip)

        while csyl > 0:
            if ((not flip) and (csyl % 2)) or ((flip) and (not (csyl % 2))):
                if csyl == numsyl:
                    werd += random.choice(beg)
                elif csyl == 1:
                    werd += random.choice(end)
                else:
                    werd += random.choice(all)
            else:
                werd += random.choice(vow)
            csyl = csyl - 1
        out.append(werd)

    return out


def get_werder():
    sent = ' '.join(get_werder_werds()).capitalize()
    sent += random.choice(['!', '.', '?'])
    return sent


if __name__ == '__main__':
    print(get_werder())
