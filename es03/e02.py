import cherrypy
import json
class Reverse(object):
	exposed = True

	def GET(self, *uri, **params):
		output = {}
		for key in params.keys():
			string = params[key]
			length = len(string)
			output = { key : string[len(string)::-1] }
			params.update(output)
		return json.dumps(params)

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