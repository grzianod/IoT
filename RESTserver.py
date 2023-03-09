import time 
import json
import cherrypy

class RESTserver(object):
	exposed = True

	def GET(self, *uri, **params):
		return "GET"

	def POST(self, *uri, **params):
		return "POST"

	def PUT(self, *uri, **params):
		pass

if __name__ == "__main__":
	conf = {
		"/" : {
			"request.dispatch" : cherrypy.dispatch.MethodDispatcher(),
		}
	}

	cherrypy.tree.mount(RESTserver(), '/server', conf)
	cherrypy.config.update({"server.socket_host" : "192.168.1.190"})
	cherrypy.config.update({"server.socket_port" : 8080})
	cherrypy.config.update({"tool.session.on" : True})

	cherrypy.engine.start()
	cherrypy.engine.block()