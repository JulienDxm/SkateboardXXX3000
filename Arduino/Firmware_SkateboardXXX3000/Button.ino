void onButtonPress() {
  digitalWrite(pinLedESP, HIGH);
  buttonPressed = true;
  startPush = millis();
}

void onButtonRelease() {
  digitalWrite(pinLedESP, LOW);
  buttonFlash = false;
  buttonPressed = false;
  startPush = 0;
}

void onButtonHold() {
  buttonFlash = true;
}