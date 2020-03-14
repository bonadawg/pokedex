#!/usr/bin/env python3

import sys
import requests
import json
from pprint import pprint
from lxml import html

SITE_URL = 'http://serebii.net/pokedex-'

with open('pokedex.json', 'r') as fd:
    dex = json.loads(fd.read())

if __name__ == '__main__':
    for mon in dex:
        url = SITE_URL + mon.lower()
        page = requests.get(url)
        tree = html.fromstring(page.content)
        print(tree.xpath('//span[@class=""]/text()'))
        break
