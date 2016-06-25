#!/usr/bin/kivy
# -*- coding: UTF-8 -*-

#save and load configs
#helps with file names

#выбирает имя файла автоматически если не указано
#Хранит конфиги в каталоге программы, называя их config.json если не указано иное



import json
import os
import sys

def get_home_config_file_name(project_name):
    #'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'.

    if ('posix' in os.name) or ('mac' in os.name):
        #home = os.getenv("HOME")
        #if not home:
        #    raise IOError("Home directory not defined, don't know where to look for config file")
        #return os.path.join(home, '.EmerCoin/emercoin.conf')
        os.path.expanduser('~/.'+project_name+'/config.json')
    elif 'nt' in os.name:
        return os.path.join(os.getenv('APPDATA'), project_name+'\config.json')
    else:
        raise("Unsupported OS:%s"%os.name)

def get_default_json_config_file_name():
    return os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]),'config.json'))

def load_json_config(file_name=None):
    if not file_name: file_name=get_default_json_config_file_name()
    try:
        with open(file_name, 'r') as fp:
            try:
                return json.load(fp)
            finally:
                fp.close()
    except IOError:
        return {}

def save_json_config(data,file_name=None):
    if not file_name: file_name=get_default_json_config_file_name()
    #Возможно надо создать каталог
    if not file_name: return 0
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    fp=open(file_name, 'w' if sys.version_info[0] > 2 else 'wb')
    if fp:
        try:
            json.dump(data, fp)
            return 1
            #json.dump(data, fp, sort_keys=True, indent=4)
        finally:
            fp.close()
    else: return 0

if __name__ == "__main__":
    #test
    c = load_json_config()
    if c: print('config has been read:',c)
    else:
        print('config can not be found')
        c = {'TestName1':1,'TestName2':'Text2','TestName3':[1,2,3],'TestName4':{'a':1,'b':2,'c':3}}
    save_json_config(c)
