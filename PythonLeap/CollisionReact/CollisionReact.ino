void setup()
{
  Serial.begin(19200); // initialize the serial port
  Serial.print("\n Starting Spiderbot v1.1 \n");
  Serial.flush();
  
  pinMode(12, OUTPUT); // LED
  
  // initialize timer1 
  noInterrupts();           // disable all interrupts
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1  = 0;

  OCR1A = 31250;            // compare match register 16MHz/256/2Hz
  TCCR1B |= (1 << WGM12);   // CTC mode
  TCCR1B |= (1 << CS12);    // 256 prescaler 
  TIMSK1 |= (1 << OCIE1A);  // enable timer compare interrupt
  interrupts();             // enable all interrupts
}

ISR(TIMER1_COMPA_vect)          // timer compare interrupt service routine
{
  digitalWrite(13, digitalRead(13) ^ 1);   // toggle LED pin
}

void loop()
{
  char reading; //declare variable
  reading = 0x0; //initialize as null
  //if data available, take in char
  if(Serial.available())
  {
      reading = Serial.read();
  }
 
  //if char read = '1' turn on pin, else turn off pin
  if( reading == '1')
  {
      digitalWrite(12, HIGH);
      
  }
  else if(reading == '0')
  {
    digitalWrite(12,LOW);
  }
}
