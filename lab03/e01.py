import cherrypy
import json

class WebService(object):
	exposed = True

	def GET(self, *uri, **params):
		if len(uri) != 0:
			raise cherrypy.HTTPError(404, "Bad Request: URI is not correctly formatted")
		if not 'targetUnit' in params.keys():
			raise cherrypy.HTTPError(404, "Bad Request: targetUnit is not in the parameters")
		if not 'originalUnit' in params.keys():
			raise cherrypy.HTTPError(404, "Bad Request: originalUnit is not in the parameters")
		if not 'value' in params.keys():
			raise cherrypy.HTTPError(404, "Bad Request: value is not in the parameters")
		if not params['targetUnit'] in ['C', 'F', 'K']:
			raise cherrypy.HTTPError(404, "Bad Request: targetUnit should be Kelvin, Fahrenheit or Celsius")
		if not params['originalUnit'] in ['C', 'F', 'K']:
			raise cherrypy.HTTPError(404, "Bad Request: originalUnit should be Kelvin, Fahrenheit or Celsius")
		try:
			value = float(params['value'])
			if params['originalUnit'] == "C" and params['targetUnit'] == "K":
				convertedValue = (float)(params['value'])+273.15
			if params['originalUnit'] == 'C' and params['targetUnit'] == 'F':
				convertedValue = (float)(params['value'])*9/5 +32
			if params['originalUnit'] == 'K' and params['targetUnit'] == 'C':
				convertedValue = (float)(params['value'])-273.15
			if params['originalUnit'] == 'K' and params['targetUnit'] == 'F':
				convertedValue = ((float)(params['value'])-273.15) * 9/5 + 32
			if params['originalUnit'] == 'F' and params['targetUnit'] == 'C':
				convertedValue = ((float)(params['value'])-32) * 5/9
			if params['originalUnit'] == 'F' and params['targetUnit'] == 'K':
				convertedValue = ((float)(params['value'])-32) * 5/9 +273.15
			response = {
				'targetUnit': params['targetUnit'],
				'originalUnit': params['originalUnit'],
				'value': params['value'],
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
    cherrypy.tree.mount(WebService(), '/converter', conf)

    cherrypy.config.update({'server.socket_host': '127.0.0.1'})
    cherrypy.config.update({'server.socket_port': 8080})

    cherrypy.engine.start() 
    cherrypy.engine.block()
