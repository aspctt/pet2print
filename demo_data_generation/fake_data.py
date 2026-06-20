# /// script
# dependencies = [
#   "paho-mqtt",
# ]
# ///

import paho.mqtt.client as mqtt
import json, time, random, ssl

HIVEMQ_HOST = "21358b8f9c1d42fdbbe8a62a8b522da4.s1.eu.hivemq.cloud"
HIVEMQ_PORT = 8883
HIVEMQ_USERNAME = "pet2print-admin"
HIVEMQ_PASSWORD = "BahcesehirCapstone2026"
TOPIC = "pet2print/telemetry"

# VERSION2
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to HiveMQ Cloud")
    else:
        print(f"Connect failed: {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(HIVEMQ_USERNAME, HIVEMQ_PASSWORD)
client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)  # cloud requires TLS
client.on_connect = on_connect

client.connect(HIVEMQ_HOST, HIVEMQ_PORT)
client.loop_start()

try:
    while True:
        payload = {
            "temp": round(random.normalvariate(257.5, 1.5), 1),
            "rpm": random.normalvariate(40, 2),
            "diameter": round(random.normalvariate(1.75, 0.04), 2),
        }
        client.publish(TOPIC, json.dumps(payload))
        print("Published:", payload)
        time.sleep(2)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()