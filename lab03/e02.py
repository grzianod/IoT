import cherrypy
import json
import time

class ConsumerService(object):
	exposed = True

	def GET(self, *uri, **params):
		if len(uri) == 0:
			raise cherrypy.HTTPError(404, "Bad Request: URI is not correctly formatted")
		if (int)(uri[0]) < 0:
			raise cherrypy.HTTPError(404, "Bad Request: value should be a POSITIVE value") 
		if not uri[1] in ['C', 'F', 'K']:
			raise cherrypy.HTTPError(404, "Bad Request: targetUnit should be Kelvin, Fahrenheit or Celsius")
		if not uri[2] in ['C', 'F', 'K']:
			raise cherrypy.HTTPError(404, "Bad Request: originalUnit should be Kelvin, Fahrenheit or Celsius")
		try:
			value = float(uri[0])
			if uri[1] == "C" and uri[2] == "K":
				convertedValue = (float)(uri[0])+273.15
			if uri[1] == 'C' and uri[2] == 'F':
				convertedValue = (float)(uri[0])*9/5 +32
			if uri[1] == 'K' and uri[2] == 'C':
				convertedValue = (float)(uri[0])-273.15
			if uri[1] == 'K' and uri[2] == 'F':
				convertedValue = ((float)(uri[0])-273.15) * 9/5 + 32
			if uri[1] == 'F' and uri[2] == 'C':
				convertedValue = ((float)(uri[0])-32) * 5/9
			if uri[1] == 'F' and uri[2] == 'K':
				convertedValue = ((float)(uri[0])-32) * 5/9 +273.15
			response = {
				'targetUnit': uri[2],
				'originalUnit': uri[1],
				'value': uri[0],
				'convertedValue': convertedValue
			}
			return json.dumps(response)
		except:
			raise cherrypy.HTTPError(404, "Bad Request: value should be a NUMBER")


if __name__ == '__main__': 
    conf = { 
    	'/': { 
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 
        } 
    } 
    cherrypy.tree.mount(ConsumerService(), '/converter', conf)

    cherrypy.config.update({'server.socket_host': '127.0.0.1'})
    cherrypy.config.update({'server.socket_port': 8080})

    cherrypy.engine.start() 
    cherrypy.engine.block()
