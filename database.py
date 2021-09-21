class Patient:

    def __init__(self, input_name, id_no, age):
        self.name = input_name
        self.id_no = id_no
        self.age = age
        self.tests = []

        
    def __repr__(self):
        return "{}: {}".format(self.id_no, self.name)
        
    def is_adult(self):
        if self.age >= 21:
            return True
        else:
            return False
        

def create_database_entry(patient_name, id_no, age):
    new_patient = Patient(patient_name, id_no, age)
    #new_patient = {"name": patient_name, "id_no": id_no, 
    #               "age": age, "tests": []}
    #new_patient = [patient_name, id_no, age, []]
    return new_patient


def print_database(db):
    locations = ["Room 1", "Room 4", "ER", "Post-Op"]
    for patient, location in zip(db, locations):
        print("{} - {}".format(patient,
                               location))


def print_patients_over_age(age, db):
    for patient in db:
        if patient["age"] > age:
            print(patient[0])


def get_patient(db, id_no):
    patient = db[id_no]
    #for patient in db:
    #    if patient["id_no"] == id_no:
    #        return patient
    return patient

def main():
    db = {}
    x = create_database_entry("Ann Ables", 120, 30)
    db[x.id_no] = x
    x = create_database_entry("Bob Boyles", 24, 31)
    db[x.id_no] = x
    x = create_database_entry("Chris Chou", 33, 33)
    db[x.id_no] = x
    x = create_database_entry("David Dinkins", 14, 34)
    db[x.id_no] = x
    print(db)

    patient_id_tested = 24
    test_done = ("HDL", 65)

    patient = get_patient(db, patient_id_tested)
    patient.tests.append(test_done)
    print(patient.is_adult())
    print(db[24].tests)
    
    print_database(db)


if __name__ == "__main__":
    main()
