#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

default_comment_list={
    "":"""
# JSON-RPC options (for controlling a running Emercoin/emercoind process)"""
    ,"server":"""
# server=1 tells Emercoin to accept JSON-RPC commands."""
    ,"rpcuser":"""
# You must set rpcuser and rpcpassword to secure the JSON-RPC api."""
    ,"rpcallowip":"""
# By default, only RPC connections from localhost are allowed.  Specify
# as many rpcallowip= settings as you like to allow connections from
# other hosts (and you may use * as a wildcard character):"""
    ,"rpcport":"""
# Listen for RPC connections on this TCP port:"""
    ,"rpcconnect":"""
# You can use Emercoin or emercoind to send commands to Emercoin/emercoind
# running on another host using this option: """
    ,"rpcssl":"""
# Use Secure Sockets Layer (also known as TLS or HTTPS) to communicate
# with Emercoin -server or emercoind"""
    ,"rpcsslciphers":"""
# OpenSSL settings used when rpcssl=1"""
}

default_order=['server','rpcuser','rpcpassword','rpcallowip','rpcport','rpcconnect','rpcssl','rpcsslciphers','rpcsslcertificatechainfile','rpcsslprivatekeyfile'];


def read_config_file(filename): #Чтение ЗНАЧАЩИХ пар. Без секций
    """
    Read a simple ``'='``-delimited config file.
    Raises :const:`IOError` if unable to open file, or :const:`ValueError`
    if an parse error occurs.
    """
    cfg = {}
    f = open(filename)
    try:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    (key, value) = line.split('=', 1)
                    cfg[key] = value
                except ValueError:
                    pass # Happens when line has no '=', ignore
    finally:
        f.close()
    return cfg

def add_to_config_file(filename,cfg,commentslist=default_comment_list):
    #Добавляет в файл парамерты
    #1. Если файла нет - создает
    #2. Если параметр есть - меняет
    #3. Если нет, то доавляет
    # при добавлении старается найти то место, где он упоминается в камментах, и добавить после этой строчки

    #делаем так-
    #1. читаем файл в список строк
    #2. записываем эти строки в новый файл, при этом если в конфиге встретили имеющееся - меняем его и удаляем из конфига
    #3. записывае что осталось, при этом вставляя камменты

    if not filename: filename=get_default_config_file_name()

    from copy import deepcopy
    cf=deepcopy(cfg)

    nlines=[]
    f = open(filename)
    try:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    (key, value) = line.split('=', 1)
                    #cfg[key] = value
                    if key and (key in cf.keys()):
                        nlines.append("%s=%s\n"%(key, cf.pop(key)))
                    else:
                        nlines.append("%s\n"%line)
                except ValueError:
                    pass # Happens when line has no '=', ignore
            else:
                #if line:nlines.append(line+"\n")
                nlines.append(line+"\n")
    finally:
        f.close()


    def addkey(nlines,key,value,commentslist):
        #спецдобавка - ищем тупо строку вида #key=value
        #если она есть - удаляем тупо каммент, ничего не добавляем
        v="%s=%s\n"%(key, value)

        if '#'+v in nlines:
            nlines[nlines.index('#'+v)]=v
        else:
            if key in commentslist:
                nlines.append(commentslist[key]+"\n")
            nlines.append(v)

    #Добавляем новые параметры по листу сортировки
    for key in default_order:
        if key in cf.keys():
            addkey(nlines,key,cf.pop(key),commentslist)


    #Добавляем оставшиеся параметры
    for key in cf.keys(): addkey(nlines,key,cf[key],commentslist)

    #Схороняем
    if nlines:
        f=open(get_default_config_file_name(), 'w' if sys.version_info[0] > 2 else 'wb')
        try:
            for l in nlines:
                f.write(l)
        finally:
            f.close()



def get_default_config_file_name():
    #'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'.
    
    if ('posix' in os.name) or ('mac' in os.name):
        #home = os.getenv("HOME")
        #if not home:
        #    raise IOError("Home directory not defined, don't know where to look for config file")
        #return os.path.join(home, '.EmerCoin/emercoin.conf') 
        os.path.expanduser('~/.EmerCoin/emercoin.conf')
    elif 'nt' in os.name:
        return os.path.join(os.getenv('APPDATA'), 'EmerCoin\emercoin.conf')
    else:
        raise("Unsupported OS:%s"%os.name)
    
def read_default_config():
    """
    Read default configuration from the current user's home directory.
    """
    try:
        return read_config_file(get_default_config_file_name())
    except (IOError,ValueError):
        return {} # Cannot read config file, ignore

def write_default_config(cfg):
    add_to_config_file(get_default_config_file_name(),cfg)

def getconf():
    return get_default_config_file_name()


"""
# JSON-RPC options (for controlling a running Emercoin/emercoind process)

# server=1 tells Emercoin to accept JSON-RPC commands.
#server=1

# You must set rpcuser and rpcpassword to secure the JSON-RPC api
#rpcuser=Ulysseys
#rpcpassword=YourSuperGreatPasswordNumber_385593

# By default, only RPC connections from localhost are allowed.  Specify
# as many rpcallowip= settings as you like to allow connections from
# other hosts (and you may use * as a wildcard character):
#rpcallowip=10.1.1.34
#rpcallowip=192.168.1.*

# Listen for RPC connections on this TCP port:
rpcport=8332

# You can use Emercoin or emercoind to send commands to Emercoin/emercoind
# running on another host using this option:
rpcconnect=127.0.0.1

# Use Secure Sockets Layer (also known as TLS or HTTPS) to communicate
# with Emercoin -server or emercoind
#rpcssl=1

# OpenSSL settings used when rpcssl=1
rpcsslciphers=TLSv1+HIGH:!SSLv2:!aNULL:!eNULL:!AH:!3DES:@STRENGTH
rpcsslcertificatechainfile=server.cert
rpcsslprivatekeyfile=server.pem
"""

import string
import random

def generate_random_pass(n=24):
    a = string.ascii_letters + string.digits
    return ''.join([random.choice(a) for i in range(n)])



def is_config_connectable():
    cfg=read_default_config()
    if not cfg: return 0
    if ('server' not in cfg) or (not cfg['server']) or (cfg['server']=='0'): return 0
    return 1

def make_config_connectable():
    cfg=read_default_config()
    if not cfg:
        print("config not found. creating...")
    else:
        if __name__ == "__main__":
            print("config exists. Server %s"%"ENABLED" if ('server' in cfg and cfg['server']) else "DISABLED")

    def addifnone(cfg,key,val):
        if key not in cfg:
            cfg[key]=val
            return 1
        else:
            return 0

    if ('server' not in cfg) or (not cfg['server']) or (cfg['server']=='0'):
        #сервер не настроен
        cfg['server']=1
        addifnone(cfg,'rpcuser',"defaultuser")
        addifnone(cfg,'rpcpassword',generate_random_pass())
        addifnone(cfg,'rpcport',8332)
        addifnone(cfg,'rpcconnect','127.0.0.1')

    write_default_config(cfg)

if __name__ == "__main__":
    if not is_config_connectable():
        make_config_connectable()
    print(read_default_config())
