def individual_serial(user) -> dict:
    return{
        "id": str(user["_id"]),
        "username": str(user["username"]),
        "full_name": str(user["full_name"]),
        "email": str(user["email"]),
        "hashed_password": str(user["hashed_password"])
    }

def list_serial(users) -> list:
    return[individual_serial(user) for user in users]