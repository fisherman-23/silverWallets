#MAIN FILE
from kivy.app import App
from kivy.uix.label import Label
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
from datetime import datetime, timedelta
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.scrollview import ScrollView
from ast import literal_eval
from kivy.uix.recycleview import RecycleView
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
import json
import re
import calendar
from decimal import Decimal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor as RFR
from sklmodel import predict_spending
from financial import ASLModel
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' #a sequence of characters that specifies a search pattern in text, used for the following email valdiaiton function
Window.size = (550,800) #sets screen size

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
selectedData = []
amount = ''
tax = ''
payMeth = ''
mlStatusString = ''
aslStatusString = ''
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
class MLGraph(BoxLayout):
    temp = []
    
    def plotMLGraph(self,dt):
        #plt figure 1 refers to the mpl figure for MLGraph
        plt.figure(1)
        global mlStatusString
        doc_ref = db.collection(u'accounts').document(userEmail)
        data = doc_ref.get().to_dict()
        userData = literal_eval(data.get(u'data').strip()) #gets data from database
        totalArr = userData
        verification,predictions,days_of_week = predict_spending(totalArr)
        # verification will be True if data instance is more than 30, *required for RMSE to be reasonable
        if verification == True:
            if self.temp != totalArr: #would not update if data still the sames
                five_days_ago = datetime.now() - timedelta(days=5)
                formatted_date = five_days_ago.strftime("%Y-%m-%d") # format as year-month-day string
                day = formatted_date.split('-')[2] #gets the respective day,monht year values
                month = formatted_date.split('-')[1]
                year = formatted_date.split('-')[0]
                arr = []
                for i in totalArr: #gets the values for past 5 days
                    if int(i[0].split('-')[0]) == int(year):
                        if int(i[0].split('-')[1]) == int(month):
                            if int(i[0].split('-')[2]) > int(day) and int(i[0].split('-')[2]) <= int(datetime.now().strftime("%Y-%m-%d").split('-')[2]):
                                arr.append(i)
                indiv_sum =0
                date_sum = []
                arr2 = arr
                for x in range(-2, len(arr2)-1): #gets the sum for each day
                    if arr2[x][0] == arr2[x+1][0]:
                        indiv_sum += float(arr2[x][2])
                    else:
                        indiv_sum += float(arr2[x][2])
                        date_sum.append([arr2[x][0],arr2[x][1],indiv_sum])
                        indiv_sum = 0 
                date_sum.append(date_sum[0]) 
                date_sum.pop(0)
                date_sum.pop(len(date_sum)-1) 

                spending_dict = {}
                past_days = date_sum
                # loop over the past_days array and add the spending value to the dictionary
                for day in past_days: 
                    spending_dict[datetime.strptime(day[0], '%Y-%m-%d').date()] = day[2]

                # create an array of the past 5 dates
                dates = [datetime.now().date() - timedelta(days=i) for i in range(4,-1,-1)]

                # create an array to hold the spending values for each date
                spending_array = []

                # loop over the past 5 dates and add the spending value from the dictionary if it exists,
                # or add 0 if it doesn't exist
                for date in dates:
                    if date in spending_dict:
                        spending_array.append(spending_dict[date])
                    else:
                        spending_array.append(0)

                self.temp = totalArr
                plt.cla() #clears all the values in graph, clean state
                self.clear_widgets()
                plt.scatter(days_of_week, predictions)
                plt.ylabel("Prediction Amount of Money Spent/$")
                plt.xlabel("Days")
                mlStatusString = "Predicted Spendings: ${},${},${},${},${}\n Previous Week's Spendings: ${}, ${}, ${}, ${}, ${}".format(round(predictions[0]),round(predictions[1]),round(predictions[2]),round(predictions[3]),round(predictions[4]),round(spending_array[0]),round(spending_array[1]),round(spending_array[2]),round(spending_array[3]),round(spending_array[4]))
                self.add_widget(FigureCanvasKivyAgg(plt.gcf()))  
        else:
            plt.cla()
            self.clear_widgets()
            mlStatusString = 'More Data Required (30 Days)'
            self.add_widget(FigureCanvasKivyAgg(plt.gcf())) #plots the graph onto the screen
    def __init__(self,**kwargs): 
        super().__init__(**kwargs)
        Clock.schedule_interval(self.plotMLGraph, 9)
class FinanceGraph(BoxLayout):
    temp = []
    def plotASLGraph(self,dt):
        global aslStatusString
        #plt figure 2 refers to the figure for ASLGraph
        plt.figure(2)
        doc_ref = db.collection(u'accounts').document(userEmail)
        data = doc_ref.get().to_dict()
        userData = literal_eval(data.get(u'data').strip())
        totalArr = userData
        target = literal_eval(data.get(u'target').strip())
        saving = literal_eval(data.get(u'saving').strip())
        if self.temp != 0:
            #Formatting the graphs
            plt.cla()
            plt.clf()
            self.clear_widgets()
            self.temp = totalArr
            cyear,cmonth,date_x,ASL,spending_y,income_a,total,water_a,income_a,elec_a,rent_a,saving_a,food_a,extras,total_debt = ASLModel(self.temp,target,saving)
            plt.subplot(2,1,1) #creates diff subplots for bar graph and pie chart
            plt.xlabel('Date')
            plt.ylabel('Spending (SGD)')
            plt.xticks(range(1,calendar.monthrange(cyear,cmonth)[1]+1))
            plt.plot(date_x,ASL,color='red')
            plt.bar(date_x,spending_y,color='green')
            remaining = income_a - total
            plt.subplot(2,1,2)
            #Deciding if the pie chart should show 'Remaining' or 'Debt' depending if you overspent or not
            if remaining >= 0:
                labels = ['Water Bills','Electricity Bills','Rent','Savings','Food','Extras','Remaining']
                piechart = np.array([water_a*100/income_a, elec_a*100/income_a, rent_a*100/income_a, saving_a*100/income_a, food_a*100/income_a, extras*100/income_a, (remaining*100/income_a)])
            else:
                remaining *= -1
                total_debt += remaining
                labels = ['Water Bills','Electricity Bills','Rent','Savings','Food','Extras','Debt']
                piechart = np.array([water_a*100/total, elec_a*100/total, rent_a*100/total, saving_a*100/total, food_a*100/total, extras*100/total, remaining*100/total])
            #Formatting the piechart
            perSpending = piechart.tolist()#converts np array to python list
            labels = [f'{l}, {s:0.1f}%' for l, s in zip(labels, perSpending)]
            plt.pie(piechart)
            plt.legend(piechart, labels=labels, loc='lower left', prop={"size":7})
            self.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            aslStatusString = 'Total Spent: ${}\nTotal Remaining: ${}\n Total Debt: ${}'.format(round(total,2),round(income_a-total,2),round(total_debt,2))
    def __init__(self,**kwargs): 
        super().__init__(**kwargs)
        Clock.schedule_interval(self.plotASLGraph, 10)
        #self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    
class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass
class HomeScreen(Screen):
    welcome_text = StringProperty("")
    ml_status_info = StringProperty("")
    asl_status_info = StringProperty("")
    def __init__(self,**kwargs): 
        super(HomeScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.welcomeString, 1) #need this to constaly update the screen as everything will be run at startup once
        #box = self.ids['box']

    def welcomeString(self,dt):
        global mlStatusString
        global aslStatusString
        self.welcome_text = 'Welcome {},'.format(userEmail.split('@')[0]) #splits user email for use in welcome screen
        self.ml_status_info = mlStatusString
        self.asl_status_info = aslStatusString
        #print(self.welcome_text)
        #print(userEmail,'1')
class SettingScreen(Screen):
    status_info = StringProperty('')
    def log_out(self):
        global userEmail
        global userPW
        userEmail = 'guest'
        userPW = ''
        self.manager.current = "start"
        #self.manager.transition.direction = 'right'
    def update_income(self):
        self.incomeAmt = self.ids['income'].text.strip() #gets value from input field
        global userEmail
        try: #data verfication
            if self.incomeAmt == '':
                print('empty fields')
                self.status_info = "Error! Empty field."
            elif not float(self.incomeAmt) > 0:
                self.status_info = "Income must be more than 0"
            else:
                doc_ref = db.collection(u'accounts').document(userEmail)
                doc_ref.update({u' target ': str(self.incomeAmt)})
                self.status_info = "Successfully updated" #updates the amt in database
                self.incomeAmt = ''
                self.ids['income'].text = '' #clears data from txt field
        except AttributeError:
            self.status_info = "Please fill in the field"
    def update_saving(self):
        self.savingPer = self.ids['saving'].text.strip()
        global userEmail
        try: #data verfication
            if self.savingPer == '':
                print('empty fields')
                self.status_info = "Error! Empty field."
            elif not ((float(self.savingPer) >=20 and float(self.savingPer) <=70)):
                self.status_info = "Saving % must be between 20 and 70 inclusive"
            else:
                doc_ref = db.collection(u'accounts').document(userEmail)
                doc_ref.update({u' saving ': str(self.savingPer)})
                self.status_info = "Successfully updated" #updates the amt in database
                self.savingPer = ''
                self.ids['saving'].text = '' #clears data from txt field
        except AttributeError:
            self.status_info = "Please fill in the field"
class ManualInputScreen(Screen):
    arrData = []
    current_date = ''
    date_label = StringProperty('')
    tag = StringProperty('')
    status_info =StringProperty('')

    def submitData(self):
        global userEmail
        print(userEmail)
        self.tf_amount = self.ids['amt'].text.strip() #strip to prevent sending blank spaces
        s =  self.tf_amount#removes trailing 0 to keep data consistent
        self.tf_amount = s.rstrip('0').rstrip('.') if '.' in s else s
        print(self.tf_amount, self.current_date,self.tag)
        try:
            if self.tf_amount == '' or self.current_date == '' or self.tag == '':
                #ask to enter value
                self.status_info = "Error! Empty fields."
            elif not float(self.tf_amount) >0:
                self.status_info = "Amount must be more than 0"
            else:
                #print(self.current_date)
                arr = self.current_date.split('-')
                #print(arr)
                temp = datetime(int(arr[0]), int(arr[1]), int(arr[2]))
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
                self.current_date = ''
                self.date_label = ''
                self.tf_amount = ''
                self.tag = ''
                self.ids['amt'].text  = ''
                self.status_info = "Successfully added"
        except AttributeError:
            self.status_info = "Error! Empty Fields."


    def on_save(self,instance,value,date_range): #save func assigns value of date
        self.date_label = str(value)
        self.current_date = str(value)
        
    def showDatePicker(self): #code to show date picker and calls save function when pressed
        Window.size = (550,801)
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        global selectedData
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            print(rv.data[index])
            selectedData.append(rv.data[index]) #adds to list of selected data
        else:
            print("selection removed for {0}".format(rv.data[index])) 
            if rv.data[index] in selectedData:#this is to prevent crashing as data will be auto-registered as remove at initial start
                selectedData.remove(rv.data[index])
class History(RecycleView):
    def __init__(self, **kwargs):
        super(History, self).__init__(**kwargs)
        Clock.schedule_interval(self.refresh, 3) #code that runs every 1sec as auto refresh

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
    def submit_debt(self):
        self.debtAmt = self.ids['debt'].text.strip() #gets value from input field
        global userEmail
        try: #data verfication
            if self.debtAmt == '':
                print('empty fields')
                self.status_info = "Error! Empty field."
            elif not float(self.debtAmt) > 0:
                self.status_info = "Debt Repayment Value must be more than 0"
            else:
                year = datetime.today().strftime('%Y')
                month = datetime.today().strftime('%m')
                month = str(int(month))
                day = datetime.today().strftime('%d')
                string = '{}-{}-{}'.format(year,month,day)
                arrData = [string,datetime.today().weekday(),str(self.debtAmt),'debt']
                doc_ref = db.collection(u'accounts').document(userEmail) #gets the path of data to be sent
                data = doc_ref.get().to_dict() #converts the array into a dict format
                userData = literal_eval(data.get('data').strip()) #what is stored in firebase  
                print(userData)
                userData.append(arrData) #combines the exisitng data with data to be sent
                doc_ref.update({u' data ': str(userData)}) # send to firebase
                self.status_info = "Successfully updated" #updates the amt in database
                self.debtAmt = ''
                self.ids['debt'].text = '' #clears data from txt field
                arrData = []
        except AttributeError:
            self.status_info = "Please fill in the field"
class HistoryScreen(Screen):
    def remove(self):
        doc_ref = db.collection(u'accounts').document(userEmail)
        data = doc_ref.get().to_dict()
        userData = literal_eval(data.get('data').strip()) #what is stored in firebase  
        global selectedData
        for i in selectedData: #extracting respective values from array into variables
            temp = str(list(dict.values(i)))
            temp = temp.strip("['")
            temp = temp.strip("']")
            temp2 = temp.split('\\n')
            dateNDay = temp2[0].split(',')
            date = dateNDay[0]
            day = dateNDay[1].strip()
            #convert into int
            amtNTag = temp2[1].split(',')
            amt = str(amtNTag[0]).replace('$','')
            amt = amt.rstrip('0').rstrip('.') if '.' in amt else amt
            tag = str(amtNTag[1]).strip()
            day = time.strptime(day, "%A").tm_wday
            arr = [date,day,amt,tag]
            if arr in userData: #check if value to be deleted exists
                userData.remove(arr) #remove the value
                doc_ref.update({u' data ': str(userData)}) #update to firebase
                print('remove')
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
        global payMeth
        
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        #temp = 'receiptTest1.jpg'
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
                merchName = tempData.get('merchant_name') #gets the values from the dict
                merchAddress = tempData.get('merchant_address')
                date = tempData.get('date')
                amount = tempData.get('total')
                if amount != None and date != None: #if both have values, then proceed
                    timeData = tempData.get('time')
                    tax = tempData.get('service_charge')
                    items = tempData.get('items')
                    #items = str(items)
                    #items = items.strip('[')
                    #items = items.strip(']')
                    #items = literal_eval(items)

                    paymentMethod = tempData.get('payment_method')
                    creditCardType = tempData.get('credit_card_type')
                    print(merchName,merchAddress,date,timeData,amount,tax,paymentMethod,creditCardType)
                    if paymentMethod != None and creditCardType != None:
                        payMeth = str(paymentMethod) + str(creditCardType)
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
    payMeth = StringProperty("")
    tag = StringProperty('')
    arrData = []
    arrReceiptData = []
    def on_enter(self):
        global merchName
        global merchAddress
        global timeData
        global date
        global amount
        global tax
        global payMeth
        
        #assigns the respective str to the label
        self.merchantInfo = 'Merchant Info: '+('-' if merchName is None else str(merchName))
        self.merchantAddress = 'Address: '+('-' if merchAddress is None else str(merchAddress))
        self.date = 'Date: '+('-' if date is None else str(date))
        self.time = 'Time: '+('-' if timeData is None else str(timeData))
        self.amount = 'Amount: '+('-' if amount is None else str(amount))
        self.tax = 'Tax: '+('-' if tax is None else str(tax))
        self.payMeth = 'Payment Meth: '+('-' if payMeth is None else str(payMeth))

    def submitData(self): #submit in format -> [date, day, amt, tag]
        global userEmail
        global merchName
        global merchAddress
        global timeData
        global date
        global amount
        global tax
        global payMeth
        print(merchName, merchAddress, timeData, tax, payMeth)
        try: #guard against error crash
            if str(amount) == '' or str(date) == '' or self.tag == '':
                #ask to enter value
                self.tag = "Error! Empty fields."
            else:
                arr = str(date).split('-')

                temp = datetime(int(arr[0]), int(arr[1]), int(arr[2]))
                day = temp.weekday()
                s = str(amount)
                amount = s.rstrip('0').rstrip('.') if '.' in s else s #removes trailing 0 to keep data consistent
                #set up array for update
                self.arrData.append(str(date))
                self.arrData.append(day)
                self.arrData.append(str(amount))
                self.arrData.append(self.tag)
                print(self.arrData)

                self.arrReceiptData.append(str(date))
                self.arrReceiptData.append(day)
                self.arrReceiptData.append(str(amount))
                self.arrReceiptData.append(self.tag)
                self.arrReceiptData.append(str(merchName))
                self.arrReceiptData.append(str(merchAddress))
                self.arrReceiptData.append(str(timeData))
                self.arrReceiptData.append(str(tax))
                self.arrReceiptData.append(str(payMeth))


                doc_ref = db.collection(u'accounts').document(userEmail)
                data = doc_ref.get().to_dict()
                print(data)
                userData = literal_eval(data.get('data').strip()) #what is stored in firebase  
                userReceiptData = literal_eval(data.get('receiptData').strip())
                print(userData,userReceiptData)
                userData.append(self.arrData) #append new data to existing
                userReceiptData.append(self.arrReceiptData) #append new data to existing
                #update database
                doc_ref.update({u' data ': str(userData)}) #updates data values, this stores all data, manual and receipt
                doc_ref.update({u' receiptData ': str(userReceiptData)}) #updates receiptData values, this only stores info from receipt

                self.arrData = [] #clears data to avoid dupe
                self.arrReceiptData = []
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
        self.text_input_email = self.ids['email'].text.strip()
        self.text_input_pw = self.ids['pw'].text.strip()
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
    
    def signup_to_firebase(self):
        global userEmail
        global userPW
        self.text_input_email = self.ids['email'].text.strip() #gets values from text field
        self.text_input_pw = self.ids['pw'].text.strip()
        self.text_input_target = self.ids['limit'].text.strip()
        self.text_input_saving = self.ids['saving'].text.strip()
        try: #data verfication
            if self.text_input_email == '' or self.text_input_pw == '' or self.text_input_target == '' or self.text_input_saving == '':
                print('empty fields')
                self.status_info = "Error! Empty fields."
            else:

                str = "pw= {};target= {};data= [];receiptData= [];saving= {}".format(self.text_input_pw,self.text_input_target,self.text_input_saving) #prepare the data into a string for the firebase set() func
                ref = db.collection(u'accounts')
                if ref.document(self.text_input_email).get().exists: #prevents override of exisitng data
                    print("already exists!")
                    self.status_info = "Error! Already exists, try logging in"
                elif check(self.text_input_email) == False:
                    self.status_info = "enter a valid email"
                elif not float(self.text_input_target) >0:
                    self.status_info = 'Income must be more than 0'
                elif not ((float(self.text_input_saving) >=20 and float(self.text_input_saving) <=70)):
                    self.status_info = '% Saving must be >20% & <70%'
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
                    self.ids['saving'].text = ''
                    self.status_info = ''
                    self.manager.current = 'login'
        except AttributeError:
            self.status_info = "Please fill in the fields"
        


class MainWidget(Widget):
    pass

class SilverWalletsApp(MDApp):
    pass
    

SilverWalletsApp().run()
