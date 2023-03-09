import cherrypy
import json

class Reverse(object):
	exposed = True

	def PUT(self, *uri, **params):
		contentLength = (int)(cherrypy.request.headers['Content-Length'])
		if contentLength:
			try:
				rawBody = cherrypy.request.body.read(contentLength)
				jsonDict = json.loads(rawBody)
			except:
				raise cherrypy.HTTPError(404, "Bad Request: JSON not valid")
		for key in jsonDict.keys():
			string = jsonDict[key]
			length = len(string)
			reversed = string[length::-1]
			output = { key : reversed }
			jsonDict.update(output)
		output = "The keys are [\'"+'\',\''.join(jsonDict.keys())+'\'] and the values are [\''+'\',\''.join(jsonDict.values())+'\']'
		return output

if __name__ == "__main__":
	conf = {
		'/' : {
			'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
			'tool.session.on' : True
		}
	}

	cherrypy.tree.mount(Reverse(), '/', conf)
	cherrypy.engine.start()
	cherrypy.engine.block()