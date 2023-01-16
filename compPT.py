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
from kivy.clock import Clock
from kivy.uix.tabbedpanel import TabbedPanel
import requests
from kivy.uix.camera import Camera
import time
import datetime
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
# import firestore
# from firestore import Collection

Window.size = (400,700) #sets screen size

Window.clearcolor = (1, 1, 1, 1) #sets bg colour
databaseURL = "https://silverwallets-c13d5.firebaseio.com" #url to get the firebase database
#print(os.path.abspath("silverwallets-c13d5-firebase-adminsdk-aurvr-bbbeab4a0c.json"))
cred_obj = credentials.Certificate(os.path.abspath("silverwallets-c13d5-firebase-adminsdk-aurvr-bbbeab4a0c.json")) #os path gets the path of the json file so it will work flawlessly on other devices
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': databaseURL,
});
# app = firebase_admin.initialize_app();
db = firestore.client();
receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt'
receiptInfo = '' 
userPW = '' 
userEmail = ''
def stringToDict(x): #converts json string into dict in python
    dictionary = dict(subString.split("=") for subString in x.split(";"))
    return(dictionary)

class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass
class HomeScreen(Screen):
    
    x = [2,3,5,6,7]
    y = [32,54,1,4,3]
    plt.plot(x,y)
    plt.xlabel("X")
    plt.ylabel("Y")
    
    welcome_text = StringProperty("")

    def __init__(self,**kwargs): 
        super(HomeScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.welcomeString, 1) #need this to constaly update the screen as everything will be run at startup once
        #box = self.ids['box']
        #box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def welcomeString(self,dt):
        self.welcome_text = 'Welcome {},'.format(userEmail.split('@')[0]) #splits user email for use in welcome screen
        #print(self.welcome_text)
        #print(userEmail,'1')

class ManualInputScreen(Screen):
    arrData = []
    current_date = ''
    date_label = StringProperty('')
    tag = StringProperty('')
    status_info =StringProperty('')
    def onButtonClicked(self):
        pass
    def text_field_amount(self, widget):
        self.tf_amount = widget.text.strip()
    def submitData(self):
        try:
            if self.tf_amount == '' or self.current_date == '' or self.tag == '':
                #ask to enter value
                self.status_info = "Error! Empty fields."
            else:
                self.status_info = "Successfully added"

                
                #print(self.current_date)
                arr = self.current_date.split('-')
                #print(arr)
                temp = datetime.datetime(int(arr[0]), int(arr[1]), int(arr[2]))
                day = temp.weekday()
                #print(day)
                self.arrData.append(self.current_date)
                self.arrData.append(day)
                self.arrData.append(self.tf_amount)
                self.arrData.append(self.tag)
                print(self.arrData)
                # send to firebase
                self.arrData = [] #clears data to avoid dupe
        except AttributeError:
            self.status_info = "Error! Empty Fields."


    def on_save(self,instance,value,date_range):
        self.date_label = str(value)
        self.current_date = str(value)
        
    def showDatePicker(self):
        Window.size = (400,701)
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()
     
class NavigationScreen(Screen):
    pass
class InputScreen(Screen):
    pass
class HistoryScreen(Screen):
    pass
class CameraScreen(Screen):
    def capture(self):
        global receiptInfo
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        temp = "IMG_{}.png".format(timestr) #adds timestamp to avoid
        camera.export_to_png(temp)
        print("Captured")
        imageFile = temp
        r = requests.post(receiptOcrEndpoint, data = { \
        'api_key': 'TEST',        # Use 'TEST' for testing purpose \
        'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
        'ref_no': 'ocr_python_123', # optional caller provided ref code \
        }, \
        files = {"file": open(imageFile, "rb")}) #^^ sends data to a receipt ocr API to process and return data
        receiptInfo = r.text #receives data in JSON string
        
        print(receiptInfo)
        
class PostCameraScreen(Screen):
    global receiptInfo 

    #screen for after reciept captured
    pass 
def LogInCheck(x,y):
    doc_ref = db.collection(u'accounts').document(x)
    if doc_ref.get().exists: #checks if doc exists before proceeding to avoid crash
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
        self.text_input_email = widget.text.strip() #values from text field
    def on_text_validate_pw(self, widget):
        self.text_input_pw = widget.text.strip()
    def signup_to_firebase(self):
        global userEmail
        global userPW
        #print(self.text_input_email)
        #ref = db.collection(u'accounts').document(u'dMo8Os9D5xwAWwgNtqIr');
        try: #validation checks
            if self.text_input_email == '' or self.text_input_pw == '':
                print('empty fields')
                self.status_info = "Error! Empty fields."
            else:
                if LogInCheck(self.text_input_email, self.text_input_pw) == True:
                    userEmail = self.text_input_email
                    self.status_info = "Correct, logging in"
                    self.manager.current = "navigate" #sends to main screen
                    
                else:
                    self.status_info = "Incorrect Details"
                    
        except AttributeError: #to prevent crashing if nothing entered
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
