#MAIN FILE
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
import numpy as np
from kivy.uix.scrollview import ScrollView
from ast import literal_eval
from kivy.uix.recycleview import RecycleView
import json
import re
import calendar
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' #a sequence of characters that specifies a search pattern in text, used for the following email valdiaiton function
Window.size = (400,700) #sets screen size

Window.clearcolor = (1, 1, 1, 1) #sets bg colour
databaseURL = "https://silverwallets-c13d5.firebaseio.com" #url to get the firebase database
#print(os.path.abspath("silverwallets-c13d5-firebase-adminsdk-aurvr-bbbeab4a0c.json"))
cred_obj = credentials.Certificate(os.path.abspath("silverwallets-c13d5-firebase-adminsdk-aurvr-bbbeab4a0c.json")) #os path gets the path of the json file auto so it will work flawlessly on other devices
default_app = firebase_admin.initialize_app(cred_obj, { #initialize the connection to firebase given the databaseURL given^^
	'databaseURL': databaseURL,
});
# app = firebase_admin.initialize_app();
db = firestore.client();
receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' #this is where the receipts will be processed
receiptInfo = '' 
userPW = '' 
userEmail = 'guest' #temp value to avoid crashing as all code will be run
merchName = ''
merchAddress = ''
timeData = ''
date = ''
category = ''
amount = ''
tax = ''
payMeth = ''
def stringToDict(x): #converts json string into dict in python
    dictionary = dict(subString.split("=") for subString in x.split(";"))
    return(dictionary)
def check(email):
    #checks if email is valid using the re library 
    #fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
class Graph(BoxLayout):
    
    signal = [7, 89.6, 45.-56.34]
    signal = np.array(signal)
    plt.plot(signal)
    plt.xlabel("X")
    plt.ylabel("Y")
    
    def __init__(self,**kwargs): 
        super().__init__(**kwargs)

        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    
class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass
class HomeScreen(Screen):
    welcome_text = StringProperty("")

    def __init__(self,**kwargs): 
        super(HomeScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.welcomeString, 1) #need this to constaly update the screen as everything will be run at startup once
        #box = self.ids['box']

    def welcomeString(self,dt):
        self.welcome_text = 'Welcome {},'.format(userEmail.split('@')[0]) #splits user email for use in welcome screen
        #print(self.welcome_text)
        #print(userEmail,'1')
class SettingScreen(Screen):
    def log_out(self):
        global userEmail
        global userPW
        userEmail = 'guest'
        userPW = ''
        self.manager.current = "start"
        #self.manager.transition.direction = 'right'

class ManualInputScreen(Screen):
    arrData = []
    current_date = ''
    date_label = StringProperty('')
    tag = StringProperty('')
    status_info =StringProperty('')
    def onButtonClicked(self):
        pass
    def text_field_amount(self, widget):
        self.tf_amount = widget.text.strip() #strip to prevent sending blank spaces
    def submitData(self):
        global userEmail
        try:
            if self.tf_amount == '' or self.current_date == '' or self.tag == '':
                #ask to enter value
                self.status_info = "Error! Empty fields."
            else:

                #print(self.current_date)
                arr = self.current_date.split('-')
                #print(arr)
                temp = datetime.datetime(int(arr[0]), int(arr[1]), int(arr[2]))
                day = temp.weekday()
                #appends all data into a single array
                self.arrData.append(self.current_date)
                self.arrData.append(day)
                self.arrData.append(self.tf_amount)
                self.arrData.append(self.tag)
                print(self.arrData)
                doc_ref = db.collection(u'accounts').document(userEmail) #gets the path of data to be sent
                data = doc_ref.get().to_dict() #converts the array into a dict format

                userData = literal_eval(data.get('data').strip()) #what is stored in firebase  
                print(userData)
                userData.append(self.arrData) #combines the exisitng data with data to be sent
                doc_ref.update({u' data ': str(userData)}) # send to firebase
                self.arrData = [] #clears data to avoid dupe
                self.status_info = "Successfully added"
        except AttributeError:
            self.status_info = "Error! Empty Fields."


    def on_save(self,instance,value,date_range): #save func assigns value of date
        self.date_label = str(value)
        self.current_date = str(value)
        
    def showDatePicker(self): #code to show date picker and calls save function when pressed
        Window.size = (400,701)
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()
        
class History(RecycleView):
    def __init__(self, **kwargs):
        super(History, self).__init__(**kwargs)
        Clock.schedule_interval(self.refresh, 1) #code that runs every 1sec as auto refresh

    def refresh(self,dt):
        global userEmail
        
        doc_ref = db.collection(u'accounts').document(userEmail)
        data = doc_ref.get().to_dict()
        userData = literal_eval(data.get(u'data').strip()) #gets data from database and puts it in an array
        self.data = [{'text': '{}, {}\n${:.2f}, {}'.format(x[0],calendar.day_name[int(x[1])],float(x[2]),x[3])} for x in userData] #puts all the data into respective string format
        #this data will be used by the recycle view in the kv file
class NavigationScreen(Screen):
    pass
class InputScreen(Screen):
    pass
class HistoryScreen(Screen):
    pass
class CameraScreen(Screen):
    status_info = StringProperty('')
    def capture(self):
        global receiptInfo
        global merchName
        global merchAddress
        global timeData
        global date
        global amount
        global tax
        global category
        global payMeth
        
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        #temp = 'swtest2.jpg'
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
        receiptInfo = receiptInfo.replace("\n", "").replace("\t", "") #clean to make it suitable for processing later on
        receiptInfo = receiptInfo.replace("\n", "").replace("\t", "")
        receiptInfo = json.loads(receiptInfo)
        print(receiptInfo)
        print(receiptInfo.get('success'))
        if receiptInfo.get('message') != 'No receipts detected.' and receiptInfo.get('success') == True:
            #prevents crash if no receipt detected
            try:
                 #if recognised as receipt, then proceed
                tempData = receiptInfo.get('receipts')
                tempData = str(tempData)
                tempData = tempData.strip('[')
                tempData = tempData.strip(']')
                tempData = tempData.replace("\n", "").replace("\t", "") #make it suitable for processing
                tempData = tempData.replace("\\n", "").replace("\t", "")
                tempData = literal_eval(tempData)
                print(tempData)
                '''merchange name
                merchant address
                date, time
                amount paid, taxes
                payment details
                category (not so sure yet)'''
                merchName = tempData.get('merchant_name')
                merchAddress = tempData.get('merchant_address')
                date = tempData.get('date')
                amount = tempData.get('total')
                if amount != None and date != None: #if both have values, then proceed
                    timeData = tempData.get('time')
                    tax = tempData.get('service_charge')
                    items = tempData.get('items')
                    category = items[0].get('category')
                    #items = str(items)
                    #items = items.strip('[')
                    #items = items.strip(']')
                    #items = literal_eval(items)
                    #category = items.get('category')
                    paymentMethod = tempData.get('payment_method')
                    creditCardType = tempData.get('credit_card_type')
                    print(merchName,merchAddress,date,timeData,amount,category,tax,paymentMethod,creditCardType)
                    self.ids['camera'].play = not self.ids['camera'].play
                    #turn off cam^^
                    self.manager.current = "postCam"
                else: #receipt lacks the critical info to proceed (date, amount)
                    self.status_info = 'Receipt lacks info, make sure receipt is clearly captured'
               
            except AttributeError:
                
                self.status_info = 'Receipt no info, make sure receipt is clealry captured'

        else:
            
            self.status_info = 'No receipt detected'
class PostCameraScreen(Screen):

    #screen for after reciept captured
    merchantInfo = StringProperty("")
    merchantAddress = StringProperty("")
    date = StringProperty("")
    time = StringProperty("")
    amount = StringProperty("")
    tax = StringProperty("")
    category = StringProperty("")
    payMeth = StringProperty("")
    tag = StringProperty('')
    arrData = []
    def on_enter(self):
        global merchName
        global merchAddress
        global timeData
        global date
        global amount
        global tax
        global category
        global payMeth
        
        #assigns the respective str to the label
        self.merchantInfo = 'Merchant Info: '+('-' if merchName is None else str(merchName))
        self.merchantAddress = 'Address: '+('-' if merchAddress is None else str(merchAddress))
        self.date = 'Date: '+('-' if date is None else str(date))
        self.time = 'Time: '+('-' if timeData is None else str(timeData))
        self.amount = 'Amount: '+('-' if amount is None else str(amount))
        self.tax = 'Tax: '+('-' if tax is None else str(tax))
        self.category = 'Category: '+('-' if category is None else str(category))
        self.payMeth = 'Payment Meth: '+('-' if payMeth is None else str(payMeth))

    def submitData(self): #submit in format -> [date, day, amt, tag]
        global userEmail
        global date
        global amount
        try: #guard against error crash
            if str(amount) == '' or str(date) == '' or self.tag == '':
                #ask to enter value
                self.tag = "Error! Empty fields."
            else:
                arr = str(date).split('-')
                #print(arr)
                temp = datetime.datetime(int(arr[0]), int(arr[1]), int(arr[2]))
                day = temp.weekday()
                #print(day)
                self.arrData.append(str(date))
                self.arrData.append(day)
                self.arrData.append(str(amount))
                self.arrData.append(self.tag)
                print(self.arrData)
                doc_ref = db.collection(u'accounts').document(userEmail)
                data = doc_ref.get().to_dict()

                userData = literal_eval(data.get('data').strip()) #what is stored in firebase  
                print(userData)
                userData.append(self.arrData)
                doc_ref.update({u' data ': str(userData)})
                # send to firebase
                self.arrData = [] #clears data to avoid dupe
                
                self.tag = "Successfully added"
                self.manager.current = "navigate"
        except AttributeError:
            self.tag = "AttributeError"
    
    
def LogInCheck(x,y):
    doc_ref = db.collection(u'accounts').document(x)
    if doc_ref.get().exists: #checks if doc exists before proceeding to avoid crash
        #now check for password 
        data = doc_ref.get().to_dict()
        pw = data.get('pw')
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
                    self.status_info = 'Success! Logging-in'
                    userEmail = self.text_input_email
                    self.text_input_email = ''
                    self.text_input_pw = ''
                    self.ids['email'].text = ''
                    self.ids['pw'].text = '' #clears data        
                    self.status_info = ""
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
        try: #data verfication
            if self.text_input_email == '' or self.text_input_pw == '' or self.text_input_target == '':
                print('empty fields')
                self.status_info = "Error! Empty fields."
            else:

                str = "pw= {};target= {};data= []".format(self.text_input_pw,self.text_input_target) #prepare the data into a string for the firebase set() func
                ref = db.collection(u'accounts')
                if ref.document(self.text_input_email).get().exists: #prevents override of exisitng data
                    print("already exists!")
                    self.status_info = "Error! Already exists, try logging in"
                elif check(self.text_input_email) == False:
                    self.status_info = "enter a valid email"
                else:
                    ref.document(self.text_input_email).set(stringToDict(str)); #creates users data in database
                    self.status_info = "Success!"
                    userEmail = self.text_input_email
                    userPW =  self.text_input_pw
                    self.text_input_email = ''
                    self.text_input_pw = ''
                    self.text_input_target = ''
                    self.ids['email'].text = ''
                    self.ids['pw'].text = '' #clears data 
                    self.ids['limit'].text = ''
                    self.status_info = ''
                    self.manager.current = 'login'
        except AttributeError:
            self.status_info = "Please fill in the fields"
        


class MainWidget(Widget):
    pass

class SilverWalletsApp(MDApp):
    pass
    

SilverWalletsApp().run()
