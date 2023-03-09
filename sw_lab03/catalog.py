import cherrypy
import json
from datetime import datetime
import time

devices = {}
users = {}
services = {}
resources = []

subscriptions = {
	"device" : {
		"REST" : "http://192.168.1.190:8080/devices",
		"MQTT" : {
				"hostname" : "test.mosquitto.org",
				"port" : 1883,
				"topic": "tiot/group18/catalog/devices/subscription"
			}
		},
	"user" : {
		"REST" : "http://192.168.1.190:8080/users",
		"MQTT" :  {
			"hostname" : "test.mosquitto.org",
			"port" : 1883,
			"topic" : "/tiot/group18/catalog/users/subscription"
		}
	},
	"service" : {
		"REST" : "http://192.168.1.190:8080/services",
		"MQTT" : {
			"hostname" : "test.mosquitto.org",
			"port" : 1883,
			"topic" : "/tiot/group18/catalog/services/subscription"	
		}
	}
}

class Subscriptions(object):
	exposed = True

	def GET(self, *uri, **params):
		global subscriptions
		if len(uri) == 0 :
			return json.dumps(subscriptions)
		try:
			return json.dumps(subscriptions[uri[0]])
		except:
			raise cherrypy.HTTPError(404, "Subscription not found")

class Devices(object):
	exposed = True

	def GET(self, *uri, **params):
		global devices
		if len(uri) == 0:
			return json.dumps(devices)
		if str(uri[0]) in devices.keys():
			return json.dumps(devices.get(uri[0]))
		else:
			cherrypy.HTTPError(404, "userID not found")

	def POST(self, *uri, **params):
		global devices
		global resources
		now = datetime.now()
		contentLength = (int)(cherrypy.request.headers['Content-Length'])
		rawBody = cherrypy.request.body.read(contentLength)
		device = json.loads(rawBody)
		if "deviceID" not in device.keys():
			raise cherrypy.HTTPError(404, "deviceID not defined")
		if "endpoints" not in device.keys():
			raise cherrypy.HTTPError(404, "endpoints not defined")
		if "resources" not in device.keys():
			raise cherrypy.HTTPError(404, "resources not defined")
		device["timestamp"] = (int)(now.strftime("%Y%m%d%H%M%S"))
		deviceID = device["deviceID"]
		del device["deviceID"]
		devices[deviceID] = device
		for r in device['resources']:
			if r not in resources:
				resources.append(r)
		return json.dumps(device)

class Services(object):
	exposed = True

	def GET(self, *uri, **params):
		global services
		if len(uri) == 0:
			return json.dumps(services)
		if str(uri[0]) in services.keys():
			return json.dumps(services.get(uri[0]))
		else:
			cherrypy.HTTPError(404, "serviceID not found")

	def POST(self, *uri, **params):
		global services
		now = datetime.now()
		contentLength = (int)(cherrypy.request.headers['Content-Length'])
		rawBody = cherrypy.request.body.read(contentLength)
		service = json.loads(rawBody)
		if "serviceID" not in service.keys():
			raise cherrypy.HTTPError(404, "serviceID not defined")
		if "description" not in service.keys():
			raise cherrypy.HTTPError(404, "description not defined")
		if "endpoints" not in service.keys():
			raise cherrypy.HTTPError(404, "endpoints not defined")
		if "resources" not in service.keys():
			raise cherrypy.HTTPError(404, "resources not defined")
		service["timestamp"] = (int)(now.strftime("%Y%m%d%H%M%S"))
		serviceID = service["serviceID"]
		del service["serviceID"]
		services[serviceID] = service
		return json.dumps(service)

class Users(object):
	exposed = True

	def GET(self, *uri, **params):
		global users
		print(params)
		if len(uri) == 0:
			return json.dumps(users)
		if str(uri[0]) in users.keys():
			return json.dumps(users.get(uri[0]))
		else:
			cherrypy.HTTPError(404, "userID not found")

	def POST(self, *uri, **params):
		global users
		now = datetime.now()
		contentLength = (int)(cherrypy.request.headers['Content-Length'])
		rawBody = cherrypy.request.body.read(contentLength)
		user = json.loads(rawBody)
		if "userID" not in user.keys():
			raise cherrypy.HTTPError(404, "userID not defined")
		if "name" not in user.keys():
			raise cherrypy.HTTPError(404, "name not defined")
		if "surname" not in user.keys():
			raise cherrypy.HTTPError(404, "surname not defined")
		if "email" not in user.keys():
			raise cherrypy.HTTPError(404, "email not defined")
		user["timestamp"] = (int)(now.strftime("%Y%m%d%H%M%S"))
		userID = device["userID"]
		del user["userID"]
		users[userID] = user
		return json.dumps(user)


if __name__ == "__main__":
	conf = {
		"/" : {
			"request.dispatch" : cherrypy.dispatch.MethodDispatcher(),
			"tool.session.on" : True
		}
	}

	cherrypy.tree.mount(Subscriptions(), '/subscriptions', conf)
	cherrypy.tree.mount(Devices(), '/devices', conf)
	cherrypy.tree.mount(Services(), '/services', conf)
	cherrypy.tree.mount(Users(), '/users', conf)

	cherrypy.config.update({'server.socket_host' : "192.168.1.190"})
	cherrypy.config.update({'server.socket_port' : 8080})

	cherrypy.engine.start()

	oldtime = (int)(datetime.now().strftime("%Y%m%d%H%M%S"))
	toDelete = []
	while(True):
		now = (int)(datetime.now().strftime("%Y%m%d%H%M%S"))
		if now - oldtime > 200:
			time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			print(f"\nRegistered devices @ {time}: ")
			print(devices)
			oldtime = now
		for deviceID in devices.keys():
			if now - devices[deviceID]["timestamp"] > 500:  
				toDelete.append(deviceID)
		for item in toDelete:
			del devices[item]
		toDelete = []

    
