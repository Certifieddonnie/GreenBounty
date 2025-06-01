# myapp/firebase_utils.py
from firebase_admin import db

def get_rtdb_ref(path='/'):
    """
    Returns a reference to a specific path in the Firebase Realtime Database.
    """
    return db.reference(path)

def write_to_rtdb(path, data):
    """
    Writes data to the specified path in the Realtime Database.
    """
    ref = get_rtdb_ref(path)
    ref.set(data)
    return True

def update_rtdb(path, data):
    """
    Updates data at the specified path in the Realtime Database.
    """
    ref = get_rtdb_ref(path)
    ref.update(data)
    return True

def get_from_rtdb(path):
    """
    Retrieves data from the specified path in the Realtime Database.
    """
    ref = get_rtdb_ref(path)
    return ref.get()

def delete_from_rtdb(path):
    """
    Deletes data from the specified path in the Realtime Database.
    """
    ref = get_rtdb_ref(path)
    ref.delete()
    return True