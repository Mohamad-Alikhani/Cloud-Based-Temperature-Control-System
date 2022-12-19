# Temperature-Control-System
A cloud based temperature control system
![image](https://user-images.githubusercontent.com/29564698/205453877-c041bfcc-cfa1-45d8-8b87-39132bebce1b.png)

ESP-32-WROOM is programmed by Arduino IDE 2.0.2 software. In this program there are three topics (inTopic, mTopic and setTopic) for subscribing and one topic(outTopic) for publishing to the cloud. In “Manual” mode the UI publishes to mTopic to turn on/off the fan and the heater. In “Automatic” mode, AWS cloud subscribes to “outTopic” to receive the data published by the IoT device and publishes to “inTopic” to turn on/off the fan and the heater. 

![image](https://user-images.githubusercontent.com/29564698/206272387-31360a84-f828-481c-950d-b8466c718c0a.png)

The defined project’s algorithm:

	The IoT device publishes the temperature every ten seconds. 
	The UI receives the JSON file and draws the temperature diagram, and it includes two modes (Manual, Automatic).
	When the mode is on “Automatic”, the AWS Event checks the temperature reacts and publishes data to the IoT device to control the temperature based on written rules.
	When the mode is on “Manual” the AWS Event doesn’t work and UI can control the fan and heater by publishing the data to the IoT device directly.

This user interface is an “.exe” file which is able to run in all PCs. The UI sub-scribes to AWS broker and when the IoT device publishes the data as a JSON file it draws and updates temperature diagram real-time. It shows the temperature and setpoint values, the fan/heater condi-tions, temperature diagram for almost one hour and a blank box for entering the setpoint. 

This project is a prototype of a temperature control system. The most advantage of this system is that it is designed cloud-based, therefore not only are we able to ex-tend the IoT devices easily, but also the system can easily interconnect to other de-fined systems in the cloud to do different scenarios. 

<img width="685" alt="image" src="https://user-images.githubusercontent.com/29564698/208336100-f22577d4-3ae0-4f9e-b11a-ce0e33efc3d7.png">
