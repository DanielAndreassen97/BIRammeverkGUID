import os
import json


CRED_FILE = "users.json"


def load_credentials(cred_file: str = CRED_FILE) -> dict:
    """Load credential data from a JSON file."""
    if not os.path.exists(cred_file):
        return {}
    try:
        with open(cred_file, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_credentials(creds: dict, cred_file: str = CRED_FILE) -> None:
    """Save credential data back to the JSON file."""
    with open(cred_file, "w") as f:
        json.dump(creds, f, indent=2)


def authenticate(username: str, password: str, cred_file: str = CRED_FILE) -> bool:
    """Authenticate a user by username and password."""
    creds = load_credentials(cred_file)
    user = creds.get(username)
    if user is None:
        return False

    if isinstance(user, dict):
        stored_pw = user.get("password")
    else:
        stored_pw = user
    return stored_pw == password


def get_customers(username: str, cred_file: str = CRED_FILE) -> list:
    """Return the list of customers associated with a user."""
    creds = load_credentials(cred_file)
    user = creds.get(username, {})
    if isinstance(user, dict):
        return user.get("customers", [])
    return []


def add_customer(username: str, customer: str, cred_file: str = CRED_FILE) -> None:
    """Add a customer to a user's profile."""
    if not customer:
        return
    creds = load_credentials(cred_file)
    user = creds.get(username)

    if user is None:
        # create new user entry
        user = {"password": "", "customers": []}
    elif isinstance(user, str):
        # upgrade simple format to new dict format
        user = {"password": user, "customers": []}

    customers = user.setdefault("customers", [])
    if customer not in customers:
        customers.append(customer)
    creds[username] = user
    save_credentials(creds, cred_file)
