import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.hivemq.com'
port = 1883
topic = "IFSC/metrologia/parquimetro"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,  msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def msg_loop(client, msg):
    while True:
        publish(client, msg)
        time.sleep(1)


def run():
    client = connect_mqtt()
    client.loop_start()

    msg_loop(client, "pinto")


if __name__ == '__main__':
    run()
