import json
import urllib3
import paho.mqtt.client as mqtt
import datetime as datetime
import time
class MQTTClient(object):
	def __init__(self, clientID, broker, port):
		self.clientID = clientID
		self.broker = broker
		self.port = port
		
		self.paho_mqtt = mqtt.Client(clientID, False)
		self.paho_mqtt.on_connect = self.onConnect
		self.paho_mqtt.on_message = self.onMessage

	def onConnect(self, paho_mqtt, userdata, flag, rc):
		print("Connected to broker '%s' on port %d" % (self.broker, self.port))		
	
	def onPublish(self, topic, message):
		print("Publishing to broker '%s' with topic '%s' the message '%s'"%(self.broker, topic, message))
		self.paho_mqtt.publish(topic, message)
	
	def onMessage(self, paho_mqtt, userdata, message):
		status = json.loads(message.payload.decode('utf-8'))
		print(status.get('e').get('v'))
	
	def onSubscribe(self, topic):
		print("Subscribing to broker '%s' at topic '%s'" % (self.broker, topic))
		self.paho_mqtt.subscribe(topic, 2)		

	def start(self):
		self.paho_mqtt.connect(self.broker, self.port)
		self.paho_mqtt.loop_start()
	
	def stop(self):
		self.paho_mqtt.loop_stop()
		self.paho_mqtt.disconnect() 

if __name__ == "__main__":
	http = urllib3.PoolManager()
	publisher = MQTTClient("arduinoYun", "test.mosquitto.org", 1883)
	catalogServer = '192.168.1.2:8080/subscriptions'
	response = http.request('GET', catalogServer)
	if response.status != 200:
		print("Request GET to Catalog Server (%s) failed"%(catalogServer))
		exit()
	subscriptions = json.loads(response.data.decode('utf-8'))
	device = {
		'deviceID' : 'arduinoYun',
		'endpoints' : 'MQTT',
		'resources' : [ 'temperature', 'motion','noise', 'fan', 'heat' ]
	}
	response = http.request('POST', subscriptions.get('device').get('REST'), body=json.dumps(device))
	if response.status != 200:
		print("POST device to Catalog failed")
		exit()
	print(json.loads(response.data.decode('utf-8')))
	
	publisher.start()
	time.sleep(1)
	while(True):
		message = input()
		msg = json.loads(message)
		print(msg)
		now = datetime.datetime.now()
		if "bn" not in msg.keys():
			print("Wrong format: Missing 'bn' field")
			continue	
		if "e" not in msg.keys():
			print("Wrong format: Missing 'e' field")
			continue
		for data in msg.get('e'):
			if 'n' not in data.keys():
				print("Wrong format: Missing 'n' field")
				continue
			if 'v' not in data.keys():	
				print("Wrong format: Missing 'v' field")
				continue
			if 'u' not in data.keys():
				print("Wrong format: Missing 'u' field")
				continue
			payload = { 
				'bn' : 'arduinoYun',
				'e' :  data
			}
			payload['e']['t'] = now.strftime("%Y:%M:%D %H:%M:%S") 
			publisher.onPublish(subscriptions.get('device').get('MQTT').get('topic')+"/arduinoYun/"+payload.get('e').get('n'), json.dumps(payload))
			
