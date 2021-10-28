import pymodm.errors
from flask import Flask, request, jsonify
import logging
from pymodm import connect, MongoModel, fields


# Define variable to contain Flask class for server
app = Flask(__name__)


class Patient(MongoModel):
    """ Database format for a Patient Record

    This class defines the MongoModel database entry for the Patient database.
    The fields are self-descriptive.  It is used for accessing the MongoDB
    database through the PyMODM package.

    """
    name = fields.CharField()
    id = fields.IntegerField(primary_key=True)
    blood_type = fields.CharField()
    tests = fields.ListField()


def initialize_server():
    """ Initializes server conditions

    This function initializes the server log as well as creates a connection
    with the MongoDB database.  User will need to edit the connection string
    to match their specific MongoDB connect string.  In order to prevent
    pushing the database access password to GitHub where others might be able
    to find it, the database user name and password are stored in a separate
    file that is not committed to the repository.  This secret file should
    also be added to the ".gitignore" file to ensure it isn't accidentally
    committed.  This secret file consists of two lines as follows:

        MONGO_DB_USER_NAME = "<user_name>"
        MONGO_DB_PASSWORD = "<password>"

    where <user_name> and <password> are replaced with the appropriate text.

    Note:  Just because the `connect` function completes does not ensure that
    the connection was actually made.  You will need to check that data is
    successfully stored in your MongoDB database.
    """
    from secrets_do_not_commit import MONGO_DB_USER_NAME, MONGO_DB_PASSWORD
    logging.basicConfig(filename="health_db_server.log", level=logging.DEBUG)
    print("Connecting to MongoDB...")
    connect("mongodb+srv://{}:{}@bme547.ba348.mongodb.net/health_db"
            "?retryWrites=true&w=majority".format(MONGO_DB_USER_NAME,
                                                  MONGO_DB_PASSWORD))
    print("Connection attempt finished.")


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


def add_database_entry(patient_name, id_no, blood_type):
    """Creates new patient database entry, updated for MongoDB/PyMODM

    This function receives information about the patient, creates an instance
    of the Patient class for saving the data into a MongoDB database using the
    PyMODM package, and saves that data set into the database.  Note that only
    the `name`, `id` and `blood_type` fields are initialized.  Since the
    `tests` list is empty, there is no need to initialize it here.  In fact,
    doing so causes problems later.

    If the save to the database is successful, an instance of Patient
    containing the data saved to the database is created in the `answer`
    variable which is returned.

    Args:
        patient_name (str): name of patient
        id_no (int):  patient id number, usually a medical record number
        blood_type (str):  patient blood type, ex. "AB+"

    Returns:
        Patient: contains the data saved to database

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
    does_patient_exist = find_patient(in_data["id"])
    if does_patient_exist is False:
        return "Patient ID {} not found in database".format(in_data["id"]), 400
    add_test_result(in_data)
    return "Added test to patient id {}".format(in_data["id"]), 200


def find_patient(id_no):
    """Retrieves patient record from database based on patient id, Updated for
    MongoDB/PyMODM

    This function searches the MongoDB "Patient" database for the record
    with an "id" of that given as the "id_no" parameter.  If a match is
    found, that Patient instance is returned.  If no match is found, the
    boolean False is returned.

    Args:
        id_no (int): id number of patient to be found in database

    Returns:
        Patient or bool: Patient instance if patient found in database, False
            if not
    """
    try:
        patient = Patient.objects.raw({"_id": id_no}).first()
    except pymodm.errors.DoesNotExist:
        patient = False
    return patient


def add_test_result(in_data):
    """Add test data to patient record, updated for MONGODB/PyMODM

    This function formats a tuple containing the test name and result.  Then,
    it calls the function to obtain the patient document from the MongoDB
    database.  Then, it appends the created tuple to the tests list of the
    patient document.  The updated patient record is then saved to the MongoDB
    database and returned.

    Args:
        in_data (dict):  dictionary containing patient id, test name and result

    Returns:
        Patient: the updated patient document, for testing purposes

    """
    test_data_to_add = (in_data["test_name"], in_data["test_result"])
    patient = find_patient(in_data["id"])
    patient.tests.append(test_data_to_add)
    patient.save()
    return patient


@app.route("/get_results/<patient_id>", methods=["GET"])
def get_results(patient_id):
    """ GET route to obtain database entry for a patient by id number

    This function implements a GET route with a variable URL.  The desired
    patient id number is included as part of the URL.  The function calls a
    validation function to ensure that the given id is an integer and that the
    patient exists in the database.  If the validation passes, the function
    calls a function to that generates a string with the patient results
    and returns that string to the caller with a status code of 200.  If the
    validation fails, an appropriate message is returned with a status code
    of 400.

    Args:
        patient_id (str): the patient id taken from the variable URL

    Returns:
        str, int: An error message if patient_id was invalid or a results
        string containing the patient data, plus a status code.

    """
    validation_response, status_code = validate_patient_id(patient_id)
    if status_code != 200:
        return validation_response, status_code
    results = generate_results(validation_response)
    return results, 200


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


def generate_results(patient_id):
    """ Create string the summarizes patient test results

    This function obtains the patient document from the database by calling
    the find_patient function.  A formatted string is then created that
    contains the patient name and list of their test results.

    Args:
        patient_id (int): the id number of the patient for whom to get results

    Returns:
        string: summary of patient test results

    """
    patient = find_patient(patient_id)
    results = "Patient Name: {}\n".format(patient.name)
    results += "Test Results:\n"
    for test in patient.tests:
        results += "{}\n".format(test)
    return results


if __name__ == '__main__':
    initialize_server()
    app.run()
