#!/usr/bin/kivy
# -*- coding: UTF-8 -*-

#EmerFundVoteApp

from kivy.app import App
from kivy.uix import boxlayout
from kivy.uix import gridlayout
from kivy.uix import button
from kivy.uix import textinput
from kivy.uix import popup
from kivy.uix import label

from kivy.lang import Builder
from kivy.app import App
#from time import sleep
#import kivy.clock 

import socket
import sys

import rpcconnet

from kivy.uix.screenmanager import ScreenManager, Screen

kv="""
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                size_hint: 1, None
                height:32
                orientation: 'horizontal'
                Label:
                    size_hint: (None, 1)
                    width: 25
                    text: "D1:"
                TextInput:
                    id: d1
                Label:
                    size_hint: None, 1
                    width: 25
                    text: "D2:"
                TextInput:
                    id: d2
                Button:
                    text: 'show'
                    on_press: app.show_vote_table()
            BoxLayout:
                id: votetable

        BoxLayout:
            size_hint: 1, 0.1
            orientation: 'horizontal'
            Button:
                text: 'Settings'
                on_press: root.manager.current = 'settings'
            Button:
                text: 'Debug'
                on_press: root.manager.current = 'debug'
            Button:
                text: 'Quit'
                on_press: app.stop()

<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: 32
            Label:
                size_hint: None, 1
                width: 100
                text: "Host:"
            TextInput:
                id: tihost
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: 32
            Label:
                size_hint: None, 1
                width: 100
                text: "Add. source:"
                id: lbstate
            ToggleButton:
                group: "gaddsource"
                text: 'Use json'
                id: btjson
            ToggleButton:
                group: "gaddsource"
                text: 'Use local wallet.dat'
                id: btwallet
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: 32
            Label:
                size_hint: None, 1
                width: 100
                text: "Sign method:"
                id: lbstate
            ToggleButton
                group: "gsignmethod"
                text: "sign using json api"
                id: tbjson
            ToggleButton
                group: "gsignmethod"
                text: "sign manual"
                id: tbmanual
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: 32
            Label:
                text: "Addresses:"
                id: lbstate
            Button:
                size_hint: None, 1
                width: 55
                text: 'Rebuild'
                id: btrebuild
                on_press: app.rebuild_addresses_list()
        GridLayout:
            cols: 1
            row_default_height: 32
            id: gladdresses
        Button:
            text: 'Save'
        Button:
            size_hint: 1, 0.1
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
<DebugScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint: 1, None
            height: 32
            orientation: 'horizontal'
            Label:
                size_hint: None, 1
                width: 45
                text: "cmd:"
            TextInput:
                size_hint: None, 1
                width: 45
                text: "list"
                id: edit1
            Label:
                size_hint: None, 1
                width: 45
                text: "data:"
            TextInput:
                id: edit2
            Button:
                size_hint: 0.2, 1
                text: 'send'
                on_release: app.send(root.ids.edit1.text,root.ids.edit2.text)
        TextInput:
            id: log
        Button:
            size_hint: 1, 0.1
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
                
"""


# Declare screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class DebugScreen(Screen):
    pass


import votesapi

class EmerFundVoteApp(App):
        		
    def build(self):
        #self.store = JsonStore('aocfg.json')
        #@if self.store.exists('Title'):
        #    print('Title exists:', self.store.get('Title'))
        #    #store.delete('Title')
        #else:
        #    print('NI Title exists:')
        # Create the screen manager

        self.gui=Builder.load_string(kv)
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(DebugScreen(name='debug'))

        self.votesapi=votesapi.votesapi()

        return self.sm

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_stop(self):
        pass

    def build_votes_table(self,votes):
        pass

    def show_vote_table(self):
        #делаем запрос
        #строим грид
        votes = self.votesapi.get_votes()
        if votes:
            self.sm.get_screen('debug').ids.log.text +='\n %s votes received'%len(votes)
            self.build_votes_table(votes)
        return 1

    def send(self,req,data):
        #pass
        #self.sm.get_screen('debug').ids.log.text +='\n send:'+data
        #sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Internet # UDP
        #sock.sendto(data, ("127.0.0.1", 1984))
        import json
        try:
            d=json.loads(data)
        except:
            import sys
            self.sm.get_screen('debug').ids.log.text +='\n wrong data:%s'%sys.exc_info()[1]
            return 0
        resp=self.votesapi.do_request(req,d)
        if resp:
            self.sm.get_screen('debug').ids.log.text +='\n resp:%s'%resp

    def check_rpc_config():
        #Подключает конфигурацию доступа к кошельку по json
        #если уже подключено - ничего не делает
        if not rpcconnet.configured:
            if not rpcconnet.init_config():
                if self.ask_for_turn_json_on():
                    import walletconfig
                    walletconfig.make_config_connectable()
                    #popup = Popup(title='Allert',content=Label(text='please restart emercoin wallet'),size_hint=(None, None), size=(400, 400))
                    popup.Popup(title='Allert',content=label.Label(text='please restart emercoin wallet'),size_hint=(.8, .8))

                else:
                    return 0

    def get_addresses_list(self,from_wallet=0):
        #получение списка адресов зависит от метода
        #метод определен в from_wallet
        res=[]
        if from_wallet:
            pass
        else:
            if not self.check_rpc_config(): return []
            la=rpcconnet.walreq({"method": "listaccounts","params":[],"jsonrpc": "2.0","id": 0})['result']
            if la:
                for a in la.keys():
                    res.append(rpcconnet.walreq({"method": "getaddressesbyaccount","params":[a],"jsonrpc": "2.0","id": 0})['result'])
        return res
    def rebuild_addresses_list(self):
        #создание нового списка адресов в
        #import kivy.uix
        #gl=kivy.uix.gridlayout()
        gl=self.sm.get_screen('settings').ids.gladdresses
        for c in gl.children:
            c.dispose()
        #‘down’/checked
        from kivy.uix import modalview
        #pp=popup.Popup(title='Allert',content=label.Label(text='please restart emercoin wallet'),size_hint=(.8, .8))
        #pp=modalview.ModalView(title='Allert',content=label.Label(text='please restart emercoin wallet'),size_hint=(.8, .8))
        pp=modalview.ModalView(size_hint=(.8, .8))
        self.sm.get_screen('settings').add_widget(pp)
        pp.open()
        #popup.Popup(title='Allert',content=label.Label(text='please restart emercoin wallet'),size_hint=(.8, .8)).open()
        al=self.get_addresses_list(self.sm.get_screen('settings').ids.btwallet.state=='down')
        for a in al:
            #создаем панель высотой 32 пиксела, на ней - чекпокс и метку с адресом
            print(a)
if __name__ == '__main__':
    EmerFundVoteApp().run()