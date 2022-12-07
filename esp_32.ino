/* ESP32 AWS IoT
 *  
 * This is a modified version of the example of using an ESP32 with AWS IoT by Author: Anthony Elder.
 *
 */ 
#include <WiFiClientSecure.h>
#include <PubSubClient.h> 
#include <DallasTemperature.h>
#include <ArduinoJson.h>
#include <limits.h>

#include <DHT.h>
#define DHT_SENSOR_PIN  13
#define DHT_SENSOR_TYPE DHT11
DHT dht_sensor(DHT_SENSOR_PIN, DHT_SENSOR_TYPE);
#define switch1 17
#define switch2 23


int var1;
const char* ssid = "add the SSID";
const char* password = "add the Password";
int var2;
int var3;
int var4=0;
float var5;
const char* awsEndpoint = "add the AWS ENDPOINT";


// xxxxxxxxxx-certificate.pem.crt
const char* certificate_pem_crt = \

"-----BEGIN CERTIFICATE-----\n" \
"add the certificate_pem_crt here";

// xxxxxxxxxx-private.pem.key
const char* private_pem_key = \

"add the private_pem_key here";


const char* rootCA = \
"-----BEGIN CERTIFICATE-----\n" \
"add the rootCA here";

WiFiClientSecure wiFiClient;
void msgReceived(char* topic, byte* payload, unsigned int len);
PubSubClient pubSubClient(awsEndpoint, 8883, msgReceived, wiFiClient); 


void setup() {
  Serial.begin(115200); delay(50); Serial.println();
  pinMode(switch1,OUTPUT);
  pinMode(switch2,OUTPUT);
  Serial.println("ESP32 AWS IoT Example");
  Serial.printf("SDK version: %s\n", ESP.getSdkVersion());

  Serial.print("Connecting to "); Serial.print(ssid);
  WiFi.begin(ssid, password);
  WiFi.waitForConnectResult();
  Serial.print(", WiFi connected, IP address: "); Serial.println(WiFi.localIP());
  dht_sensor.begin(); // initialize the DHT sensor
  Serial.println("Dallas Temperature IC Control Library Demo");
  wiFiClient.setCACert(rootCA);
  wiFiClient.setCertificate(certificate_pem_crt);
  wiFiClient.setPrivateKey(private_pem_key);
}

unsigned long lastPublish;
int msgCount;

void loop() {
  float tempC = dht_sensor.readTemperature();
  pubSubCheckConnect();
  char msg[128];
  
  
  if (millis() - lastPublish > 10000) {
    sprintf(msg, "{\"Device_ID\":\"esp32_609F1C\", \"Fan\":%d, \"Heater\":%d, \"Flag1\":%d, \"Flag2\":%d, \"Temp\":%.1f, \"Setpoint\":%.1f, \"time_stamp\":%d}", var1, var2, var3, var4, tempC, var5, millis()/1000);
    boolean rc = pubSubClient.publish("outTopic", msg);
    Serial.print("Published, rc="); Serial.print( (rc ? "OK: " : "FAILED: ") );
    Serial.println(msg);
    lastPublish = millis();
    Serial.print("Requesting temperatures...");
    Serial.println("DONE");
    Serial.print("Temperature for Device 1 is: ");
    Serial.print(tempC);
  }

}

void msgReceived(char* topic, byte* payload, unsigned int length) {
  Serial.print("incoming: ");
  Serial.println(topic);
  if (strcmp(topic,"inTopic")== 0)
  {
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload);
    const char* message = doc["message"];
    Serial.println();
    
    for (int i = 0; i < length; i++) 
    {
      Serial.print((char)payload[i]); 
    }
      char switches = (char)payload[0];       
      Serial.print("Command: ");
      Serial.println(switches);
    if (switches == 49) 
    {
      digitalWrite(switch1, HIGH);
      Serial.println("The switch of Fan becomes ON");
      var1=1;
    }
    else if (switches == 48) 
    {
      digitalWrite(switch1, LOW);
      Serial.println("The switch of Fan becomes OFF");
      var1=0;
    }
    else if (switches == 50) 
    {
      digitalWrite(switch2, LOW);
      Serial.println("The switch of Heater becomes OFF");
      var2=0;
    }
    else if (switches == 51) 
    {
      digitalWrite(switch2, HIGH);
      Serial.println("The switch of Heater becomes OFF");
      var2=1;
    }
    Serial.println();
  }
  else if (strcmp(topic,"mTopic")== 0)
  {
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload);
    const char* message = doc["message"];
    Serial.println();
    for (int i = 0; i < length; i++) 
    {
      Serial.print((char)payload[i]); 
    }
      char switches = (char)payload[0]; 
      Serial.print("Command: ");
      Serial.println(switches);
    if (switches == 49) 
    {
      var4=0;
      digitalWrite(switch1, HIGH);
      Serial.println("The switch of Fan becomes ON");
      var1=1;
    }
    else if (switches == 48) 
    {
      var4=0;
      digitalWrite(switch1, LOW);
      Serial.println("The switch of Fan becomes OFF");
      var1=0;
    }
    else if (switches == 50) 
    {
      var4=0;
      digitalWrite(switch2, LOW);
      Serial.println("The switch of Heater becomes OFF");
      var2=0;
    }
    else if (switches == 51) 
    {
      var4=0;
      digitalWrite(switch2, HIGH);
      Serial.println("The switch of Heater becomes OFF");
      var2=1;
    }
    Serial.println();
  }
  else if(strcmp(topic,"setTopic")== 0)
  {
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload);
    const char* message = doc["message"];
    Serial.println();
    
    for (int i = 0; i < length; i++) 
    {
      Serial.print((char)payload[i]); 
    }
      var4=1;
      var5 = (float)(((int)(char)payload[0]-48)*10+(int)(char)payload[1]-48)+(float)((int)(char)payload[3]-48)*0.1;
      var3 = 0;
      
      Serial.print("Command: ");
      Serial.println(var5);
    
    Serial.println();

  }
}

void pubSubCheckConnect() {
  if ( ! pubSubClient.connected()) {
    Serial.print("PubSubClient connecting to: "); Serial.print(awsEndpoint);
    while ( ! pubSubClient.connected()) {
      Serial.print(".");
      pubSubClient.connect("ESPthingXXXX");
      delay(1000);
    }
    Serial.println(" connected");
    pubSubClient.subscribe("inTopic");
    pubSubClient.subscribe("mTopic");
    pubSubClient.subscribe("setTopic");
  }
  pubSubClient.loop();
}
