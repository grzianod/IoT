from MyMQTT import MyMQTT
import json
import time

class Subscriber(object):
	def __init__(self, topic):
		self.client = MyMQTT("Subscriber", "mqtt.eclipseprojects.io", 1883, self)
		self.topic = topic

	def start(self):
		self.client.start()
		self.client.mySubscribe(self.topic)

	def unsubscribe(self):
		self.client.stop()

	def notify(self, topic, msg):
		print("Received %s on topic %s... " %(msg, topic))

	def stop(self):
		self.client.stop()



if __name__ == "__main__":
	chosen = False
	subscriber = ""

	while(True):
		choice = input("What kind of data you want to retrieve?\n\ta: data from all the building\n\tf: data from a particular floor\n\tr: data from a particular room\n\tc: to go back to this menu\n\tw: wait for publishes\n\tq: to quit\nYour choice: ")
		if choice == "a":
			subscriber = Subscriber("/IoT S.p.A./#")
			subscriber.start()
			chosen = True
		if choice == "f":
			floorID = input("Type the floor [0-->4]: ")
			if(floorID < 0 or floorID > 4):
				print("Invalid floorID")
			else:
				subscriber = Subscriber(f"/IoT S.p.A/{floorID}/#")
				subscriber.start()
				chosen = True
		if choice == "r":
			floorID = input("Type the floor [0-->4]: ")
			roomID = input("Type the room [1-->3]: ")
			if(floorID < 0 or floorID > 4 or roomID < 1 or roomID > 3):
				print("Invalid floorID/roomID")
				flag = True
			else:
				subscriber = Subscribe(f"/IoT S.p.A./{floorID}/{rooomID}/#")
				subscriber.start()
				chosen = True
		if choice == "c":
			if(chosen):
				subscriber.stop()
			else:
				print("No Subscriber running yet...")
			chosen = False
		if choice == "w":
			if(chosen):
				while(True):
					time.sleep(1)
			else:
				print("No Subscriber running yet...")
				chosen = False
		if choice == "q":
			print("Quitting from menu...")
			if(chosen):
				subscribe.stop()
			break


