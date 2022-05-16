from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import time
import json


# Connection constants
TOKKEN = "snz5ChFVQUv7Y6b3kfLY"
ID = "e0ef8d40-d548-11ec-af97-53d20f5a6d2d"

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


# Instance client connection and configure it
client = TBDeviceMqttClient("127.0.0.1", token=TOKKEN, port=1883, quality_of_service=0)



if __name__ == "__main__":
    
    # Connect to ThingsBoard
    client.connect()
    
    try:
        # Sending telemetry without checking the delivery status
        result = client.send_telemetry(payload)
        print("[MQTT] Result of sending message: ", result.get())
        time.sleep(10)  
    except:
        client.disconnect()



# # Sending telemetry and checking the delivery status (QoS = 1 by default)
# result = client.send_telemetry(telemetry)
# # get is a blocking call that awaits delivery status  
# success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
# # Disconnect from ThingsBoard
# client.disconnect()