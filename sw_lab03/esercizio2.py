import cherrypy
import json
import paho.mqtt.client as mqtt
import urllib3
import time

class Subscriber(object):
	def __init__(self, clientID, broker, port):
		self.broker = broker
		self.port = port
		self.clientID = clientID

		self.topic = ""
		self.paho_mqtt = mqtt.Client(clientID, False)
		self.paho_mqtt.on_connect = self.onConnect
		self.paho_mqtt.on_message = self.onMessage
	
	def onConnect(self, paho_mqtt, userdata, flags, rc):
			print("Connected to '%s' with result code: '%d'" %(self.broker, rc))

	def onMessage(self, client, userdata, message):
		data = json.loads(message.decode('utf-8'))
		print(data)
								

	def onPublish(self, topic, message):
			print("Publishing to broker '%s' with topic '%s' the message '%s'"%(self.broker, topic, message))
			self.paho_mqtt.publish(topic, message, 2)

	def onSubscribe(self, topic):
			print("Subscribing to broker '%s' with '%s' " %(self.broker, topic))
			self.paho_mqtt.subscribe(topic, 2)
			self.topic = topic

	def start(self):
			self.paho_mqtt.connect(self.broker, self.port)
			self.paho_mqtt.loop_forever()

	def stop(self):
			self.paho_mqtt.unsubscribe()
			self.paho_mqtt.loop_stop()	
			self.paho_mqtt.disconnect()

if __name__ == "__main__":
	http = urllib3.PoolManager()
	response = http.request('GET', '192.168.1.2:8080/subscriptions/')
	if response.status != 200:
		print("Request GET to Catalog failed")
		exit()
	subscriptions = json.loads(response.data.decode('utf-8'))
	serviceSubscription = subscriptions.get('service').get('REST')
	message = {
		'serviceID' : 'MBP-di-Graziano',
		'description' : 'offering temperature interface service',
		'endpoints' : 'MQTT',
		'resources' : 'temperature'
	}
	
	response = http.request('POST', serviceSubscription, body=json.dumps(message))
	if response.status != 200:
		print("Request POST to Catalog failed")
	subscriber = Subscriber("MBP-di-Graziano", "test.mosquitto.org", 1883)

	response = http.request('GET', subscriptions.get('device').get('REST'))
	if response.status != 200:
		print("Request GET to Catalog failed")
	if len(response.data) == 0:
		print("No device registered")	
	devices = json.loads(response.data.decode('utf-8'))
	subscriber.onSubscribe(subscriptions.get('device').get('MQTT').get('topic')+"/"+devices.get('arduino').get('deviceID')+"/"+devices.get('arduino').get('resources')[0])
	subscriber.start()
