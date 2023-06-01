int buzzPin = 4;
int smokeDetect = A0;
int ledPin = 2;
 
void setup() {
  Serial.begin(9600);
  pinMode(buzzPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(smokeDetect, INPUT);
}

void loop() {
  Serial.println(analogRead(smokeDetect));

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

      // 3 is buzzer on
      case '3':
        digitalWrite(buzzPin, HIGH);
        break;

      // 4 is buzzer off
      case '4':
        digitalWrite(buzzPin, LOW);
        break;
      
      default:
        break;
    }
  }
}
