#!/usr/bin/env python3

import sys
import json
import csv
from pprint import pprint

if __name__ == '__main__':

    data = {}

    with open('pokedex-v2.csv') as fd:
        reader = csv.DictReader(fd)
        for row in reader:
            name = row['Pokemon']
            if name in data:
                name += f' {row["Forme"]}'
            data[name] = row
    
    
    fd_w = open('pokedex.json', 'w')

    for i in data:
        data[i]['Dex #'] = int(data[i]['Dex #'][1:])
        for j in data[i]:
            if data[i][j] == '-----':
                data[i][j] = None
            try:
                data[i][j] = int(data[i][j])
            except:
                pass

    fd_w.write(json.dumps(data))
    fd_w.close()
