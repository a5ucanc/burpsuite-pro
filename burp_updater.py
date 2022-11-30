#! /usr/bin/python

from glob import glob
import os
import sys
from os import path
import platform
from telnetlib import NOP
import requests

try:
    import wget
    from bs4 import BeautifulSoup
except ModuleNotFoundError as e:
    print(f'[!] Please install {e.name} with pip3')
    exit()


BASE_URL = 'https://portswigger.net'
CONFIG_FILE = 'updater_configs.txt'

# additional = ['wget', 'beautifulsoup4']
# for lib in additional:
#     if lib not in sys.modules:
#         errors = True
#         print(
#             f'[!] Error: could not find {lib}, please install using: pip3 install {lib}')
# if errors:
#     exit()


def load_config():
    # Load configs from updater_configs.txt
    try:
        with open(CONFIG_FILE, 'r') as conf:
            lines = conf.readlines()
            for line in lines:
                field, value = line.split(':')
                match field:
                    case 'download_folder':
                        download = value.replace('\n', '')
                    case 'machine':
                        machine = value.replace('\n', '')
                    case _:
                        if not download and machine:
                            return ''
        return {'folder': download, 'machine': machine}
    except Exception:
        return ''


def start_config():
    wd = os.getcwd()
    default_burp = os.listdir(wd)
    for file in default_burp:
        if path.isdir(path.join(wd, file)):
            if 'burpsuite' in file:
                default_burp = path.join(wd, file)
                break
    with open(CONFIG_FILE, 'w') as conf:
        print(f'[*] Burp folder location ({default_burp}) ')
        conf.write('download_folder:' + default_burp + '\n')
        machine = f'{platform.system()}${platform.machine()}'
        conf.write('machine:' + machine + '\n')
    return {'folder': default_burp, 'machine': machine}


conf = load_config()
while not conf:
    conf = start_config()


# Todo: regex, I am to lazy to learn this stuff
def filter_func(element: str):
    if element.string.find('Community') != -1:
        return False

    elif element.string.find('Jar') != -1:
        return True
    sy, mac = conf['machine'].split('$')
    if element.string.find(sy) != -1:
        return True


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
relevant = list(filter(filter_func, builds))

# for index, os in enumerate(relevant):
#     print(f' [{index}] {os.string}')
# selected = int(input('[#] Select build: '))
link = relevant[0]['href']

# Check and delete if installed version less then latest
try:
    [curr_ver_file] = glob(conf['folder'] + '/burpsuite_pro*.jar')
    curr_ver = path.splitext(path.basename(curr_ver_file))[0]
    curr_ver = curr_ver[curr_ver.find('v')+1:]

except ValueError:
    curr_ver = '0'

if int(curr_ver.replace('.','')) < int(version[0].replace('.','')):
    os.remove(curr_ver_file) if curr_ver != '0' else NOP
    # Download
    print('[*] Starting the download of ' + relevant[0].text)
    burp = wget.download(BASE_URL + link, out=conf['folder'])
    print('\n[*] Download completed, Burp Suite updated successfuly to ' + version[0])
else:
    print(f'[!] Burp Suite is up to date (v{curr_ver})')
