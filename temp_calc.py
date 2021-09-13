def detect_fever(temperature_list):
    fever_limit = 100.0
    for temperature in temperature_list:
        if temperature >= fever_limit:
            return True
    return False
