from health_db_server import initialize_server

initialize_server()


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
    add_database_entry(expected_name, expected_id, "O+")
    answer = find_patient(expected_id)
    assert answer.id == expected_id
    assert answer.name == expected_name


def test_add_test_result():
    from health_db_server import add_test_result
    from health_db_server import add_database_entry
    add_database_entry("David Testing", 12345, "O+")
    out_data = {"id": 12345, "test_name": "HDL", "test_result": 123}
    answer = add_test_result(out_data)
    # answer.delete()
    assert answer.tests[-1] == ("HDL", 123)

