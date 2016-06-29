#!/usr/bin/kivy
# -*- coding: UTF-8 -*-

#EmerFundVoteApp

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label

from kivy.uix.textinput import TextInput

from kivy.lang import Builder
from kivy.app import App

from kivy.clock import Clock

#from kivy.uix.scrollview import ScrollView

import rpcconnet

from kivy.uix.screenmanager import ScreenManager, Screen

kv="""
<MenuScreen>:
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
                text: 'Show'
                on_press: app.show_vote_table()
        ScrollView:
            BoxLayout:
                size_hint: 1, None
                height:400

                orientation: 'vertical'
                id: votetable

        BoxLayout:
            size_hint: 1, None
            height: 32
            orientation: 'horizontal'
            Button:
                text: 'Settings'
                on_press: app.open_settings()
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
            height: 25
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
                background_color:(1,1.2,1.5,1)
                text: 'Use json'
                id: btjson
            ToggleButton:
                background_color:(1,1.2,1.5,1)
                group: "gaddsource"
                text: 'Use local wallet.dat'
                id: btwallet
            ToggleButton:
                background_color:(1,1.2,1.5,1)
                group: "gaddsource"
                text: 'Add manually'
                id: btmanual
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: 32
            Label:
                size_hint: None, 1
                width: 100
                text: "Wallet path"
            TextInput:
                id: ti_wallet_file
                text: ''
            Button:
                size_hint: None, 1
                wight: 100
                text: 'Choose...'
                id: b_wallet_file
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
                background_color:(1,1.2,1.5,1)
                text: "Sign using json api"
                id: btjsonsign
            ToggleButton
                background_color:(1,1.2,1.5,1)
                background_normal: 'atlas://data/images/defaulttheme/button'
                background_down: 'atlas://data/images/defaulttheme/button_pressed'
                group: "gsignmethod"
                text: "Sign manually"
                id: btmanualsign
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: 25
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: 32
            Label:
                text: "Addresses:"
                id: lbstate
                size_hint: None, 1
                width: 100
            Button:
                text: 'Rebuild'
                id: btrebuild
                on_press: app.rebuild_addresses_list()
            Button:
                text: 'Add manual'
                id: btmanualadd
                on_press: app.settings_manual_add_address()
        ScrollView:
            GridLayout:
                cols: 1
                size_hint: 1, None
                height: 64
                row_default_height: 32
                id: gladdresses
        Button:
            text: 'Reload config'
            size_hint: 1, None
            height: 32
            on_press: app.gui_load_config()
        Button:
            text: 'Save'
            size_hint: 1, None
            height: 32
            on_press: app.gui_save_config()
        Button:
            size_hint: 1, None
            height: 32
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
                on_release: app.debug_send(root.ids.edit1.text,root.ids.edit2.text)
        TextInput:
            id: log
        Button:
            size_hint: 1, None
            height: 32
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

from kivyadd import MessageBox
from kivyadd import ThreadMessageBox

class EmerFundVoteApp(App):
        		
    def build(self):
        #self.store = JsonStore('aocfg.json')
        #@if self.store.exists('Title'):
        #    print('Title exists:', self.store.get('Title'))
        #    #store.delete('Title')
        #else:
        #    print('NI Title exists:')
        # Create the screen manager

        #from kivy.atlas import Atlas
        #from kivy.cache import Cache
        #self.atlas= Atlas('theme-1.atlas')
        #Cache.append("kv.atlas", 'data/images/defaulttheme', self.atlas)
        

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

    #======================Конфиги
    def open_settings(self, *largs):
        self.sm.current = 'settings'
        self.gui_load_config()

    def gui_save_config(self):
        #{'jsonrpc':1,'connection':{'host':'128.199.60.197'}}
        if 'connection' not in self.votesapi.config:
            self.votesapi.config['connection']={}
        self.votesapi.config['connection']['host']= self.sm.get_screen('settings').ids.tihost.text

        if self.sm.get_screen('settings').ids.btwallet.state=='down':
            self.votesapi.config['wallet_method']='wallet'
        elif self.sm.get_screen('settings').ids.btmanual.state=='down':
            self.votesapi.config['wallet_method']='manual'
        else:
            self.votesapi.config['wallet_method']='json'

        if self.sm.get_screen('settings').ids.btmanualsign.state=='down':
            self.votesapi.config['jsonrpc_sign']=0
        else:
            self.votesapi.config['jsonrpc_sign']=1

        self.votesapi.config['wallet_file']=self.sm.get_screen('settings').ids.ti_wallet_file.text

        gl=self.sm.get_screen('settings').ids.gladdresses
        self.votesapi.config['addresses']=[]
        for c in gl.children:
            #self.sm.get_screen('settings').ids['adr%s'%n].text
            if c.children[0].state=='down':
                self.votesapi.config['addresses'].append(c.children[0].text)
        gl.height=len(gl.children)*32

        self.votesapi.save_config()


    def settings_get_addr_btn(self,addr):
        gl=self.sm.get_screen('settings').ids.gladdresses
        for c in gl.children:
            if c.children[0].text==addr:
                return c.children[0]
        return None

    def settings_get_address_label(self,b):
        #по кнопке возвращает этикетку
        return b.parent.children[1]

    def settings_add_update_address_button(self,addr,text='???'):
        b=self.settings_get_addr_btn(addr)
        if b:
            #кнопка есть
            if text!='???':
                self.settings_get_address_label(b).text=text
        else:
            #добавляем кнопку и метку
            return self.add_address_panel(len(self.sm.get_screen('settings').ids.gladdresses.children),text,addr).children[0]
        return b
    def gui_load_config(self):
        self.votesapi.load_config()

        #if ('connection' not in self.votesapi.config):
        #    self.votesapi.config['connection']={}
        if 'connection' not in self.votesapi.config or self.votesapi.config['connection']['host']=='':
            self.sm.get_screen('settings').ids.tihost.text = '128.199.60.197'
        else:
            self.sm.get_screen('settings').ids.tihost.text = self.votesapi.config['connection']['host']

        #wallet_method btjson btwallet btmanual
        if 'wallet_method' in self.votesapi.config:
            if self.votesapi.config['wallet_method']=='wallet':
                self.sm.get_screen('settings').ids.btwallet.state='down'
            elif self.votesapi.config['wallet_method']=='manual':
                self.sm.get_screen('settings').ids.btmanual.state='down'
            else:
                self.sm.get_screen('settings').ids.btjson.state='down'


        if 'jsonrpc_sign' in self.votesapi.config:
            if self.votesapi.config['jsonrpc_sign']=='1' or self.votesapi.config['jsonrpc_sign']==1:
                self.sm.get_screen('settings').ids.btjsonsign.state='down'
            else:
                self.sm.get_screen('settings').ids.btmanualsign.state='down'


        if self.sm.get_screen('settings').ids.btmanualsign.state=='down':
            self.votesapi.config['jsonrpc_sign']=0
        else:
            self.votesapi.config['jsonrpc_sign']=1

        if 'wallet_file' in self.votesapi.config:
            self.sm.get_screen('settings').ids.ti_wallet_file.text = self.votesapi.config['wallet_file']

        if 'addresses' in self.votesapi.config:
            self.rebuild_addresses_list()

        #Сбрасываем выделения
        for c in self.sm.get_screen('settings').ids.gladdresses.children:
            c.children[0].state=='normal'

        if 'addresses' in self.votesapi.config:
            for addr in self.votesapi.config['addresses']:
                #b=self.get_addr_btn(addr)
                #if b is None:
                #    self.add_address_panel(len(self.sm.get_screen('settings').ids.gladdresses.children),'???',addr)
                #    b=self.get_addr_btn(addr)
                b=self.settings_add_update_address_button(addr)
                b.state='down'

    def show_vote_table(self):
        #Удаляем текущие голосования и запускаем запрос новых
        while len(self.sm.get_screen('menu').ids.votetable.children)>0:
            self.sm.get_screen('menu').ids.votetable.remove_widget(self.sm.get_screen('menu').ids.votetable.children[0])
            #c.dismiss()

        ThreadMessageBox(self._show_vote_table,{},self, modal=1, titleheader="Information: loading data, please wait", message="Пожалуйста, подождите, идет загрузка данных голосований")
        #self._show_vote_table()
    def _show_vote_table(self):
        params={}

        if not self.votesapi.config:
            self.votesapi.load_config()
        if ('connection' not in self.votesapi.config):
            self.votesapi.config['connection']={}
        if ('host' not in self.votesapi.config['connection']) or self.votesapi.config['connection']['host']=='':
            self.votesapi.config['connection']['host'] ='128.199.60.197'

        resp=self.votesapi.do_request('list',params)

        #запуск в основном потоке
        if resp:
            self.last_vote_table_responce=resp
            Clock.schedule_once(self.show_vote_table_callback, 0.01)

    def show_vote_table_callback(self,*args):
        children_height = 32+32+16+5

        resp=self.last_vote_table_responce

        for v in resp:
            bl = BoxLayout(orientation= 'vertical',size_hint=(1, None), height=children_height)

            blt = BoxLayout(orientation= 'horizontal',size_hint=(1, None), height=32)
            blb = BoxLayout(orientation= 'horizontal')


            #votes
            blt.add_widget(ToggleButton(text='YES',on_press=self.on_vote_button_press,background_color=(1,1.2,1.5,1),size_hint=(None, 1), width=32,group='gg%s'%v['question_id'],id='by%s'%v['question_id'])) #, on_press=self.open_3
            blt.add_widget(ToggleButton(text='NO',on_press=self.on_vote_button_press,background_color=(1,1.2,1.5,1),size_hint=(None, 1), width=32,group='gg%s'%v['question_id'],id='bn%s'%v['question_id'])) #, on_press=self.open_3

            #blt.add_widget(ToggleButton(text='YES',background_color=(1,1.2,1.5,1),background_normal= '',background_down= '',size_hint=(None, 1), width=32,group='gg%s'%v['question_id'],id='by%s'%v['question_id'])) #, on_press=self.open_3
            #blt.add_widget(ToggleButton(text='NO',background_color=(1,1.2,1.5,1),background_normal= '',background_down= '',size_hint=(None, 1), width=32,group='gg%s'%v['question_id'],id='bn%s'%v['question_id'])) #, on_press=self.open_3


            #background_color=(1,1.2,1.5,1)
            #background_normal= 'atlas://data/images/defaulttheme/button'
            #background_down= 'atlas://data/images/defaulttheme/button_pressed'


            #blt.add_widget(Label(text='#%s:%s'%(v['question_id'],v['name']),size_hint=(None,1), width=200))
            #blt.add_widget(Label(text='Q:%s'%v['qmin'],size_hint=(None,1), width=50))
            #blt.add_widget(Label(text='L:%s'%v['lmin'],size_hint=(None,1), width=50))
            #blt.add_widget(Label(text='%s - %s'%(v['begin_date'],v['end_date']),size_hint=(None,1), width=200))

            blt.add_widget(Label(text='#%s:%s'%(v['question_id'],v['name']),size_hint=(.4,1)))
            blt.add_widget(Label(text='Q:%s'%v['qmin'],size_hint=(.1,1)))
            blt.add_widget(Label(text='L:%s'%v['lmin'],size_hint=(.1,1)))
            blt.add_widget(Label(text='%s - %s'%(v['begin_date'],v['end_date']),size_hint=(.4,1)))

            blb.add_widget(TextInput(text=v['descr']))

            bl.add_widget(Label(text='',size_hint=(1, None), height=5))
            bl.add_widget(blt)
            bl.add_widget(blb)
            self.sm.get_screen('menu').ids.votetable.add_widget(bl)

        if len(self.sm.get_screen('menu').ids.votetable.children)>0:
            self.sm.get_screen('menu').ids.votetable.height=len(self.sm.get_screen('menu').ids.votetable.children)*children_height
        else:
            self.sm.get_screen('menu').ids.votetable.height=400

    def on_vote_button_press(self,btn):
        if btn.parent.children[len(btn.parent.children)-1].state=='down':
            btn.parent.children[len(btn.parent.children)-1].background_color=(1,1.8,0.8,1)
        else:
            btn.parent.children[len(btn.parent.children)-1].background_color=(1,1.2,1.5,1)

        if btn.parent.children[len(btn.parent.children)-2].state=='down':
            btn.parent.children[len(btn.parent.children)-2].background_color=(5,0.7,0.4,1)
        else:
            btn.parent.children[len(btn.parent.children)-2].background_color=(1,1.2,1.5,1)

        '''
        if btn.state=='down':
            if btn.text=='YES':
                btn.background_color=(1,2,1,1)
            else:
                btn.background_color=(2,1,1,1)
        else:
            btn.background_color=(1,1.2,1.5,1)
        '''

    def debug_send(self,req,data):
        #pass
        #self.sm.get_screen('debug').ids.log.text +='\n send:'+data
        #sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Internet # UDP
        #sock.sendto(data, ("127.0.0.1", 1984))
        try:
            import json
            d=json.loads(data)
        except:
            import sys
            self.sm.get_screen('debug').ids.log.text +='\n wrong data:%s'%sys.exc_info()[1]
            return 0
        resp=self.votesapi.do_request(req,d)
        if resp:
            self.sm.get_screen('debug').ids.log.text +='\n resp:%s'%resp

    def turn_on_json(self):
        import walletconfig
        walletconfig.make_config_connectable()
        MessageBox(parent=self,titleheader='Information: you have to restart the wallet app',message='Для продолжения работы перезапустите кошелек Emercoin', size_hint=(.9,None), size=(0,300))

    def check_rpc_config(self):
        #Подключает конфигурацию доступа к кошельку по json
        #если уже подключено - ничего не делает
        if not rpcconnet.configured():
            if not rpcconnet.init_config():
                #Спрашиваем одобрение включить json и включаем ежели одобрят
                MessageBox(self, titleheader="Do you want to turn JSON RPC server on?", message="""В настоящее время функция доступа к кошельку для других приложнний отключена.
Для получения адресов и подписания голосов требуется включить эту функцию.
Потом ее можно будет отключить.

Включить сервер JSON для текущего кошелька?""", size_hint=(.9,.5), options=({"YES": "turn_on_json()", "NO (CANCEL)": ""}))
                return 0
        return 1
    def get_addresses_list(self,wallet_method=""):
        #получение списка адресов зависит от метода
        #метод определен в from_wallet
        res=[]
        if not wallet_method:
            if 'wallet_method' in self.votesapi.config:
                wallet_method=self.votesapi.config['wallet_method']
            else:
                return res

        if wallet_method=='wallet':
            return res
        elif wallet_method=='json':
            if not self.check_rpc_config(): return []
            try:
                la=rpcconnet.walreq({"method": "listaccounts","params":[],"jsonrpc": "2.0","id": 0})['result']
            except:
                MessageBox(parent=self,titleheader='Error: can\'t access wallet application',message='Приложение "кошелек Emercoin" недоступно.\nВозможно, кошелек не запущен\nили требует его перезапуска', size_hint=(.9,0.4))
                return res
            if la:
                for a in la.keys():
                    res.append((a,rpcconnet.walreq({"method": "getaddressesbyaccount","params":[a],"jsonrpc": "2.0","id": 0})['result']))
        return res

    def add_address_panel(self,n,ltext,addr):
        bl=BoxLayout(orientation= 'horizontal',size_hint=(1, None), height=32)
        bl.add_widget(Label(text=ltext,size_hint=(None,1), width=100))
        bl.add_widget(ToggleButton(text=addr,id='adr%s'%n,background_color=(1,1.2,1.5,1))) #, on_press=self.open_3

        self.sm.get_screen('settings').ids.gladdresses.add_widget(bl)
        return bl

    def settings_manual_add_address(self):
         MessageBox(self, options=({"Ok": "settings_add_update_address_button('\%s')","Cancel": ""}), edit_add=True , titleheader="Request: please enter a new address", message="Пожалуйста введите новый адрес")

    def rebuild_addresses_list(self):
        #Удаление старых элементов. Пока не практикуем.
        for c in self.sm.get_screen('settings').ids.gladdresses.children:
            pass
        ThreadMessageBox(self._rebuild_addresses_list,{},self, modal=1, titleheader="Information: loading data, please wait", message="Пожалуйста, подождите, идет загрузка данных")

    def rebuild_addresses_list_callback(self,*args):
        al=self.last_rebuild_addresses_list
        for a in al:
            for addr in a[1]:
                self.settings_add_update_address_button(addr,a[0])


    def _rebuild_addresses_list(self):
        #создание нового списка адресов в
        #import kivy.uix
        #gl=kivy.uix.gridlayout()
        #Добавляем (обновляем наименование) для новых, если они есть
        wm='json'
        if self.sm.get_screen('settings').ids.btwallet.state=='down':wm='wallet'
        elif self.sm.get_screen('settings').ids.btmanual.state=='down':wm='manual'

        #Высываем функцию основного потока
        self.last_rebuild_addresses_list = self.get_addresses_list(wm)
        if self.last_rebuild_addresses_list:
            Clock.schedule_once(self.rebuild_addresses_list_callback, 0.01)


if __name__ == '__main__':

    EmerFundVoteApp().run()