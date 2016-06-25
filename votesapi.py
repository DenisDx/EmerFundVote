#!/usr/bin/python
# -*- coding: UTF-8 -*-

#модуль обеспечения связи с сервером голо сований

import json
import jsonstorage
import requests

class votesapi():
    def load_config(self,file_name=None):
        fn=file_name if file_name else self.config_file_name
        if fn:
            self.config=jsonstorage.load_json_config(fn)

    def save_config(self,file_name=None):
        fn=file_name if file_name else self.config_file_name
        if fn:
            jsonstorage.save_json_config(self.config,fn)

    def __init__(self,config_file_name=None,config=None):
        self.config=config
        self.config_file_name=config_file_name
        if not self.config_file_name:
            self.config_file_name = jsonstorage.get_home_config_file_name('EmerFundVotes')
        if (self.config is None) and self.config_file_name:
            self.load_config()

    def do_request(self,req,data,config=None):
        if not config: config=self.config
        #url = "http://%s:%s"%('localhost',config['rpcport'])
#        url = "http://%s/vote/vote.php"%(config['connection']['host'])
        url = "http://%s/vote/%s.php"%(config['connection']['host'],req)
        headers = {'content-type': 'application/json'}
        try:
            res = requests.post(url, data=json.dumps(data), headers=headers)
        except:
            print('Connection problem')
            return {}
        if res:
            try:
                return res.json()
            except:
                print('Wrong server responce:',res.content)
                return {}
        else:
            print('Empty server responce')
            return {}

    def get_votes(self, only_active=1):
        data={}
        #if only_active: data['end_date']
        return self.do_request('list',data)

    def test(self):
        print('Current config=',self.config)
        if not self.config:
            self.config={'jsonrpc':1,'connection':{'host':'128.199.60.197'}}
        self.save_config()
        print(self.do_request("list",""))
        print(self.get_votes())


def votesapi_self_test():
    x=votesapi().test()

if __name__ == "__main__":
    votesapi_self_test()
