int potPin = A0;
int ledPin = 2;
bool motionDetected = false;
int motionPin = 7;
 
void setup() {
  Serial.begin(9600);
  pinMode(potPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(motionPin, INPUT);
}

void loop() {
  motionDetected = analogRead(motionPin);
  if (digitalRead(motionPin) == HIGH){
    motionDetected = !motionDetected;
  }

  Serial.print(motionDetected);
  Serial.print(',');
  Serial.println(analogRead(potPin));

  if (motionDetected) {
    // Since analogRead returns a value from 0 to 1023 and analogWrite takes a value from 0 to 255,
    // we need to find a way to map the read value to the write value.
    int ledValue = 127 + analogRead(potPin) * 0.125;
    analogWrite(ledPin, ledValue);
  }
  
  if (Serial.available()) {
    int input = Serial.read();

    switch (input) {
      // 1 is led on
      case '1':
        digitalWrite(ledPin, HIGH);
        break;
      
      // 2 is led off
      case '2':
        digitalWrite(ledPin, LOW);
        break;
      
      default:
        break;
    }
  }
}