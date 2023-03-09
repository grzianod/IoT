if __name__ == "__main__":
	personal_data = { "Name" : "",
						"Surname" : "",
						"Birth" : { "Place of birth" : "",
									"Date of birth" : "" 
									},
						"Age" : ""
					}


	personal_data['Name'] = input("Insert your name: ")
	personal_data['Surname'] = input("Insert your surname: ")
	personal_data['Birth']['Place of birth'] = input("Insert your place of birth: ")
	personal_data['Birth']['Date of birth'] = input("Insert your birthdate: ")
	personal_data['Age'] = input("Insert your age: ");

	print(f"Hi {personal_data['Name']} {personal_data['Surname']}, nice to meet you.")
	print(f"You were born the {personal_data['Birth']['Date of birth']} in {personal_data['Birth']['Place of birth']}, your age is {personal_data['Age']}")