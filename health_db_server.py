from flask import Flask, request, jsonify
import logging
from pymodm import connect, MongoModel, fields


# Define variable to contain Flask class for server
app = Flask(__name__)

# Create database as an empty list
db = []


def initialize_server():
    logging.basicConfig(filename="health_db_server.log", level=logging.DEBUG)
    print("Connecting to MongoDB...")
    connect("mongodb+srv://daw:jzuHZP0u69vyfskG@bme547.ba348.mongodb.net/"
            "health_db?retryWrites=true&w=majority")
    print("Connected.")


@app.route("/", methods=["GET"])
def status():
    """Used to indicate that the server is running
    """
    return "Server is on"


@app.route("/new_patient", methods=["POST"])
def new_patient():
    """Implements /new_patient route for adding a new patient to server
    database

    The /new_patient route is a POST request that should receive a JSON-encoded
    string with the following format:

    {"name": str, "id": int, "blood_type": str}

    The function then calls validation functions to ensure that the needed
    keys and data types exist in the received JSON, then calls a function to
    add the patient data to the database.  The function then returns to the
    caller either a status code of 200 and the patient info if it was
    successfully added, or a status code of 400 and an error message if there
    was a validation problem.

    Returns:
        str, int: message including patient data if successfully added to the
                  database or error message if not, followed by a status code

    """
    in_data = request.get_json()
    expected_keys = {"name": str, "id": int, "blood_type": str}
    error_string, status_code = validate_server_input(in_data, expected_keys)
    if error_string is not True:
        return error_string, status_code
    added_patient = add_database_entry(in_data["name"],
                                       in_data["id"],
                                       in_data["blood_type"])
    return "Added patient {}".format(added_patient)


def validate_server_input(in_data, expected_keys):
    """Validates that input data to server contains a dictionary with the
    correct keys and data types

    Various routes for this server are POST requests that receive JSON-encoded
    strings which should contain dictionaries.  To avoid server errors, this
    function checks that the input data is a dictionary, that it has the
    specified keys, and specified data types.

    To specify what the needed keys and data types are, a dictionary is sent
    as a parameter to this function.  The keys of this dictionary are the
    needed keys for the input data and the value for each key is the Python
    data type that should be in the input.  For example:

    {"name": str, "id": int, "blood_type: str}

    Args:
        in_data (any type): the input data to a route that has been
            deserialized from a JSON string.  Ideally, it is a dictionary.
        expected_keys (dict): a dictionary with keys matching the keys that
            should be in the input data dictionary and values of the
            corresponding data type.

    Returns:
        str or bool , int: returns True, 200 if data validation is successful.
            Returns an error message string and 400 if data validation is
            unsuccessful.

    """
    if type(in_data) is not dict:
        return "The input was not a dictionary.", 400
    for key in expected_keys:
        if key not in in_data:
            return "The key {} is missing from input".format(key), 400
        if type(in_data[key]) is not expected_keys[key]:
            return "The key {} has the wrong data type".format(key), 400
    return True, 200


class Patient(MongoModel):
    name = fields.CharField()
    id = fields.IntegerField(primary_key=True)
    blood_type = fields.CharField()
    tests = fields.ListField()


def add_database_entry(patient_name, id_no, blood_type):
    """Creates new patient database entry

    This function receives information about the patient, creates a dictionary,
    and appends that dictionary to the database list.  The patient dictionary
    has the following format:

    {"name": str, "id_no": int, "blood_type": str, "tests": list}

    The "tests" list is initialized as an empty list while the values for the
    other keys are taken from the input parameters.  After the new patient
    is added, the database is printed to the console for debugging purposes.
    The created dictionary is returned to enable this function to be tested.

    Args:
        patient_name (str): name of patient
        id_no (int):  patient id number, usually a medical record number
        blood_type (str):  patient blood type, ex. "AB+"

    Returns:
        dict: the patient database entry

    """
    patient_to_add = Patient(name=patient_name,
                             id=id_no,
                             blood_type=blood_type)
    answer = patient_to_add.save()
    return answer


@app.route("/add_test", methods=["POST"])
def add_test():
    """Implements /add_test route for adding a new test result to a patient
    record in the server database

    The /add_test route is a POST request that should receive a JSON-encoded
    string with the following format:

    {"id": int, "test_name": str, "test_result": int}

    The function then calls validation functions to ensure that the needed
    keys and data types exist in the received JSON and that a patient with the
    given id exists in the database.  A function is then called to add the
    test results to the patient record.  The function returns to the
    caller either a status code of 200 and a success message, or a status code
    of 400 and an error message if there was a validation problem.

    Returns:
        str, int: message saying test data successfully added to the
                  database or error message if not, followed by a status code
    """
    in_data = request.get_json()
    expected_keys = {"id": int, "test_name": str, "test_result": int}
    error_string, status_code = validate_server_input(in_data, expected_keys)
    if error_string is not True:
        return error_string, status_code
    patient = find_patient(in_data["id"])
    if patient is False:
        return "Patient ID {} not found in database".format(in_data["id"]), 400
    add_test_result(patient, in_data)
    return "Added test to patient id {}".format(in_data["id"]), 200


def find_patient(id_no):
    """Retrieves patient record from database based on patient id

    This function iterates through the database list and checks the "id" key
    of each patient dictionary against the "id_no" parameter.  If a match is
    found, that patient dictionary is returned.  If no match is found, the
    boolean False is returned.

    Args:
        id_no (int): id number of patient to be found in database

    Returns:
        dict or bool: patient dictionary if patient found in database, False
            if not
    """
    for patient in db:
        if patient["id"] == id_no:
            return patient
    return False


def add_test_result(patient, in_data):
    """Add test data to patient record

    This function formats a tuple containing the test name and result and
    appends it to the tests list of the patient dictionary.

    Args:
        patient (dict): patient data
        in_data (dict):  dictionary containing test name and result

    Returns:
        dict, the updated patient dictionary, for testing purposes only

    """
    test_data_to_add = (in_data["test_name"], in_data["test_result"])
    patient.tests.append(test_data_to_add)
    return patient


@app.route("/get_results/<patient_id>", methods=["GET"])
def get_results(patient_id):
    """ GET route to obtain database entry for a patient by id number

    This function implements a GET route with a variable URL.  The desired
    patient id number is included as part of the URL.  The function calls a
    validation function to ensure that the given id is an integer and that the
    patient exists in the database.  If the validation passes, the function
    calls a function to retrieve the patient record and returns it to the
    caller with a status code of 200.  If the validation fails, an appropriate
    message is returned with a status code of 400.

    Args:
        patient_id (str): the patient id taken from the variable URL

    Returns:
        str or dict , int: An error message string if patient_id was invalid
            or a dictionary containing the patient data, plus a status code.

    """
    validation_response, status_code = validate_patient_id(patient_id)
    if status_code != 200:
        return validation_response, status_code
    patient = find_patient(validation_response)
    return jsonify(patient), 200


def validate_patient_id(patient_id):
    """Validates that the string obtained from the variable URL of
    /get_results/<patient_id> contains an integer and that a patient exists
    in the database with that id.

    A string is sent to this function which first checks if the string contains
    an integer.  If not, an appropriate error message is returned.  If the
    string does contain an integer, that integer is used to check the database.
    If a patient exists with that id number, then the integer is returned
    along with a status code of 200.  Otherwise, an error message is returned
    with a status code of 400.

    Args:
        patient_id (str): string containing an inputted patient_id

    Returns:
        str or int , int: the patient_id if it exists in database or an error
        message followed by a status code

    """
    try:
        id_no = int(patient_id)
    except ValueError:
        return "Patient id was not a valid integer", 400
    patient = find_patient(id_no)
    if patient is False:
        return "Patient id of {} does not exist in database".format(id_no), 400
    return id_no, 200


if __name__ == '__main__':
    initialize_server()
    app.run()
