import cherrypy
import json
import time

conversions=[]
class ConsumerService(object):
	exposed = True

	def POST(self, *uri, **params):
		global conversions
		contentLength = (int)(cherrypy.request.headers['Content-Length'])
		if contentLength:
			try:
				rawBody = cherrypy.request.body.read(contentLength)
				jsonDict = json.loads(rawBody)
			except:
				raise cherrypy.HTTPError(404, "Bad Request: could not convert raw data")
			if not 'targetUnit' in jsonDict.keys():
				raise cherrypy.HTTPError(404, "Bad Request: targetUnit not present")
			if not 'originalUnit' in jsonDict.keys():
				raise cherrypy.HTTPError(404, "Bad Request: originalUnit not present")
			if not 'value' in jsonDict.keys():
				raise cherrypy.HTTPError(404, "Bad Request: value not present")
			if not jsonDict['originalUnit'] in ['C', 'K', 'F']:
				raise cherrypy.HTTPError(404, "Bad Request: originalUnit not permitted")
			if not jsonDict['targetUnit'] in ['C', 'K', 'F']:
				raise cherrypy.HTTPError(404, "Bad Request: targetUnit not permitted")
			try:
				jsonDict['timestamp'] = time.time()
				jsonDict['convertedValue'] = []
				for val in jsonDict['value']:
					if jsonDict['originalUnit'] == "C" and jsonDict['targetUnit'] == "K":
						converted = (float)(float(val) + 273.15)
					if jsonDict['originalUnit'] == 'C' and jsonDict['targetUnit'] == 'F':
						converted = (float)(float(val) * 9/5 + 32)
					if jsonDict['originalUnit'] == 'K' and jsonDict['targetUnit'] == 'C':
						converted = (float)(float(val) - 273.15)
					if jsonDict['originalUnit'] == 'K' and jsonDict['targetUnit'] == 'F':
						converted = (float)((float(val) - 273.15) * 9/5 + 32)
					if jsonDict['originalUnit'] == 'F' and jsonDict['targetUnit'] == 'C':
						converted = (float)((float(val) - 32) * 5/9)
					if jsonDict['originalUnit'] == 'F' and jsonDict['targetUnit'] == 'K':
						converted = (float)((float(val) - 32) * 5/9 + 273.15)
					jsonDict['convertedValue'].append(converted)	
				conversions.append(jsonDict);
				print(conversions)
				return json.dumps(jsonDict)
			except:
				raise cherrypy.HTTPError(404, "Bad Request: value is not a NUMBER")

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
