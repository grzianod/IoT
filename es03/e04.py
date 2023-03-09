import cherrypy
import json
import requests
import time

if __name__ == "__main__":
	currencies = {
		'E' : 'EUR',
		'U' : 'USD',
		'P' : 'GBP'
	}
	while True:
		print("\nAvailable commands:\n  - latest\n  - date\n  - time_series\n  - exit\nYour choice:");
		input_choice = input()
		if input_choice == "exit":
			break
		print("\nWhich base currency you want:\n  - E: Euro\n  - U: USD\n  - P: GBP\nYour choice: ")
		input_curr = input()
		if not input_curr in currencies.keys():
			print("\nCurrencie choice not valid\n")
			continue
		if input_choice == "latest":
			response = requests.get(f"https://api.frankfurter.app/latest?from={currencies.get(input_curr)}")
			jsonDict = response.json();
			print(f"\n\t1 {currencies.get(input_curr)} = ")
			rates = "rates"
			for rate in jsonDict[rates].keys():
				print("\t %10.2f %s" % (jsonDict[rates].get(rate), rate))

		if input_choice == "time_series":
			print("\nType a start date [YYYY-MM-DD]:")
			start = input()
			print("\nType an end date [YYYY-MM-DD]:")
			end = input()
			response = requests.get(f"https://api.frankfurter.app/{start}..{end}?from={currencies.get(input_curr)}")
			jsonDict = response.json();
			rates = "rates"
			dates = "dates"
			for date in jsonDict[rates].keys():
				print(f"\n@ {date} : 1 {currencies.get(input_curr)} = ")
				for rate in jsonDict[rates].get(date).keys():
					print("\t\t %10.2f %s" % (jsonDict[rates].get(date).get(rate), rate))
		if input_choice == "date":
			print("\nType a date [YYYY-MM-DD]:")
			date = input()
			response = requests.get(f"https://api.frankfurter.app/{date}?from={currencies.get(input_curr)}")
			jsonDict = response.json();
			print(f"\n@ {date} : 1 {currencies.get(input_curr)} = ")
			rates = "rates"
			for rate in jsonDict[rates].keys():
				print("\t\t %10.2f %s" % (jsonDict[rates].get(rate), rate))

