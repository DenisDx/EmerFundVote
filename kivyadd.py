import kivy
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App

class MessageBox(App):
    def __init__(self, parent, titleheader="Message", message="", options={"OK": ""}, size_hint=(.8,.2), font_size=0,  size=None):
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
        def build(self):
            bl=BoxLayout(orientation= 'vertical')
            bl.add_widget(Button(text='Test alert', on_press=self.open_alert))
            bl.add_widget(Button(text='Test yn', on_press=self.open_yn))
            return bl
    MessageBoxTest().run()