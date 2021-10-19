import requests

# Successfully add patient
patient1 = {"name": "Ann Ables", "id": 201, "blood_type": "A+"}
r = requests.post("http://127.0.0.1:5000/new_patient", json=patient1)
print(r.status_code)
print(r.text)

# Successfully add patient
patient2 = {"name": "Bob Boyles", "id": 202, "blood_type": "O-"}
r = requests.post("http://127.0.0.1:5000/new_patient", json=patient2)
print(r.status_code)
print(r.text)

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

