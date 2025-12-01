
import requests
from faker import Faker

# This script helps to quickly fill your database with test users for development.
# This is not part of the main app—just a handy tool for local testing and demos.

# Here the Faker library will generate realistic names and emails, no need to make them up yourself.
fake = Faker()

# This is the API endpoint where new users get registered.
# We'll send POST requests here to add users to the database.
API_URL = "http://127.0.0.1:8001/api/accounts/register/"

def create_user(role):
    """
    Create a single user with the given role (either 'teacher' or 'student').

    Function makes up a name and email, then sends them to the API as if a real person was signing up.
    Perfect way to fill your database for testing features that need users.
    """
    # Make up a realistic name and email for this user.
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = f"{first_name.lower()}.{last_name.lower()}{fake.random_int(min=10, max=99)}"
    email = f"{username}@example.com"
    password = "password123"  # Simple password for all test users—easy to remember during development.

    # Build the data dictionary to send to the API. These fields match what the backend expects.
    data = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }

    # Send the registration request. If the server isn't running, let the developer know.
    try:
        response = requests.post(API_URL, json=data)
        # If the user was created, print a success message.
        if response.status_code == 201:
            print(f"Successfully created {role}: {username}")
        else:
            # If something went wrong, show the error details so it's easier to debug.
            print(f"Failed to create {role}: {username}. Status: {response.status_code}, Response: {response.json()}")
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")
        print("Is the Django development server running? Start it with 'python manage.py runserver'.")
        return False # If unable to reach the server, stop the script so you can fix it.
    return True

def main():

    """
    This is the entry point for the script. It creates teachers and students for testing.

    Script can be run whenever fresh test users are needed in the local database.
    """
    print("--- Starting User Population Script ---")

    # First add 5 teachers to the database.
    print("\n--- Creating Teachers ---")
    for _ in range(5):
        if not create_user("teacher"):
            break # If a connection error is hit, stop so you can fix the server.

    # Add 20 students.
    print("\n--- Creating Students ---")
    for _ in range(20):
        if not create_user("student"):
            break # Again, stop if there's a connection problem.
            
    print("\n--- User Population Script Finished ---")

if __name__ == "__main__":
    main()
