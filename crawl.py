#!/usr/bin/env python3

import sys
import requests
import json
from pprint import pprint
from lxml import html

#SITE_URL = 'http://serebii.net/pokedex-'
SITE_URL = 'http://pokemondb.net/pokedex/'

def get_moves(mon, tmp, move_dex):
        url = SITE_URL + tmp.lower()
        page = requests.get(url)
        cnt = 0
        move_dex[mon] = {}

        #try:
        #    url = f'{SITE_URL}swsh/{dex[mon]["Dex #"]:03d}.shtml'
        #    page = requests.get(url)
        #except:
        #    url = f'{SITE_URL}sm/{dex[mon]["Dex #"]:03d}.shtml'
        #    page = requests.get(url)
        #print(page.text)
        #tree = html.fromstring(page.content)
        for line in page.text.splitlines():
            #if 'Standard Level Up' in line:
            if '/move/' in line:
                moves = line.split('>')
                for i in range(len(moves)):
                    if 'Egg moves' in moves[i] or 'learnt on evolution' in moves[i] or 'learnt by TM' in moves[i]:
                        return move_dex
                    if 'cell-num' in moves[i]:
                        if not cnt % 3:
                            lv = int(moves[i+1].split('<')[0])
                            mv = moves[i+4].split('<')[0]
                            if lv not in move_dex[mon]:
                                move_dex[mon][lv] = [mv]
                            else:
                                move_dex[mon][lv].append(mv)
                        cnt += 1
        return move_dex                

def get_info(mon, tmp, updateddex):
    url = SITE_URL + tmp.lower()
    page = requests.get(url)
    cnt = 0
    
    lines = page.text.splitlines()

    for i in range(len(lines)):
        if 'EV yield' in lines[i]:
            updated_dex[mon]['EV Yield'] = lines[i+2].split('<')[0].rstrip()
        elif 'Catch rate' in lines[i]:
            try:
                updated_dex[mon]['Catch Rate'] = int(lines[i+1].split('>')[1].split()[0])
            except:
                updated_dex[mon]['Catch Rate'] = None
        elif 'Base <a href="/glossary#def-friendship">Friendship' in lines[i]:
            try:
                updated_dex[mon]['Base Friendship'] = int(lines[i+1].split('>')[1].split()[0])
            except:
                updated_dex[mon]['Base Friendship'] = None
        elif 'Base Exp.' in lines[i]:
            try:
                updated_dex[mon]['Base Experience'] = int(lines[i+1].split('>')[1].split('<')[0])
            except:
                updated_dex[mon]['Base Experience'] = None
        elif 'Growth Rate' in lines[i]:
            updated_dex[mon]['Growth Rate'] = lines[i+1].split('>')[1].split('<')[0]
        elif 'Gender<' in lines[i]:
            try:
                if 'Genderless' in lines[i+1]:
                    updated_dex[mon]['Gender'] = {'Male': 0, 'Female': 0, 'Genderless': True}
                else:
                    gen = lines[i+1].split('>')
                    male = float(gen[2].split('%')[0]) / 100
                    female = float(gen[4].split('%')[0]) / 100
                    updated_dex[mon]['Gender'] = {'Male': male, 'Female': female, 'Genderless': False}
            except:
                updated_dex[mon]['Gender'] = {'Male': 0, 'Female': 0, 'Genderless': True}

        elif 'Egg cycles' in lines[i]:
            updated_dex[mon]['Egg Cycles'] = int(lines[i+1].split('>')[1].split()[0])
            return updated_dex
                
    return updated_dex                

with open('pokedex.json', 'r') as fd:
    dex = json.loads(fd.read())

with open('move_dex.json', 'r') as fm:
    move_dex = json.loads(fm.read())

if __name__ == '__main__':
    #go = False
    #move_dex = {}
    updated_dex = {}
    go = True
    for mon in dex:
        updated_dex[mon] = dex[mon]
        tmp = mon
        if 'Mega' in mon or 'Forme' in mon or 'Alolan' in mon or 'Galarian' in mon:
            continue
        #fd_w = open('updated_dex.json', 'w')
        elif '(female)' in mon.lower():
            tmp = 'nidoran-f'
        elif '(male)' in mon.lower():
            tmp = 'nidoran-m'
        elif 'Jr.' in mon:
            tmp = 'mime-jr'
        elif '. ' in mon:
            tmp = mon.replace('. ', '-')
        elif ': ' in mon:
            tmp = mon.replace(': ', '-')
        elif ' ' in mon:
            tmp = mon.replace(' ', '-')
        elif "'" in mon:
            tmp = mon.replace("'", '')
        print(mon, tmp)
        if go:
            updated_dex = get_info(mon, tmp, updated_dex)
        #if not move_dex[mon]:
        #    print(f'{mon} is empty')
        #    del move_dex[mon]
        #else:
        #    continue
    fd_w = open('updated_dex.json', 'w')
    fd_w.write(json.dumps(updated_dex))
    fd_w.close()
    '''
        print(mon)
        if go:
            move_dex = get_moves(mon, move_dex)
        #fd_w = open('updated_dex.json', 'w')
            #fd_w.write(json.dumps(move_dex))
            #fd_w.close()
    #pprint(move_dex)

                #print(line)
        #print(tree.xpath('/html/body/div[1]/div[2]/main/div/div/div/div/div[4]/ul/li[1]/table[2]/tbody/tr[3]/td[2]'))
    #print(c1, c2)
    '''
