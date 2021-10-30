# Health Database Server Description using MongoDB/PyMODM

## Intro
The file `health_db_server.py` contains server code for the implementation
of a MondoDB database using the PyMODM package.  Here, I will describe how the
code was modified for use with MongoDB/PyMODM.

## Connection to MongoDB
The connection to MongoDB is established using the `connect` function imported
from `pymodm`.  I have placed this `connect` call in the `initialize_server()`
function.  While it could also be placed in the global section of the module
(similar to where the `app = Flask(__name__)` statement is placed), it can
be advantageous to keep it in a function so that your test module could 
make a separate connection to a test database (see below for more info).

## Adding a new entry to database
The `Patient` class, derived from `MongoModel`, defines what our database
entry will look like.  The function `add_database_entry()` now creates an 
instance of the `Patient` class and initializes the contents of the `name`,
`id`, and `blood_type` fields.  Since no initial values are to be put in the
`tests` list field, it is not given a value in the call to `Patient`.  However,
a `tests` field is still created and will start empty.  The created `Patient`
object is then saved to the database using the `.save()` method.

## Adding a new test result to a patient
I made a few changes for this to work with MongoDB/PyMODM.  The 
`find_patient()` was modified so that it searches the MongoDB database for
the primary key matching the given parameter.  If the id is found, the
database document is stored in the `patient` variable.  If the id is not
found, an error will be generated.  This error is handled in a try/except
block and causes the `patient` variable to be False.  This variable is 
returned.

The `add_test_result()` function was also modified.  It now only receives
the `in_data` dictionary.  It first creates the tuple to be stored as part
of the `tests` list.  Then, it calls the `find_patient` function sending it the
id of the patient to find.  We know the patient will exist because we will
check that before calling this function.  The patient record will be saved in
the `patient` variable.  As described above, the `.tests` property of
`patient` will exist as an empty list.  So, we can `append` to it like any
other list.  Then, we save the updated record back to the database.

Finally, the `add_test` flask handler function is modified slightly to call
these functions.

## Getting results
The `/get_results/<patient_id>` route was improved and converted to using
MongoDB/PyMODM.  The `get_results()` function first calls the 
`validate_patient_id()` function to validate that the `<patient_id>` of the 
variable URL is in fact an integer and that this patient id exists in the
database by calling `find_patient()`.  If the patient exists, a new function
called `generate_results()` is called and is sent the patient id.  
`generate_results()` calls `find_patient()` to get the patient record and then
creates a string containing the patient results.

## Testing
The file `test_health_db_server.py` demonstrates the needed unit tests for
the server functions.  Note, these are sample tests, and you may need a wider
range of coverage than shown here.

### `test_validate_server_input`
This test is pretty straight forward and does not involve MongoDB.

### `test_add_database_entry`
When needing to test a function that does MongoDB interactions, you generally
follow these steps:<br>
a. establish a database connection<br>
b. set-up the database contents as needed to run test<br>
c. call the function to be tested<br>
d. erase any database entries made for the test so it does not interfere with
  other tests or your production database<br>
e. make an `assert` statement to check for the correct outcome.<br>

a. The connection to the database is established at the top of the testing module
by calling the `health_db_server.initialize_server()` function.  This will
connect to the same database used by the server code.  By being outside this
function, this connection can be used by all the tests.

b. Since this test function is testing the addition of an entry to the 
database, there is no setup that needs to be done.

c. A call to `add_database_entry` is made and the response is stored in the 
`answer` variable.  If the save to the database was correct, `answer` will be
an instance of the `Patient` class with the data saved to the database.

d. This entry to the database is removed from the database using the 
`.delete()` method.  Note that this does not delete the `answer` variable and
it will still have the `Patient` class information.  But, it does delete the
remote database entry.
e. The returned `Patient.name` is compared against the expected_name used to
add the entry.

### `test_find_patient`
This function will follow the same five steps as above.

a. Previously done

b. The database is set up for the test by using the `add_database_entry()` 
function to add a database entry that we can find in the test.  We save the
return from this function in a variable called `entry_to_delete` so we can
later delete it from the database.

c. We call the function to be tested and store the response in `answer` which
will be either a `Patient` instance of the patient is found or `False` if not.

d. We delete the entry that was made in the database for testing.

e. Check that the `answer.id` and `answer.name` match the patient we were
looking for.

### `test_find_patient_missing`
The above function tested `find_patient` when a patient exists.  This function
tests if a patient is missing.  These two functions could be combined into
one using a `parametrize` decorator with some modifications.

This function does not need steps (b) and (d) because no database setup is
needed because we want to look for a missing patient id.

### `test_add_test_result`
Here, the database prep consists of using `add_database_enty` to create a 
database entry to which we can add a test.  Then, we create the dictionary
containing the patient id and test results which we then send to the
`add_test_results()` function.  This function should return a `Patient` 
object that was saved to the database.  So, after we delete the database
entry, we can check that the returned `Patient` has the submitted test data
as the last entry in its `.tests` list.

### `test_validate_patient_id`
This unit test has three cases covering each of the possible outcomes of the
patient id validation:  i) the id is an integer and exists in database,
ii) the id is an integer and does not exist in the database, and iii) the id
is not an integer.

First, the database is set up for testing by adding a test patient using the
`id_to_add` parameter.  Then, a call is made to the `validate_patient_id`
function sending it the `id_to_search`.  The test entry is deleted from the
database and the answer compared with the expected answer.

### `test_generate_reults`
This function follows the same five steps, but there are more steps needed to
set up the database.

## Alternative approach for setting up testing database
In the description above, the same database that is used by the server code
is also used for the unit tests.  This is because the test module uses the
`initialize_server` function from the server code and its `connect` function
to establish the connection.  

An alternative is to use a completely separate database for the testing module.
Instead of calling `initialize_server` to use its `connect string`, you could
include a `connect` command directly in the test module.  It could then point
to a different database that is separate from your "production" database that
the server uses.  And advantage of this is that you could just set up your
database once for testing.  But, any change made to the database would have to
be reset before the tests are run again.