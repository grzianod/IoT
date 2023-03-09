from MyMQTT import MyMQTT
import time
import json

class Light(object):
	def __init__(self, clientID, status:bool):
		self.clientID = clientID
		self.status = False
		self.MyMQTTClient = MyMQTT(self.clientID, "mqtt.eclipseprojects.io", 1883, self)

	def run(self):
		print("Running %s " % (self.clientID))
		self.MyMQTTClient.start()

	def end(self):
		print("Ending %s " % (self.clientID))
		self.MyMQTTClient.stop()

	def notify(self, topic, msg):
		print("Received '%s' under topic '%s'" % (msg, topic))
		jsonDict = json.loads(msg)
		self.status = jsonDict['status']
		print("Light status updated to %s @ %s" % (jsonDict['status'], jsonDict['timestamp']))

	def load(self):
		jsonDict = {
			"status": self.status,
			"timestamp": time.time()
		}
		return json.dumps(jsonDict)




if __name__ == "__main__":
	light_pub = Light("Light Publisher", False)
	light_sub = Light("Light Subscriber", False)
	light_pub.run()
	light_sub.run()
	light_sub.MyMQTTClient.mySubscribe("/light/status")
	time.sleep(2)

	for i in range(3):
		if(light_pub.status):
			light_pub.MyMQTTClient.myPublish("/light/status", light_pub.load())
			light_pub.status = False
		else:
			light_pub.MyMQTTClient.myPublish("/light/status", light_pub.load())
			light_pub.status = True
		time.sleep(2)

	light_sub.end()
	light_pub.end()
