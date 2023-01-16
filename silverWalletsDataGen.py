import random
import datetime
print("silverWallets data generator V1 by ojs")
n = int(input("28/29/30/31, days in month "))
month = int(input("enter month in terms of its position in year 1,2... "))
rent = str(input("user rents? T|F"))
arr = []
totalArr = []
cost = 0.0
for i in range(1,n):
	#reserve last day for utils/savings/rent
	arr = []
	date = "2023-{}-{}".format(month,i)
	temp = date.split('-')
	day = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2])).weekday()
	cost = round(random.uniform(5.0,20.0),1)
	arr.append(date)
	arr.append(day)
	arr.append(cost)
	arr.append("food")
	totalArr.append(arr)
	arr = []
	r = random.randint(0,10)
	if r > 5:
		#extra
		cost = round(random.uniform(10.0,50.0),1)
		
		arr.append(date)
		arr.append(day)
		arr.append(cost)
		arr.append("extra")
		totalArr.append(arr)
		arr = []
	r = random.randint(1,10)
	if r > 5:
		#essential
		cost = round(random.uniform(20.0,70.0),1)
		arr.append(date)
		arr.append(day)
		arr.append(cost)
		arr.append("essential")
		totalArr.append(arr)
		arr = []
		r = random.randint(0,100)
		if r > 10:
			cost = round(random.uniform(10.0,200.0),1)
			
		arr.append(date)
		arr.append(day)
		arr.append(cost)
		arr.append("itemgoal")
		totalArr.append(arr)
		arr = []
arr = []	
date = "2023-{}-{}".format(month,i)
temp = date.split('-')
day = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2])).weekday()
if rent =="T":
	cost = round(random.uniform(1000.0,2500.0),1)
	arr.append(date)
	arr.append(day)
	arr.append(cost)
	arr.append("rent")
	totalArr.append(arr)
	arr = []
else:
	
	cost = round(random.uniform(50.0,150.0),1)
	arr.append(date)
	arr.append(day)
	arr.append(cost)
	arr.append("elec")
	totalArr.append(arr)
	arr = []
	
	cost = round(random.uniform(100.0,200.0),1)
	arr.append(date)
	arr.append(day)
	arr.append(cost)
	arr.append("water")
	totalArr.append(arr)

arr = []
r = random.randint(1,50)
if r < 10:
	cost = round(random.uniform(100.0,500.0),1)
	arr.append(cost)
	arr.append(day)
	arr.append(date)
	arr.append("savings")
	totalArr.append(arr)
	arr=[]
print(totalArr)
