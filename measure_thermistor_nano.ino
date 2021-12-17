void setup() {
  Serial.begin(115200);
}

void loop(){
  if(Serial.available() > 0){
    char dummy = 0;
    //Empty serial buffer
    while(Serial.available() > 0){
      dummy = Serial.read();
    }
    float x = 0.0;
    //Average 100 ADC measurements
    for(byte j=0; j<100; j++){
      x += analogRead(A0);
    }
    x /= 100.0;
    Serial.println(x,2);
  }
}
