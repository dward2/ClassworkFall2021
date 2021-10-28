from health_db_server import db
from health_db_server import initialize_server

initialize_server()


def test_add_database_entry():
    from health_db_server import add_database_entry
    expected_name = "David"
    answer = add_database_entry(expected_name, 5, "O+")
    print(answer)
    answer.delete()
    assert answer.name == expected_name


# def test_find_patient():
#     from health_db_server import find_patient
#     from health_db_server import add_database_entry
#     db.clear()
#     add_database_entry("David", 1, "O+")
#     answer = find_patient(1)
#
#     assert answer == expected
