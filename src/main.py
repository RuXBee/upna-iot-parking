import random
import time
import minimalmodbus
from tb_device_mqtt import TBDeviceMqttClient
import serial

# MQTT Thingsboard connection constants
TOKKEN = "78bZrkitNCo5CbfpHaZy"
ID = "e108a700-df6e-11ec-aa3d-f1baa053ab77"
# Instance client connection and configure it
client = TBDeviceMqttClient("127.0.0.1", token=TOKKEN, port=1883, quality_of_service=1)

# Initialize modbus Instrument as master
slave_id = 13
modbus = minimalmodbus.Instrument(port="COM5", slaveaddress=slave_id, mode=minimalmodbus.MODE_RTU)
ADDRESS_IS_THERE_PRESENCE = 2

# Message
payload = {"datetime": "xxxxx",
           "parking": "UPNA",
           "p1": False,
           "p2": False,
           "p3": False,
           "p4": False,
           "p5": False,
           "p6": False,
           "p7": False,
           "p8": False,
           "p9": False,
           "p10": True,
           "p12": True,
           "p13": True,
           "p14": True,
           "p15": True,
           "p16": True,
           "p17": True,
           "p18": True,
           "p19": True,
           "p20": True,
           }


if __name__ == "__main__":
    
    print( "Possible message results:\n\
           -----------------------------  \n\
          | TB_ERR_AGAIN = -1           | \n\
          | TB_ERR_SUCCESS = 0          | \n\
          | TB_ERR_NOMEM = 1            | \n\
          | TB_ERR_PROTOCOL = 2         | \n\
          | TB_ERR_INVAL = 3            | \n\
          | TB_ERR_NO_CONN = 4          | \n\
          | TB_ERR_CONN_REFUSED = 5     | \n\
          | TB_ERR_NOT_FOUND = 6        | \n\
          | TB_ERR_CONN_LOST = 7        | \n\
          | TB_ERR_TLS = 8º             | \n\
          | TB_ERR_PAYLOAD_SIZE = 9     | \n\
          | TB_ERR_NOT_SUPPORTED = 10   | \n\
          | TB_ERR_AUTH = 11            | \n\
          | TB_ERR_ACL_DENIED = 12      | \n\
          | TB_ERR_UNKNOWN = 13         | \n\
          | TB_ERR_ERRNO = 14           | \n\
          | TB_ERR_QUEUE_SIZE = 15      | \n\
           -----------------------------")
    
    # Connect to ThingsBoard
    client.connect()
    
    last_time_s = time.process_time()
    last_value = 0
    while 1:
        try:
            # Sending telemetry without checking the delivery status
            current_time_s = time.process_time()
            
            if time.process_time() - last_time_s > 1:
                last_time_s = time.process_time()
                current_value = int(modbus.read_register(registeraddress=ADDRESS_IS_THERE_PRESENCE, functioncode=3))
                if current_value != last_value:
                    last_value = current_value
                    for key in payload:
                        if type(payload[key]) == bool:
                            payload[key] = bool(random.randint(0,1))
                    
                    payload["p1"] = current_value
                    result = client.send_telemetry(payload)
                    print("[MQTT] Result: ", result.get())
        
        except KeyboardInterrupt:
            print("[STOP] Exit from main program...")
            client.disconnect()
            break
