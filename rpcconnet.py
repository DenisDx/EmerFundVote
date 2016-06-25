#!/usr/bin/python
# -*- coding: UTF-8 -*-


#Модуль запрашивает у кошелька всякую дребедень

import requests
import json
import walletconfig

global current_wallet_config
current_wallet_config=[]

def configured():
    return 'server' in current_wallet_config and current_wallet_config['server']

def init_config():
    global current_wallet_config
    if not walletconfig.is_config_connectable():
        print('RPC disabled')
        current_wallet_config=[]
        return 0
    else:
        current_wallet_config=walletconfig.read_default_config()
        return 1

def walreq(req,config=None):
    if not config: config=current_wallet_config
    url = "http://%s:%s@%s:%s"%(config['rpcuser'],config['rpcpassword'],'localhost',config['rpcport'])
    headers = {'content-type': 'application/json'}
    return requests.post(url, data=json.dumps(req), headers=headers).json()

def get_balance(acc=""):
    return walreq({"method": "getbalance","params": [acc] if acc else [],"jsonrpc": "2.0","id": 0})['result']


#"http://user:password@127.0.0.1:8332"
#url = "http://%s:%s@%s:%s"%(walletconfig['rpcuser'],walletconfig['rpcpassword'],'localhost',walletconfig['rpcport'])
#headers = {'content-type': 'application/json'}

#req = {
#    "method": "getbalance",
#    "params": [],
#    "jsonrpc": "2.0",
#    "id": 0,
#}

def test():
    print('Balance:%s\n'%get_balance())
    print(
        walreq({"method": "getaddressesbyaccount","params":[],"jsonrpc": "2.0","id": 0})['result']
        )

    la=walreq({"method": "listaccounts","params":[],"jsonrpc": "2.0","id": 0})['result']
    print('Accounts:',la)


    #getaccountaddress что такое я не знаю
    print('Addresses:')
    for a in la.keys():
        print(a,':',walreq({"method": "getaddressesbyaccount","params":[a],"jsonrpc": "2.0","id": 0})['result'])

    #print('Accountaddress:')
    #for a in la.keys():
    #    print(a,':',
    #        walreq({"method": "getaccountaddress","params":[a],"jsonrpc": "2.0","id": 0})['result']
    #    )


if __name__ == "__main__":
    if init_config():
        test()