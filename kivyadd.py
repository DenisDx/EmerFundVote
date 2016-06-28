#!/usr/bin/kivy
# -*- coding: UTF-8 -*-


import kivy
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App

class MessageBox(App):
    def __init__(self, parent, titleheader="Message", message="", options={"OK": ""}, size_hint=(.8,.2), font_size=None,  size=None, modal=0):
    #def build(self, parent, titleheader="Message", message="", options={"OK": ""}, size_hint=(.8,.2),  size=(None, None)):
        def popup_callback(instance):
            self.retvalue = instance.text
            self.popup.dismiss()


        self.parent = parent
        self.retvalue = None
        self.titleheader = titleheader
        self.message = message
        self.options = options
        self.font_size=font_size
        if size: self.size = size
        else: self.size=(0,0)
        if size_hint: self.size_hint=size_hint

        #box = GridLayout(orientation='vertical', cols=1)
        box = GridLayout(cols=1)
        box.orientation='vertical'
        #self.add_widget(box)
        #box.add_widget(Label(text=self.message, font_size=self.font_size))
        box.add_widget(Label(text=self.message))
        b_list =  []
        buttonbox = BoxLayout(orientation='horizontal',size_hint=(1, None),height=32)
        box.add_widget(buttonbox)
        for b in self.options:
            b_list.append(Button(text=b, on_press=popup_callback))
            #b_list[-1].bind(on_press=self.popup_callback)
            buttonbox.add_widget(b_list[-1])
        if modal:
            #Допилить
            self.popup = ModalView()
            self.popup.title=titleheader
            self.popup.size_hint=self.size_hint
            self.popup.size=self.size
            self.popup.add_widget(box)
        else:
            self.popup = Popup(title=titleheader, content=box, size_hint=self.size_hint, size=self.size)
        #self.popup = Popup(title=titleheader, content=box, size_hint=self.size_hint)
        self.popup.open()
        self.popup.bind(on_dismiss=self.OnClose)

    def OnClose(self, event):
        self.popup.unbind(on_dismiss=self.OnClose)
        self.popup.dismiss()
        if self.retvalue != None and self.options[self.retvalue] != "":
            command = "self.parent."+self.options[self.retvalue]
            exec(command)
    def dismiss(self):
        self.retvalue = 'dismiss'
        self.popup.dismiss()

from threading import Thread
from time import sleep


#Это класс для запуска функции в отдельном потоке, которая показывает окно ожидания пока эта функция работает, а потом его закрывает
class ThreadMessageBox(App):
    def __init__(self,function,fargs,parent,**kwargs):
        self.terminated = False
        self.parent=parent
        self.kwargs=kwargs
        self.function=function
        self.fargs=fargs
        Thread(target=self.work_cycle).start()
        self.dlg = MessageBox(self.parent,**self.kwargs)
    def work_cycle(self):
        #dlg = MessageBox(self.parent,**self.kwargs)
        self.function(**self.fargs)
        self.dlg.dismiss()
    def close(self):
        self.terminated = True

class ModalDialog(App):
    #полная херня
    def __init__(self,parent,**kwargs):
        from kivy.base import EventLoop
        self.result=None
        dlg = MessageBox(parent,**kwargs)
        while (dlg) and (self.result is None):
                EventLoop.idle()
        return self.result

if __name__ == '__main__':
    class MessageBoxTest(App):
        def open_alert(self,message=''):
            if not (message is str):message='test message'
            MessageBox(parent=self,titleheader='Test alert',message=message, size_hint=(.9,None), size=(0,200))
            #MessageBox(self,'Test alert','This is alert')
            #MessageBox()
        def open_yn(self,*args):
            dlg = MessageBox(parent=self, titleheader="YN header", message="Message", size_hint=(.9,.4),
                             options=({"YES": "open_alert(message='YES!')", "NO": "open_alert(message='NO!')","CANCEL": ""}))
        def testmsg(self,a):
            MessageBox(self,"a=%s"%a)


        def open_3(self,*args):
            self.ffoptions=({"a=1": "testmsg(1)", "a=2": "testmsg(2)","CANCEL": ""})
            MessageBox(self, options=self.ffoptions)

        def open_modalview(self,*args):
            self.a=0
            MessageBox(self, modal=1, options=({"a=1": "a=1", "a=2": "a=2","CANCEL": ""}))

        def open_modal(self,*args):
            res = ModalDialog(self, titleheader="ModalView mode", message="Message\nMessage\nMessage\nMessage\n", options=({"result=1": "testmsg(1)", "result=2": "testmsg(2)","CANCEL": ""}))
            MessageBox(self,"res=%s"%res)

        def long_time_work(self,steps):
            r=100000.
            for i in range(steps):
                r=r/(i+1)+r*i
            print(r)

        def open_tmb(self,*args):
            ThreadMessageBox(self.long_time_work,{'steps':1000000},self, size_hint=(.9,.4), titleheader="ThreadMessageBox test", message="Подождите, \nне спешите...\n", options=({"Stop": ""}))

        def build(self):
            bl=BoxLayout(orientation= 'vertical')
            bl.add_widget(Button(text='Test alert', on_press=self.open_alert))
            bl.add_widget(Button(text='Test yn', on_press=self.open_yn))
            bl.add_widget(Button(text='Test 3', on_press=self.open_3))
            bl.add_widget(Button(text='Modalview test', on_press=self.open_modalview))
            bl.add_widget(Button(text='Modal test', on_press=self.open_modal))

            bl.add_widget(Button(text='ThreadMessageBox test', on_press=self.open_tmb))
            return bl
    MessageBoxTest().run()