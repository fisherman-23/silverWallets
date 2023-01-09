from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
import firebase_admin
from firebase_admin import credentials, firestore
import os
from kivymd.app import MDApp
from kivy.lang import Builder

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

userPW = '' 
userEmail = ''
def stringToDict(x):
    dictionary = dict(subString.split("=") for subString in x.split(";"))
    return(dictionary)

class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass
class HomeScreen(Screen):
    pass
class NavigationScreen(Screen):
    pass
class InputScreen(Screen):
    pass
class HistoryScreen(Screen):
    pass

def LogInCheck(x,y):
    doc_ref = db.collection(u'accounts').document(x)
    if doc_ref.get().exists:
        #now check for password 
        data = doc_ref.get().to_dict()
        pw = data.get(' pw ')
        #print(pw)
        #print(type(pw))

        if pw.strip() == y: #TAKE Note: firebase stores values with spacings use strip
            #print('true',pw,type(pw))
            return True
        else:
            #print('false',pw,type(pw),y)
            return False
            
    else:
        return False
    
class LogInScreen(Screen):
    status_info = StringProperty("")
    def on_text_validate_email(self, widget):
        self.text_input_email = widget.text.strip()
    def on_text_validate_pw(self, widget):
        self.text_input_pw = widget.text.strip()
    def signup_to_firebase(self):
        global userEmail
        global userPW
        #print(self.text_input_email)
        #ref = db.collection(u'accounts').document(u'dMo8Os9D5xwAWwgNtqIr');
        try:
            if self.text_input_email == '' or self.text_input_pw == '':
                print('empty fields')
                self.status_info = "Error! Empty fields."
            else:
                if LogInCheck(self.text_input_email, self.text_input_pw) == True:
                    self.status_info = "Correct, logging in"
                    self.manager.current = "navigate"
                    
                else:
                    self.status_info = "Incorrect Details"
                    
        except AttributeError:
            #print('a',self.text_input_email,self.text_input_pw)
            self.status_info = "Please fill in the fields"

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
        global userEmail
        global userPW
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
                    userEmail = self.text_input_email
                    userPW =  self.text_input_pw
                    self.status_info = "Success!"
        except AttributeError:
            self.status_info = "Please fill in the fields"
        


class MainWidget(Widget):
    pass

class SilverWalletsApp(MDApp):
    pass
    

SilverWalletsApp().run()
