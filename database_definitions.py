from pymodm import MongoModel, fields


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
