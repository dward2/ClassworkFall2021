from health_db_server import initialize_server

initialize_server()


def test_add_database_entry():
    from health_db_server import add_database_entry
    expected_name = "David Testing"
    answer = add_database_entry(expected_name, 5, "O+")
    answer.delete()  # This deletes the entry in the database, it does not
    # delete the answer variable
    assert answer.name == expected_name


# def test_find_patient():
#     from health_db_server import find_patient
#     from health_db_server import add_database_entry
#     db.clear()
#     add_database_entry("David", 1, "O+")
#     answer = find_patient(1)
#
#     assert answer == expected
