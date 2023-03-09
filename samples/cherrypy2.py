import json
import time
import cherrypy

register = []

class Person(object):
	def __init__(self, name, surname, sex, age:int):
		self.__name = name
		self.__surname = surname
		self.__sex = sex
		self.__age = age

	def getName(self):
		return self.__name

	def getSurname(self):
		return self.__surname

	def getSex(self):
		return self.__sex

	def getAge(self):
		return self.__age

	def __str__(self):
		return f"Name : {self.getName()} Surname : {self.getSurname()} Gender : {self.getSex()} Age : {self.getAge()}"

	def dict(self):
		dictionary = {
			'Name': self.getName(),
			'Surname': self.getSurname(),
			'Sex': self.getSex(),
			'Age': self.getAge()
		}
		return dictionary

class WebService(object):
	exposed = True

	def GET(self, *uri, **params):
		global register
		if len(uri) != 0:
			raise cherrypy.HTTPError(404, "Bad Request: missing params!")
		if not 'Name' in params.keys() or not 'Surname' in params.keys() or not 'Sex' in params.keys() or not 'Age' in params.keys():
			raise cherrypy.HTTPError(404, "Bad Request: a Person should be filled with all fields")
		if not params['Sex'] in ['M', 'F', 'T', 'A']:
			raise cherrypy.HTTPError(404, "Bad Request: unknown gender")
		person = Person(params['Name'], params['Surname'], params['Sex'], params['Age'])
		timestamp = time.time()
		toAdd = [ person.dict(), timestamp]
		register.append(toAdd)
		print("REGISTER: ")
		print(register)
		return f"ADDED - {person} @ {timestamp}"

	def POST(self, *uri, **params):
		global register
		contentLength = (int)(cherrypy.request.headers['Content-Length'])
		if contentLength == 0:
			raise cherrypy.HTTPError(404, "Bad Request: missing params!")
		rawData = cherrypy.request.body.read(contentLength)
		jsonDict = json.loads(rawData)
		if not 'Name' in jsonDict.keys() or not 'Surname' in jsonDict.keys() or not 'Sex' in jsonDict.keys() or not 'Age' in jsonDict.keys():
			raise cherrypy.HTTPError(404, "Bad Request: a Person should be filled with all fields")
		if not jsonDict['Sex'] in ['M', 'F', 'T', 'A']:
			raise cherrypy.HTTPError(404, "Bad Request: unknown gender")
		person = Person(jsonDict['Name'], jsonDict['Surname'], jsonDict['Sex'], jsonDict['Age'])
		timestamp = time.time()
		toAdd = [ person.dict(), timestamp]
		register.append(toAdd)
		print("REGISTER: ")
		print(register)
		return f"ADDED - {person} @ {timestamp}"

if __name__ == '__main__': 
    conf = { 
    	'/': { 
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 
        } 
    } 
    cherrypy.tree.mount(WebService(), '/', conf)

    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})

    cherrypy.engine.start() 
    cherrypy.engine.block()

