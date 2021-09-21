def create_database_entry(patient_name, id_no, age):
    new_patient = {"name": patient_name, "id_no": id_no, 
                   "age": age, "tests": []}
    return new_patient


def print_database(db):
    locations = ["Room 1", "Room 4", "ER", "Post-Op"]
    for patient_id, location in zip(db, locations):
        print("{} - {}".format(db[patient_id]["name"],
                               location))


def print_patients_over_age(age, db):
    for patient_id in db:
        if db[patient_id]["age"] > age:
            print(db[patient_id]["name"])


def get_patient(db, id_no):
    patient = db[id_no]
    return patient

def main():
    db = {}
    x = create_database_entry("Ann Ables", 120, 30)
    db[x["id_no"]] = x
    x = create_database_entry("Bob Boyles", 24, 31)
    db[x["id_no"]] = x
    x = create_database_entry("Chris Chou", 33, 33)
    db[x["id_no"]] = x
    x = create_database_entry("David Dinkins", 14, 34)
    db[x["id_no"]] = x
    print(db)

    patient_id_tested = 24
    test_done = ("HDL", 65)

    patient = get_patient(db, patient_id_tested)
    patient["tests"].append(test_done)
    print(db)
    
    print_database(db)


if __name__ == "__main__":
    main()
