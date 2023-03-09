import cherrypy
import json
import time
from e01 import Light

light = ""

class WebService(object):
	exposed=True

	def GET(self):
		return open("index.html")

	def PUT(self, *uri, **params):
		global light
		dict = {
			"status" : uri[0],
			"timestamp" : time.time()
		}
		light.MyMQTTClient.myPublish("/light/status", json.dumps(dict))


if __name__ == "__main__":
	conf = {
                '/' : {
                        'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
                        'tool.session.on' : True
                },
                '/css' : {
                        'tools.staticdir.on' : True,
                        'tools.staticdir.dir' : '/Users/grazianodinocca/Desktop/IoT/es03/css'
                },
                '/js' : {
                        'tools.staticdir.on' : True,
                        'tools.staticdir.dir' : '/Users/grazianodinocca/Desktop/IoT/es03/js'
                },
        }

	cherrypy.tree.mount(WebService(), '/', conf)
	cherrypy.engine.start()

	light = Light("Light Subscriber", False)
	light.run()
	light.MyMQTTClient.mySubscribe("/light/status")


	cherrypy.engine.block()