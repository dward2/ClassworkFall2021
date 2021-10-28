import pytest
from health_db_server import initialize_server

initialize_server()


@pytest.mark.parametrize("in_data, expected", [
    ({"name": "Test Name", "id": 1, "blood_type": "O+"}, (True, 200)),
    ({"nxme": "test Name", "id": 1, "blood_type": "O+"},
     ("The key name is missing from input", 400)),
    ({"name": "Test Name", "id_no": 1, "blood_type": "O+"},
     ("The key id is missing from input", 400)),
    ({"name": "test Name", "id": 1, "bloodtype": "O+"},
     ("The key blood_type is missing from input", 400)),
    ({"name": "test Name", "id": 1, "blood_type": "O+", "extrakey": 2},
     (True, 200)),
    ({"name": "test Name", "id": "1", "blood_type": "O+"},
     ("The key id has the wrong data type", 400)),
    (["name", "David"], ("The input was not a dictionary.", 400))
])
def test_validate_server_input(in_data, expected):
    from health_db_server import validate_server_input
    expected_keys = {"name": str, "id": int, "blood_type": str}
    answer = validate_server_input(in_data, expected_keys)
    assert answer == expected


def test_add_database_entry():
    from health_db_server import add_database_entry
    expected_name = "David Testing"
    answer = add_database_entry(expected_name, 5, "O+")
    answer.delete()  # This deletes the entry in the database, it does not
    # delete the answer variable
    assert answer.name == expected_name


def test_find_patient():
    from health_db_server import find_patient
    from health_db_server import add_database_entry
    expected_name = "David Testing"
    expected_id = 12345
    entry_to_delete = add_database_entry(expected_name, expected_id, "O+")
    answer = find_patient(expected_id)
    entry_to_delete.delete()
    assert answer.id == expected_id
    assert answer.name == expected_name


def test_add_test_result():
    from health_db_server import add_test_result
    from health_db_server import add_database_entry
    add_database_entry("David Testing", 12345, "O+")
    out_data = {"id": 12345, "test_name": "HDL", "test_result": 123}
    answer = add_test_result(out_data)
    answer.delete()
    assert answer.tests[-1] == ("HDL", 123)


@pytest.mark.parametrize("id_to_add, id_to_search, expected", [
    (12345, 12345, (12345, 200)),
    (12345, 23456, ("Patient id of 23456 does not exist in database", 400)),
    (12345, "dog", ("Patient id was not a valid integer", 400))
])
def test_validate_patient_id(id_to_add, id_to_search, expected):
    from health_db_server import validate_patient_id
    from health_db_server import add_database_entry
    entry_to_delete = add_database_entry("David Testing", id_to_add, "O+")
    answer = validate_patient_id(id_to_search)
    entry_to_delete.delete()
    assert answer == expected


def test_generate_results():
    from health_db_server import generate_results
    from health_db_server import add_database_entry
    from health_db_server import add_test_result
    entry_to_delete = add_database_entry("David Testing", 12345, "O+")
    out_data = {"id": 12345, "test_name": "HDL", "test_result": 123}
    add_test_result(out_data)
    out_data["test_name"] = "LDL"
    out_data["test_result"] = 50
    add_test_result(out_data)
    answer = generate_results(12345)
    expected = "Patient Name: David Testing\n" \
               "Test Results:\n" \
               "['HDL', 123]\n" \
               "['LDL', 50]\n"
    """Note that even though the data were initially put into the record
       as tuples, MongoDB stores all "array"-type variables the same and 
       they are returned as lists to Python."""
    entry_to_delete.delete()
    assert answer == expected



