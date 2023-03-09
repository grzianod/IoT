import cherrypy
import random
import string

class HelloWorld(object):
	@cherrypy.expose
	def index(self):
		return "HelloWorld"

	@cherrypy.expose
	def generate(self, length=16):
		my_string = ''.join(random.sample(string.hexdigits, int(length)))
		cherrypy.session['my_string'] = my_string
		return my_string 

	@cherrypy.expose
	def display(self):
		return cherrypy.session['my_string']

if __name__ == "__main__":
	conf = {
		'/': {'tools.sessions.on':True }
	}
	cherrypy.tree.mount(HelloWorld(), '/', conf)
	cherrypy.config.update({'server.socket_host':'0.0.0.0'})
	cherrypy.config.update({'server.socket_port':8080})
	cherrypy.engine.start()
	cherrypy.engine.block()
