#define R_pin 11  // присваиваем имя RED для пина 11
#define G_pin 12 // присваиваем имя GRN для пина 12
#define B_pin 13  // присваиваем имя BLU для пина 13
int ser;
int R = 0;
int G = 0;
int B = 0;
int Time = 1000;
void setup() {
 pinMode(R_pin, OUTPUT);  // используем Pin11 для вывода
 pinMode(G_pin, OUTPUT); // используем Pin12 для вывода
 pinMode(B_pin, OUTPUT);  // используем Pin13 для вывода
 Serial.begin(9600);
 Serial.setTimeout(5);
}

void loop() {
  ser = 1;
  delay(100);
  Serial.println(ser);
  if (Serial.available() > 0){
    ser = 0;
    Serial.println(ser);
    R = Serial.parseInt(); 
    G = Serial.parseInt();
    B = Serial.parseInt();
    Time = Serial.parseInt();
    digitalWrite(R_pin, R);
    digitalWrite(G_pin, G);
    digitalWrite(B_pin, B);
    delay(5000);
  }

  int R = 0;
  int G = 0;
  int B = 0;
}
