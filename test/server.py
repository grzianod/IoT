import json
import cherrypy
import time
from datetime import datetime
import paho.mqtt.client as mqtt

updates = []
status = {
	"sensor": "led",
	"value" : 0,
	"timestamp": 0,
	"device": "ND"
}

class MQTTpublisher(object):
	def __init__(self, username, broker, port):
		self.username = username	
		self.broker = broker
		self.port = port

		self.client = mqtt.Client(username, broker, port)
		self.client.on_connect = self.onConnect
		self.client.on_publish = self.onPublish

	def onConnect(self, client, userdata, flag, rc):
		print("Connected to broker \"%s\" with result code: %d" % (self.broker,rc))

	def onPublish(self, topic, message):
		print("Publishing \"%s\" to broker \"%s\" on topic \"%s\"" % (message, self.broker, topic))
		self.client.publish(topic, message, 2) 		

	def start(self):
		self.client.connect(self.broker, self.port)
		self.client.loop_start()

	def stop(self):
		self.client.disconnect()
		
class Server(object):
	exposed = True

	def GET(self, *uri, **params):
		global updates
		if len(params) != 0 and len(uri) == 0:
			try:
				status['device'] = params['device']
				status['sensor'] = params['sensor']
				status['value'] =  params['value']
				status['timestamp'] = (int)(datetime.now().strftime("%Y%m%d%H%M%S"))
				updates.append(status)
				publisher = MQTTpublisher("LEDpublisher", "broker.emqx.io", 1883)
				publisher.start()
				publisher.onPublish("/test/led", json.dumps(status))
				publisher.stop()
				return json.dumps(status)	
			except:
				raise cherrypy.HTTPError(404, "Missing field") 
		return json.dumps(updates)

	def POST(self, *uri, **params):
		global status
		global updates
		publisher = MQTTpublisher("LEDpublisher", "broker.emqx.io", 1883)
		publisher.start()
		contentLength = (int)(cherrypy.request.headers.get('Content-Length'))	
		rawBody = cherrypy.request.body.read(contentLength)
		jsonDict = json.loads(rawBody)
		if "device" not in jsonDict.keys():
			raise cherrypy.HTTPError(404, "Device field not found")
		if "sensor" not in jsonDict.keys():
			raise cherrypy.HTTPError(404, "Sensor field not found")
		if "value" not in jsonDict.keys():
			raise cherrypy.HTTPError(404, "Value field not found")
		if jsonDict["value"] < 0 or jsonDict["value"] > 255:
			raise cherrypy.HTTPError(404, "Value not in range [0;255]")
		status["sensor"] = jsonDict["sensor"]
		status["value"] = jsonDict["value"] 	
		status["timestamp"] = datetime.now().strftime("%Y%m%d%H%M%S")
		status["device"] = jsonDict["device"]
		updates.append(status)
		publisher.onPublish("/test/led", json.dumps(status).encode('utf-8'))
		publisher.stop()
		return json.dumps(status)

if __name__ == "__main__":
	conf = {
		'/': {
			'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on' : True
		}
	}
	cherrypy.tree.mount(Server(), '/led', conf)	
	cherrypy.config.update({'server.socket_host':'192.168.1.190'})
	cherrypy.config.update({'server.socket_port': 8080})	
	cherrypy.engine.start()
	cherrypy.engine.block()
