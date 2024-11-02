# create classes for each table in the db

class User:
    def __init__(self, user_id, password, role):
        self.user_id = user_id
        self.password = password
        self.role = role