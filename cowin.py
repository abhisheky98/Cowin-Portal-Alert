# -*- coding: utf-8 -*-
"""
Created on Fri May 21 10:21:02 2021

@author: Abhishek
"""

#Import Libraries
import requests
import json
import time
import datetime
import smtplib

#Define Constants
PINCODE = "<your pincode>" #Example 600040
MY_EMAIL = "<your email>" #From this mail id, the alerts will be sent
MY_PASSWORD = "<your password>" #Enter the email id's password

#Derive the date and url
#url source is Cowin API - https://apisetu.gov.in/public/api/cowin
today = time.strftime("%d/%m/%Y")
print(today)
url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={today}"

#Write a loop which checks for every 1000 seconds
while True:
    #Start a session
    with requests.session() as session:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = session.get(url, headers=headers)

        #Receive the response
        response = response.json()
        for center in response['centers']:
            for session in center['sessions']:

                #For Age not equal to 45 and capacity is above zero
                if (session['min_age_limit'] != 45) & (session['available_capacity'] > 0):
                    message_string=f"Subject: {today}'s Alert'!! \n\n Available - {session['available_capacity']} in {center['name']} on {session['date']} for the age {session['min_age_limit']}"

                    #Configure GMAIL settings
                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(MY_EMAIL, MY_PASSWORD)
                        connection.sendmail(
                            from_addr=MY_EMAIL,
                            to_addrs=["<email where alert is to be sent >"], #for multiple receipients, add another email id after a comma in the list
                            msg=message_string
                        )
                        print("hello")
        time.sleep(1000)
                 