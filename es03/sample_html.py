import cherrypy
import os

class Example(object): 
        """docstring for Example"""
        exposed=True
        
        def __init__(self):
                self.id=1 
        def GET(self):
                return open("index.html")

if __name__ == '__main__': 
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
        cherrypy.tree.mount(Example(),'/',conf)
        cherrypy.engine.start()
        cherrypy.engine.block()