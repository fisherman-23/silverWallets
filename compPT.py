from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
import firebase_admin
from firebase_admin import credentials, firestore
import os
# import firestore
# from firestore import Collection

Window.size = (400,700)
Window.clearcolor = (1, 1, 1, 1)
databaseURL = "https://silverwallets-c13d5.firebaseio.com"
#print(os.path.abspath("silverwallets-c13d5-firebase-adminsdk-aurvr-bbbeab4a0c.json"))
cred_obj = credentials.Certificate(os.path.abspath("silverwallets-c13d5-firebase-adminsdk-aurvr-bbbeab4a0c.json")) #os path gets the path of the json file so it will work flawlessly on other devices
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': databaseURL,
});
# app = firebase_admin.initialize_app();
db = firestore.client();

userEmail = ''

def stringToDict(x):
    dictionary = dict(subString.split("=") for subString in x.split(";"))
    return(dictionary)

class StartScreen(Screen):
    pass

class SignUpScreen(Screen): #screen property allows switch between, layout nested inside
    email_info = StringProperty("")
    status_info = StringProperty("")
    
    def on_text_validate_email(self, widget): #function that gets value of email text field when confirm button pressed
        self.text_input_email = widget.text.strip()
        print(self.text_input_email)

    def on_text_validate_pw(self, widget):
        self.text_input_pw = widget.text.strip()
        print(self.text_input_pw)

    def on_text_validate_target(self, widget):
        self.text_input_target = widget.text.strip()
        print(self.text_input_target)
    
    def signup_to_firebase(self):
        #print(self.text_input_email)
        #ref = db.collection(u'accounts').document(u'dMo8Os9D5xwAWwgNtqIr');
        try:
            if self.text_input_email == '' or self.text_input_pw == '' or self.text_input_target == '':
                print('empty fields')
                self.status_info = "Error! Empty fields."
            else:
                str = " pw = {}; target = {}; data = []".format(self.text_input_pw,self.text_input_target)
                ref = db.collection(u'accounts')
                if ref.document(self.text_input_email).get().exists: #prevents override of exisitng data
                    print("already exists!")
                    self.status_info = "Error! Already exists, try logging in"
                else:
                    ref.document(self.text_input_email).set(stringToDict(str));
        except AttributeError:
            self.status_info = "Please fill in the fields"
        
        

class MainWidget(Widget):
    pass

class SilverWalletsApp(App):
    pass
SilverWalletsApp().run()
