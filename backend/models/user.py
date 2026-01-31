import extensions
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    @staticmethod
    def create_user(name, email, password, role="user"):
        hashed_password = generate_password_hash(password)

        user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role
        }

        return extensions.db.users.insert_one(user)

    @staticmethod
    def find_by_email(email):
        return extensions.db.users.find_one({"email": email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
