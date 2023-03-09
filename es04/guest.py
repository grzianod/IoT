import json
from MyMQTT import MyMQTT
import time

last = ""

class Guest(object):
	def __init__(self, username):
		self.username = username
		self.client = MyMQTT(username, "mqtt.eclipseprojects.io", 1883, self)
		self.client.start()
		self.client.mySubscribe("/chat/") 

	
	def send(self, msg):
		global last
		dict = {
			"user" : self.username,
			"msg" : str(msg),
			"timestamp" : time.time()
		}
		if last == self.username:
			print("Bad Request: message NOT sent")
		else: 
			self.client.myPublish("/chat/", json.dumps(dict))


	def notify(self, topic, msg):
		dict = json.loads(msg)
		last = dict['user']
		if not dict['user'] == self.username:
			print("%s - '%s' send '%s' @ %s" %(self.username, dict['user'], dict['msg'], dict['timestamp']))

	def stop(self):
		self.client.stop()



