#define pirPin 12

long unsigned int lowIn;
boolean lockLow = true;
boolean takeLowTime;
int PIRValue = 0;

void setup() {
   Serial.begin(115200);
   pinMode(pirPin, INPUT);
}

void loop() {
   int detection = PIRSensor();

   Serial.println(detection);
   delay(1000);
}

int PIRSensor() {
   if(digitalRead(pirPin) == HIGH) {
      if(lockLow) {
         PIRValue = 1;
         lockLow = false;
         delay(50);
      }
      takeLowTime = true;
   }
   if(digitalRead(pirPin) == LOW) {
      if(takeLowTime){
         lowIn = millis();
         takeLowTime = false;
      }
      if(!lockLow && millis() - lowIn > 500) {
         PIRValue = 0;
         lockLow = true;
         delay(50);
      }
   }
   return PIRValue;
}
