#matplotlib & financial math formulas
#Importin gthe relevant modules
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import date
from datetime import datetime
import calendar
import time
import random
import datetime

def ASLModel(totalArr,income):

    #Finding the current month and year
    today = datetime.datetime.now()
    cyear = today.year
    cmonth = today.month

    #Naming variables for the coordinates of the graph
    date_x = []
    spending_y = []
    ASL = []
    #Naming variables for the algorithm
    total = 0
    income_a = 0
    water_a = 0
    elec_a = 0
    rent_a = 0
    food_a = 0
    extras = 0
    total_debt = 0

    #Allows the graph to be updated
    #plt.ion()

    #Input for monthly income
    income_a = float(income)
    #Input for savings for the month, and ensures that the saving amount is reasonable
    saving_a = float(1200)
    #Adds the saving amount to the total savings as well as the total amount spent for the month
    saving = 0
    saving += saving_a
    total += saving_a
    #Adds the coordinates for the Advisory Spending Limit, the first y value, the spending amount for each day, the second y value, along with the coordinates for the date, the x value
    for x in range(1,calendar.monthrange(cyear,cmonth)[1]+1):
        date_x.append(x)
        ASL.append((income_a-(93.4+42.9+2200))/calendar.monthrange(cyear,cmonth)[1])
        spending_y.append(0)
    #Factors in the savings for the month into the Advisory Spending Limit for the first day of the month
    ASL[0] += saving_a
    spending_y[0] += saving_a
    #Adding values to the respective variables to keep track of the spending
    for i in totalArr:
        plt.clf()
        year = int(i[0].split('-')[0])
        month = int(i[0].split('-')[1])
        day = int(i[0].split('-')[2])
        tag = i[3]
        amt = float(i[2])
        if month == cmonth:
                if tag == 'water':
                    ASL[day-1] += 93.4
                if tag == 'elec':
                    ASL[day-1] += 42.9
                if tag == 'rent':
                    ASL[day-1] += 2200
                if tag == 'extras':
                    spending = amt
                    extras += spending
                    spending_y[day-1] += spending
                elif tag == 'water':
                    water_a = amt
                    spending_y[day-1] += water_a
                    total += water_a
                elif tag == 'elec':
                    elec_a = amt
                    spending_y[day-1] += elec_a
                    total += elec_a
                elif tag == 'rent':
                    rent_a = amt
                    spending_y[day-1] += rent_a
                    total += rent_a
                elif tag == 'food':
                    spending = amt
                    food_a += spending
                    spending_y[day-1] += spending
                    total += spending
                elif tag == 'debt':
                    spending = amt
                    total_debt -= spending
                    spending_y[day-1] += spending
                    total += spending
                else:
                    spending = amt
                    extras += spending
                    spending_y[day-1] += spending
                    total += spending
                    
    return(cyear,cmonth,date_x,ASL,spending_y,income_a,total,water_a,income_a,elec_a,rent_a,saving_a,food_a,extras,total_debt)




    #Print the relevant Spending information
    #print('Total spent:',total)
    #print('Total remaining:',income_a - total)
    #print('Total debt:',total_debt)
    #print('Total savings;',saving)
