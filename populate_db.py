
import requests
from faker import Faker

# This script helps you quickly fill your database with test users for development.
# It's not part of the main app—just a handy tool for local testing and demos.

# We use the Faker library to generate realistic names and emails, so you don't have to make them up yourself.
fake = Faker()

# This is the API endpoint where new users get registered.
# We'll send POST requests here to add users to the database.
API_URL = "http://127.0.0.1:8001/api/accounts/register/"

def create_user(role):
    """
    Create a single user with the given role (either 'teacher' or 'student').

    This function makes up a name and email, then sends them to the API as if a real person was signing up.
    It's a quick way to fill your database for testing features that need users.
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

    # Try to send the registration request. If the server isn't running, let the developer know.
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
        return False # If we can't reach the server, stop the script so you can fix it.
    return True

def main():

    """
    This is the entry point for the script. It creates teachers and students for testing.

    Run this script whenever you need fresh test users in your local database.
    """
    print("--- Starting User Population Script ---")

    # First, let's add 5 teachers to the database.
    print("\n--- Creating Teachers ---")
    for _ in range(5):
        if not create_user("teacher"):
            break # If we hit a connection error, stop so you can fix the server.

    # Now, let's add 20 students.
    print("\n--- Creating Students ---")
    for _ in range(20):
        if not create_user("student"):
            break # Again, stop if there's a connection problem.
            
    print("\n--- User Population Script Finished ---")

if __name__ == "__main__":
    main()
