#! /usr/bin/python

from glob import glob
import os
from os import path
from telnetlib import NOP
import requests

try:
    import wget
    from bs4 import BeautifulSoup
except ModuleNotFoundError as e:
    print(f'[!] Please install {e.name} with pip3')
    exit()


BASE_URL = 'https://portswigger.net'

# Get the main release page https://portswigger.net/burp/releases#professional
# Search for the latest version avalible, usually not stable
print("[*] Looking for the latest version")
releases = requests.get(BASE_URL + '/burp/releases')
soup = BeautifulSoup(releases.text, 'html.parser')
versions = soup.find_all('a', class_='noscript-post')
versions = list(filter(lambda x: x.text.find('Professional') != -1, versions))
for v in versions:
    download = requests.get(BASE_URL + v['href'])
    # Stable versions are marked with class label-light-red-small
    if download.text.find('label-light-red-small') != -1:
        latest = v['href']
        version = ' '.join(v.text.split()).replace(
            'Professional / Community ', '').split(' ')
        break

# Fetch the download link based on requested build
soup = BeautifulSoup(download.text, 'html.parser')
builds = soup.find_all('a', download='release')
relevant = list(filter(lambda element: element.string.find('Jar') != -1, builds))

# for index, os in enumerate(relevant):
#     print(f' [{index}] {os.string}')
# selected = int(input('[#] Select build: '))
link = relevant[0]['href']

# Check and delete if installed version less then latest
try:
    [curr_ver_file] = glob(os.getcwd() + '/burpsuite_pro/burpsuite*.jar')
    curr_ver = path.splitext(path.basename(curr_ver_file))[0]
    curr_ver = curr_ver[curr_ver.find('v')+1:]

except ValueError:
    curr_ver = '0'

if int(curr_ver.replace('.','')) < int(version[0].replace('.','')):
    os.remove(curr_ver_file) if curr_ver != '0' else NOP
    # Download
    print('[*] Starting the download of ' + relevant[0].text + ' version ' + version[0])
    burp = wget.download(BASE_URL + link, out=os.getcwd() + '/burpsuite_pro/')
    print('\n[*] Download completed, Burp Suite updated successfuly to ' + version[0])
else:
    print(f'[!] Burp Suite is up to date (v{curr_ver})')
