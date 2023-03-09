import paho.mqtt.client as mqtt

class MyMQTT:
	def __init__(self, clientID, broker, port, notifier):
		self.broker = broker
		self.port = port
		self.notifier = notifier
		self.clientID = clientID

		self.__topic = ""
		self.__isSubscriber = False

		self.__paho_mqtt = mqtt.Client(clientID, False)

		self.__paho_mqtt.on_connect = self.myOnConnect
		self.__paho_mqtt.on_message = self.myOnMessageReceived

	def myOnConnect(self, paho_mqtt, userdata, flags, rc):
		print("Connected to %s with result code: %d" %(self.broker, rc))

	def myOnMessageReceived(self, paho_mqtt, userdata, msg):
		self.notifier.notify(msg.topic, msg.payload)

	def myPublish(self, topic, msg):
		print("Publishing '%s' with topic '%s'" % (msg, topic))
		self.__paho_mqtt.publish(topic, msg, 2)

	def mySubscribe(self, topic):
		print("Subscribing to %s " % (topic))
		self.__paho_mqtt.subscribe(topic, 2)
		self.__isSubscriber = True
		self.__topic = topic

	def start(self):
		self.__paho_mqtt.connect(self.broker, self.port)
		self.__paho_mqtt.loop_start()

	def stop(self):
		if(self.__isSubscriber):
			self.__paho_mqtt.unsubscribe(self.__topic)

		self.__paho_mqtt.loop_stop()
		self.__paho_mqtt.disconnect()