import paho.mqtt.client as mqtt
import random
import datetime as datetime
import time
import json

devices = {}
endpoints = [ "REST", "MQTT" ]
resources = [ "temperature", "humidity", "led", "light", "heat" ]

class Catalogue(object):
	def __init__(self, clientID, broker, port):
		self.broker = broker
		self.clientID = clientID
		self.port = port
		self.notifier = self

		self.topic = ""
		self.__paho_mqtt = mqtt.Client(clientID, False)
		self.__paho_mqtt.on_connect = self.onConnect
		self.__paho_mqtt.on_message = self.onMessage

	def onConnect(self, paho_mqtt, userdata, flag, rc):
		print("Connected to %s with result code: %d" %(self.broker, rc))
	
	def onMessage(self, paho_mqtt, userdata, msg):
		global devices
		now = datetime.datetime.now()
		device = json.loads(msg.payload)
		device["timestamp"] = now.strftime("%Y:%M:%D %H:%M:%S")
		devices[device["deviceID"]] = device
		print("\nDevice received:")
		print(device)

	def onPublish(self, topic, msg):
		print("\nPublishing '%s' with topic '%s'" %(msg, topic))
		self.__paho_mqtt.publish(topic, msg, 2)
	
	def onSubscribe(self, topic):
		print("Subscribing to '%s' with topic '%s'" % (self.broker, topic))
		self.__paho_mqtt.subscribe(topic, 2)
		self.topic = topic

	def start(self):
		self.__paho_mqtt.connect(self.broker, self.port)
		self.__paho_mqtt.loop_start()

	def stop(self):
		self.__paho_mqtt.unsubscribe(self.topic)
		self.__paho_mqtt.loop_stop()
		self.__paho_mqtt.disconnect()

if __name__ == "__main__":
	catalogue = Catalogue('device_catalogue', 'test.mosquitto.org', 1883)
	catalogue.start()	
	catalogue.onSubscribe('/tiot/group18/catalog/subscription/devices/subscription/#')

	while (True):
		print(devices)
		deviceID = str(int(time.time()))
		device = {
			"deviceID": deviceID,
			"resources": random.choice(resources),
			"endpoints": random.choice(endpoints),
			}
		jsonDevice = json.dumps(device)
		catalogue.onPublish(f'/tiot/group18/catalog/subscription/devices/subscription/{deviceID}', jsonDevice) 	
		time.sleep(4)
		
