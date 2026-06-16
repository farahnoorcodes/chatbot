import datetime   # library to select greetings according to time
import time
presenthour= datetime.datetime.now().hour # function to find the current hour
name = input("enter your name: ") # to get the name of the user, to give greetings
if 5<= presenthour<=12:
    print(" Good Morning ", name)
elif 12<= presenthour<=17:
    print(" Good Afternoon",name)
elif 17<= presenthour<=21:
    print(" Good Evening",name)
else:
    print(" Good Night",name)
print("|==========CHATBOT=========|") # actual conversation start here
print("===start the conversation===")
def chatbotresponse(userchat):#function to get desired response
    
    if userchat in["hello","hi","hey","salam","assalamualiakum"]:
        print("Bot : hey!! how can i help you?")
    elif userchat in["I'm fine.","I'm fine. how about you?","im fine","im ok","I'm okay","im okay"]:
        print("Bot : nice. good to know that:)")
    elif userchat in ["im depressed","motivate me","advice me","what should i do"]:
        print("bot : don't worry . every bug of your code help you to become a better developer (*-*) ")
    elif userchat in ["how are you","how r u","hru","what about u",]:
        print("Bot : I'm fine. how are you?")
    elif userchat in ["tell me about python","what is python","what python can do","what is the easiest computer language","what is the most efficient computer language ","what is the efficient computer language"]:
        print("Bot : python is the easiest and most efficient computer language for last 20 years. it can do AI") 
    elif userchat in ["what's your name","what is you name","your name","who are you","introduce yourself","yourself"]:
        print("Bot : I'm your python AI chatbot assistant! created by FARAH NOOR")  
    elif userchat in ["what time it is","tell me the time","tell me the current time","time"]:
        presenthour= datetime.datetime.now().hour
        print("Bot : it's ",presenthour)    
    elif userchat in ["what date it is","tell me the date","tell me the current date","date"]:
        presentmonth= datetime.datetime.now().date().month
        presentday= datetime.datetime.now().date().day
        presentyear= datetime.datetime.now().date().year
        print("Bot : it's ",presentday,"/",presentmonth,"/",presentyear)    
    else: # if the user chat is out of the knowledge or stored memoery of the bot
        print("I'm not getting your point , plz clear what you are saying")

while True:
    userchat=input("you : ").lower().strip()
     # functions to get all the input in the lower case and remove extra spaces
    bot_response=chatbotresponse(userchat)#function call
    if userchat in["quit","bye","see you next time","allah hafiz","exit"]:
        # exit condition to close the chat
        print("Bot : okieee goodbye!!!")
        break # exit the loop
    