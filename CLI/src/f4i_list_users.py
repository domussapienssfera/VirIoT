#!/usr/bin/python3
import argparse
import json
import requests
import os
from pathlib import Path


viriot_dir = str(Path.home())+"/.viriot"
token_file = viriot_dir+"/token"

def printj(msg):
    print("\n")
    jres = json.loads(msg)
    for elem in jres:
        elem.pop("yamlFiles", None)
    print(json.dumps(jres, indent=4, sort_keys=True))
    print("\n")

def get_token():
    if not os.path.isfile(token_file):
        print("Token not found")
        return None
    with open(token_file, 'r') as file:
        data = json.load(file)
        token = data["access_token"]
        return token


def init_args(parser):

    parser.set_defaults(func=run)
    parser.add_argument('-c', action='store', dest='controllerUrl',
                    help='Controller url (default: http://127.0.0.1:8090)', default='http://127.0.0.1:8090')


def run(args): 
    url=args.controllerUrl+"/listUsers"
    token = get_token()
    if not token:
        return
    headers = {
        'Authorization': "Bearer " + token,
        'accept': "application/json",
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers)
    printj(response.text)
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    init_args(parser)
    args=parser.parse_args()
    args.func(args)
