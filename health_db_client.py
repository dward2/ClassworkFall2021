"""This file originally started as a script in which to call and test the
health_db_server code.  It has been modularized so that the health_db_gui
can call some of these function to interact with the server.  A new function
called "main" can be used so this file can still be run independently to test
the server.

"""
import requests


def add_patient_to_server(name_input, id_input, blood_type_input):
    """ Makes request to server to add specified patient information

    This function takes patient information as parameter inputs and makes
    a post request to the health database server to store this patient
    information on the server.  It prints the server response to the
    console as well as returns it to the caller.

    Args:
        name_input (str): patient name
        id_input (str or int): patient id (medical record number)
        blood_type_input (str): patient blood type including rH factor

    Returns:
        str: server response string
    """
    patient1 = {"name": name_input, "id": convert_id_to_int(id_input),
                "blood_type": blood_type_input}
    r = requests.post("http://127.0.0.1:5000/new_patient", json=patient1)
    print(r.status_code)
    print(r.text)
    return r.text


def convert_id_to_int(id_input):
    id_output = int(id_input)
    return id_output


def main():
    # Successfully add patient
    add_patient_to_server("Ann Ables", "201", "A+")

    # Successfully add patient
    add_patient_to_server("Bob Boyles", 202, "O-")

    # Check for missing key
    patient3 = {"name": "Chris Cooper", "id": 202}
    r = requests.post("http://127.0.0.1:5000/new_patient", json=patient3)
    print(r.status_code)
    print(r.text)

    # Check for bad data type
    patient3 = {"name": "Chris Cooper", "id": "202", "blood_type": "AB+"}
    r = requests.post("http://127.0.0.1:5000/new_patient", json=patient3)
    print(r.status_code)
    print(r.text)

    # Successfully add test data
    test1 = {"id": 201, "test_name": "HDL", "test_result": 160}
    r = requests.post("http://127.0.0.1:5000/add_test", json=test1)
    print(r.status_code)
    print(r.text)

    # Check if patient does not exist
    test2 = {"id": 205, "test_name": "HDL", "test_result": 160}
    r = requests.post("http://127.0.0.1:5000/add_test", json=test2)
    print(r.status_code)
    print(r.text)

    # Successful Get Results
    r = requests.get("http://127.0.0.1:5000/get_results/201")
    print(r.status_code)
    print(r.text)

    # Bad Get Results
    r = requests.get("http://127.0.0.1:5000/get_results/205")
    print(r.status_code)
    print(r.text)

    r = requests.get("http://127.0.0.1:5000/get_results/abc")
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    main()
