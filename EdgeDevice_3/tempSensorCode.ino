int fanPin = 7;
int ledPin = 2;
int tempSensor = A0;
 
void setup() {
  Serial.begin(9600);
  pinMode(fanPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(tempSensor, INPUT);
}

void loop() {

  float voltage = (analogRead(tempSensor) * 5.0) / 1024;
  // Print the temperature in Celsius
  Serial.println((voltage - 0.5) * 100);

  if (Serial.available()){
    int input = Serial.read();

    switch(input){
      // 1 is led on
      case '1':
        digitalWrite(ledPin, HIGH);
        break;
      
      // 2 is led off
      case '2':
        digitalWrite(ledPin, LOW);
        break;

      // 3 is fan on
      case '3':
        digitalWrite(fanPin, HIGH);
        break;

      // 4 is fan off
      case '4':
        digitalWrite(fanPin, LOW);
        break;
      
      default:
        break;
    }
  }
}