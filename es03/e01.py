import cherrypy

class Reverse(object):
	exposed = True

	def GET(self, *uri, **params):
		input = uri[0]
		length = len(input)
		reversed = input[length::-1]
		return reversed

if __name__ == "__main__":
	conf = {
		'/' : {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tool.session.on': True
		}
	}
	cherrypy.tree.mount(Reverse(), '/', conf)
	cherrypy.engine.start()
	cherrypy.engine.block()