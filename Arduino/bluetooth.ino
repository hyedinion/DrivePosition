#include <SoftwareSerial.h>

#define rxd 8
#define txd 7
SoftwareSerial bluetooth(rxd,txd);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  bluetooth.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(bluetooth.available()){
    char code;
    code = bluetooth.read();
    if(code == '0')//------------------------------------첫번째 인자 '0' input
    {
      bluetooth.println("10 5 30");
      Serial.print(code);
    }
    else if (code =='1')
    {
      Serial.print(code);
      Serial.print("----\n");
      String inString = bluetooth.readString();
      Serial.print(inString);
    }
  } 
  if(Serial.available()){
    //bluetooth.println("10 20 30");
    //bluetooth.write(Serial.read());
  }

}
