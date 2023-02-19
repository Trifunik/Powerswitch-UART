/* Used for STM8 to switch power; Part of the Powerswitch-UART*/

int counter = 0;
int old_value = 0;

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  Serial_begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  while (Serial_available() == 0) {};
  // get incoming byte:
  int value  = Serial_read();
  Serial_write(value);    // give feedback

  if ( value == 0x0d) {
    if (counter == 2) digitalWrite(LED_BUILTIN, LOW);   // switch LED On
    if (counter == 3) digitalWrite(LED_BUILTIN, HIGH);  // switch LED Off
    counter = 0;
    old_value = 0;

  } else {
    if (counter == 0) {
      if ( value == 'o' || value == 'O') {
        counter = counter + 1; 
      }
    } else {
      switch (counter) {
        case 1:
          if ( value == 'n' || value == 'N' || value == 'f' || value == 'F') {
            counter = counter + 1;
            old_value = value;
          }
          break;
        case 2:
          if ((value == 'f' || value == 'F') && (old_value == 'f' || old_value == 'F')) {
            counter = counter + 1;
            old_value = value;
          } else {
            counter = 0;
            old_value = 0;
          }
          break;
        default:
          counter = 0;
          old_value = 0;
      }
    }
  }
}
