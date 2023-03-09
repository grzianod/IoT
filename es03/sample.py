import cherrypy

class HelloWorld(object):
	exposed = True

	def GET(self, *uri, **params):
		output = "Hello World!"
		print(len(uri))
		print(params)
		if len(uri) != 0:
			output+='<br>uri: '+', '.join(uri)
		if params != {}:
			output+='<br>params: '+str(params)
		return output

if __name__ == "__main__":
	conf = {
		'/' : {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tool.session.on': True
		}
	}
	cherrypy.tree.mount(HelloWorld(), '/', conf)
	cherrypy.engine.start()
	cherrypy.engine.block()
