import time
import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from datetime import datetime
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk


Temperature=[]
Time=[]
new_data={}
temp2=0
flag1=0
fan_value=0
heater_value=0
setpoint_value=0
flag=0


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "add the end point"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "add the crt file"
PATH_TO_PRIVATE_KEY = "add the private key"
PATH_TO_AMAZON_ROOT_CA_1 = "add the root CA"
#MESSAGE = "Fan"
TOPIC = "outTopic"
TOPIC2 = "mTopic"
RANGE = 20



def customCallback(client, userdata,message):
    global messages
    global temp2
    global flag1
    global flag2
    global fan_value
    global heater_value
    global setpoint_value
    global fan_value_display
    global heater_value_display

    messages=str(message.payload.decode("utf-8"))
    flag1=int(messages[58])
    flag2=int(messages[69])
    fan_value = int(messages[35])
    heater_value = int(messages[47])
    if fan_value==0:
        fan_value_display="OFF"
    elif fan_value==1:
        fan_value_display="ON"
    if heater_value ==0:
        heater_value_display="OFF"
    elif heater_value ==1:
        heater_value_display="ON"

    try:
        temp2=float((messages[79]+messages[80]+messages[81]+messages[82]))
    except ValueError:
        temp2=0
    try:
        setpoint_value = float((messages[96] + messages[97] + messages[98] + messages[99]))
    except ValueError:
        setpoint_value=0


    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    Graph()


root = tk.Tk()
root.title("Control")
root.title('Temperature Control System')
root.geometry("1500x920")
root.iconbitmap('C:/add the address of the pi/R.ico')

mode=StringVar()
fan=StringVar()
heater=StringVar()
setpoint=IntVar()


fan_on = PhotoImage(file = r"add the address of the pic\on.png")
fan_off = PhotoImage(file = r"add the address of the pic\off.png")
set_btn = PhotoImage(file = r"add the address of the pic\set.png")

def Fan_on():
    global fan
    fan='on'
    Publish()

def Fan_off():
    global fan
    fan='off'
    Publish()

Fan_on_img = Image.open('on.png')
Fan_on_img = Fan_on_img .resize((100,100), Image.Resampling.LANCZOS)
fanon_img= ImageTk.PhotoImage(Fan_on_img)

button = Button(root, text="set", image=fanon_img, command=Fan_on, font= ('Helvetica 30 bold'), compound= LEFT, width=300, height=100)
button.place(x=30,y=200)

Fan_off_img = Image.open('off.png')
Fan_off_img = Fan_off_img .resize((100,100), Image.Resampling.LANCZOS)
fanoff_img= ImageTk.PhotoImage(Fan_off_img)

button = Button(root, text="reset", image=fanoff_img, command=Fan_off,  font= ('Helvetica 30 bold'), compound= LEFT, width=300, height=100)
button.place(x=30,y=310)

def Heater_on():
    global heater
    heater='on'
    Publish()

def Heater_off():
    global heater
    heater='off'
    Publish()


heater_set_img = Image.open('HeaterOn.jfif')
heater_set_img = heater_set_img .resize((100,100), Image.Resampling.LANCZOS)
Heater_set_img= ImageTk.PhotoImage(heater_set_img)

button = Button(root, text="heater_set", command=Heater_on, image=Heater_set_img, font= ('Helvetica 20 bold'), compound= LEFT, width=300, height=100)
button.place(x=30,y=560)

heater_reset_img = Image.open('HeaterOff.jfif')
heater_reset_img = heater_reset_img .resize((100,100), Image.Resampling.LANCZOS)
Heater_reset_img= ImageTk.PhotoImage(heater_reset_img)

button = Button(root, text="heater_reset", command=Heater_off, image=Heater_reset_img, font= ('Helvetica 20 bold'), compound= LEFT, width=300, height=100)
button.place(x=30,y=670)

radio_state = StringVar()
def radio_used():
    global mode
    mode=radio_state.get()
    Publish()

#Variable to hold on to which radio button value is checked.

radiobutton1 = Radiobutton(text="Automatic", value='Automatic', variable=radio_state, command=radio_used,tristatevalue=0,font=('Helvetica 40 bold'))
radiobutton2 = Radiobutton(text="Manual", value='Manual', variable=radio_state, command=radio_used,tristatevalue=0,font=('Helvetica 40 bold'))
radiobutton1.place(x=1100,y=30)
radiobutton2.place(x=30,y=30)


#Entries
entry = Entry(root,font=('Helvetica 30 bold'),width=10)
#Gets text in entry
print(entry.get())
entry.place(x=1160,y=160)

e = Label(root, text="Set a setpoint",font=('Helvetica 20 bold'),width=20)
e.place(x=1100,y=110)
temp_display_txt = Label(root, text="Temperature Value",font=('Helvetica 20 bold'),width=20)
temp_display_txt.place(x=1100,y=420)
setpoint_display_txt = Label(root, text="Setpoint Value",font=('Helvetica 20 bold'),width=20)
setpoint_display_txt.place(x=1100,y=620)


def setpoint():
    global setpoint
    setpoint=float(entry.get())
    Publish()

Setpoint_img = Image.open('set.png')
Setpoint_img = Setpoint_img.resize((100,100), Image.Resampling.LANCZOS)
setpoint_img= ImageTk.PhotoImage(Setpoint_img)

button = Button(root,text="set", image=setpoint_img, command=setpoint,font= ('Helvetica 30 bold'), compound= LEFT,width=215, height=100)
button.place(x=1160,y=220)

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(TOPIC, 1, customCallback)


def Subscribe():
    myAWSIoTMQTTClient.connect()
    myAWSIoTMQTTClient.subscribe(TOPIC, 1, customCallback)


def Publish():
    global flag2

    if mode == 'Manual':

        if fan == 'on':
            flag2 = 0
            message1 = 1
            myAWSIoTMQTTClient.publish(TOPIC2, json.dumps(message1), 1)
            print("Published: '" + json.dumps(message1) + "' to the topic: " + "'mTopic'")

        elif fan == 'off':
            flag2 = 0
            message2 = 0
            myAWSIoTMQTTClient.publish(TOPIC2, json.dumps(message2), 1)
            print("Published: '" + json.dumps(message2) + "' to the topic: " + "'mTopic'")

        if heater == 'on':
            flag2 = 0
            message3 = 3
            myAWSIoTMQTTClient.publish(TOPIC2, json.dumps(message3), 1)
            print("Published: '" + json.dumps(message3) + "' to the topic: " + "'mTopic'")

        elif heater == 'off':
            flag2 = 0
            message4 = 2
            myAWSIoTMQTTClient.publish(TOPIC2, json.dumps(message4), 1)
            print("Published: '" + json.dumps(message4) + "' to the topic: " + "'mTopic'")

    elif mode=='Automatic':
        myAWSIoTMQTTClient.disconnect()
        myAWSIoTMQTTClient.connect()

        flag2=1
        message5 = {"Device_ID": "esp32_609F1C",
                   "Fan": fan_value,
                   "Heater": heater_value,
                   "Flag1": 1,
                   "Flag2": flag2,
                   "Temp": temp2,
                   "Setpoint": setpoint,
                   "time_stamp": 1030}

        myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message5), 1)
        print("Published: '" + json.dumps(message5) + "' to the topic: " + "'outTopic'")
        myAWSIoTMQTTClient.disconnect()
        Subscribe()


def Graph():
    global flag
    print(flag)
    now = datetime.now()
    second = now.second
    # H:M:S
    dt_string = now.strftime("%H:%M:%S")
    print("time =", dt_string)
    print(second)
    flag = 1
    if len(Temperature)<100:
        Temperature.append(temp2)


    elif len(Temperature)>=100:

        for i in range(99):
            Temperature[i] = Temperature[i+1]
        Temperature[99]=temp2
    if len(Time)<100:
        Time.append(dt_string)
    elif len(Time) >= 100:
        flag=1
        for i in range(99):
            Time[i] = Time[i+1]
        Time[99] = dt_string
    new_data["time"]=Time
    new_data["temp"] = Temperature
    print(new_data)
    print(len(Temperature))

    if flag == 1:
        df2 = pd.DataFrame(new_data)
        figure2 = plt.Figure(figsize=(7, 7), dpi=100)
        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, root)
        line2.get_tk_widget().place(x=400,y=70)
        df2 = df2[['time', 'temp']].groupby('time').sum()
        df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
        ax2.set_title('Temperature Vs. Time')

    setpoint_display = StringVar()
    setpoint_display.set(str(setpoint_value))
    setpoint_display_win = Label(root, textvariable=setpoint_display, font=('Helvetica 40 bold'), relief="solid", fg='gray')  # shows as text in the window
    setpoint_display_win.place(x=1220, y=680)
    temp_display = StringVar()
    temp_display.set(str(temp2))
    temp_display_win= Label(root, textvariable=temp_display, font=('Helvetica 40 bold'), relief="solid", fg='gray')  # shows as text in the window
    temp_display_win.place(x=1220, y=480)
    fan_display = StringVar()
    fan_display.set("          Fan is " + fan_value_display +"          ")
    fan_display_win = Label(root, textvariable=fan_display, font=('Helvetica 20 bold'), relief="solid", bg='green')  # shows as text in the window
    fan_display_win.place(x=30, y=160)
    heater_display= StringVar()
    heater_display.set("        Heater is " + heater_value_display +"       ")
    heater_display_win = Label(root, textvariable=heater_display, font=('Helvetica 20 bold'), relief="solid", bg='red')  # shows as text in the window
    heater_display_win.place(x=30, y=520)

root.mainloop()










            
