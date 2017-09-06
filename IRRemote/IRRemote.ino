#include <IRremote.h>           
int IR_PIN = 8;      
IRrecv irrecv(IR_PIN);
decode_results IRResults;        

void setup(){
  Serial.begin(9600);
  irrecv.enableIRIn();   
}

void loop() {
  if (irrecv.decode(&IRResults)) {
    Serial.println(IRResults.value, HEX);
    irrecv.resume();
  }
}
