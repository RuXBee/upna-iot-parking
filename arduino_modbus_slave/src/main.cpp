#include <Arduino.h>
#include "ModbusRTUSlave.h"
#include "NewPing.h"

// Configure and set values of RS485 port
const word buf_size = 256;
const uint16_t number_holding_registers = 10;
const uint16_t baud_rate = 19200;
const uint8_t slave_id = 13;
// This is the buffer for the ModbusRTUSlave object.
// It is used to store the Modbus messages.
// A size of 256 bytes is recommended, but sizes as low as 8 bytes can be used.
byte buf[buf_size];
ModbusRTUSlave modbus(Serial, buf, buf_size);

// Define modbus map with registers
struct modbusmap_t {
  uint16_t device_id = slave_id;
  uint16_t ultrasonic_sensor_cm;
  uint16_t flag_is_there_presence;
  uint16_t millis_program_counter_sec;
  uint16_t testing_value;
} modbusregs;


// Setup ultrasonic sensor configuration
#define TRIGGER_PIN  12                             // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11                             // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200                            // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
#define THRESHOLD_DISTANCE 50                       // Threshold for known if car is parked
uint32_t before = 0;

// This is a function that will be passed to the ModbusRTUSlave for reading holding registers.
long holdingRegisterRead(word address) {
  if (address == (&modbusregs.device_id - (uint16_t*)&modbusregs)) return modbusregs.device_id;
  else if (address == (&modbusregs.device_id - (uint16_t*)&modbusregs)) {
    modbusregs.ultrasonic_sensor_cm = sonar.ping_cm();
    return modbusregs.ultrasonic_sensor_cm;
  }
  else if (address == (&modbusregs.flag_is_there_presence - (uint16_t*)&modbusregs)) return modbusregs.flag_is_there_presence;
  else if (address == (&modbusregs.millis_program_counter_sec - (uint16_t*)&modbusregs)) {
    modbusregs.millis_program_counter_sec = millis()/1000;
    return modbusregs.millis_program_counter_sec;
  }
  else if (address == (&modbusregs.testing_value - (uint16_t*)&modbusregs)) {
    modbusregs.testing_value = random(1, 65000);
    return modbusregs.testing_value;
  }
  else return false;
}

// This is a function that will be passed to the ModbusRTUSlave for writing to holding registers.
boolean holdingRegisterWrite(word address, word value) {
  Serial.println("[MODBUS-0x06] Writing... ");
  if (address == (&modbusregs.testing_value - (uint16_t*)&modbusregs)) {
    digitalWrite(LED_BUILTIN, !(digitalRead(LED_BUILTIN)));
    modbusregs.testing_value = value;
  }
  return true;
}

void setup() {
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(ECHO_PIN, OUTPUT);
  pinMode(TRIGGER_PIN, OUTPUT);

  Serial.begin(19200);
  modbus.begin(slave_id, baud_rate);
  sonar.begin();

  // Configure the holdingRegister(s).
  modbus.configureHoldingRegisters(number_holding_registers, holdingRegisterRead, holdingRegisterWrite); 
}

void loop() {
  
  modbus.poll();

  if (millis() - before > 1000) {
    before = millis();
    // String message = "[PING] Distance: " + String(sonar.ping_cm()) + " Cm";
    // Serial.println(message);
    if (sonar.ping_cm() < THRESHOLD_DISTANCE) {
      modbusregs.flag_is_there_presence = 1;
      digitalWrite(LED_BUILTIN, HIGH);
    } 
    else {
      modbusregs.flag_is_there_presence = 0;
      digitalWrite(LED_BUILTIN, LOW); 
    }
  }

}
