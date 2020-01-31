const int tempPin=A0;
void setup() {
  Serial.begin(9600);

}

void loop() {
  int tempVal=analogRead(tempPin);
  float voltage = (tempVal/1024.0)*5;
  float temperature = (voltage-0.5)*100.0;
  Serial.print(temperature);
  Serial.print("\n");
  delay(2000);
}
