def create_database_entry(patient_name, id_no, age):
    new_patient = {"name": patient_name, "id_no": id_no, 
                   "age": age, "tests": []}
    #new_patient = [patient_name, id_no, age, []]
    return new_patient


def print_database(db):
    locations = ["Room 1", "Room 4", "ER", "Post-Op"]
    for patient, location in zip(db, locations):
        print("{} - {}".format(patient,
                               location))


def print_patients_over_age(age, db):
    for patient in db:
        if patient[2] > age:
            print(patient[0])


def get_patient(db, id_no):
    for patient in db:
        if patient["id_no"] == id_no:
            return patient


def main():
    db = []
    x = create_database_entry("Ann Ables", 120, 30)
    db.append(x)
    x = create_database_entry("Bob Boyles", 24, 31)
    db.append(x)
    x = create_database_entry("Chris Chou", 33, 33)
    db.append(x)
    x = create_database_entry("David Dinkins", 14, 34)
    db.append(x)
    print(db)

    patient_id_tested = 24
    test_done = ("HDL", 65)

    patient = get_patient(db, patient_id_tested)
    patient["tests"].append(test_done)
    
    print_database(db)


if __name__ == "__main__":
    main()
