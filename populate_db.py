import requests
from faker import Faker

# This is a little helper script to populate the database with some test data.
# It's not part of the main application, just a tool for development.

# Let's initialize the Faker library, which will help us generate fake data.
fake = Faker()

# This is the URL of the registration endpoint.
# The script will send POST requests to this URL to create new users.
API_URL = "http://127.0.0.1:8001/api/accounts/register/"

def create_user(role):
    """
    Creates a single user with the specified role.
    
    This function generates a fake username and email, then sends a POST request
    to the API to create the user in the database. It's like simulating a user
    signing up through a web form.
    """
    # Generate some plausible-looking user data.
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = f"{first_name.lower()}.{last_name.lower()}{fake.random_int(min=10, max=99)}"
    email = f"{username}@example.com"
    password = "password123"  # For testing, a simple, standard password can be used.

    # This is the data payload to send in the request.
    # It matches the fields the UserSerializer expects.
    data = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }

    # Now, make the request to the API.
    try:
        response = requests.post(API_URL, json=data)
        # Check if the request was successful.
        if response.status_code == 201:
            print(f"Successfully created {role}: {username}")
        else:
            # If something went wrong, the API should give some clues.
            print(f"Failed to create {role}: {username}. Status: {response.status_code}, Response: {response.json()}")
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")
        print("Is the Django development server running? You can start it with 'python manage.py runserver'")
        return False # Stop the script if the server can't be reached.
    return True

def main():
    """
    The main function to run the user creation script.
    """
    print("--- Starting User Population Script ---")
    
    # First, create 5 teachers.
    print("\n--- Creating Teachers ---")
    for _ in range(5):
        if not create_user("teacher"):
            break # Stop if there was a connection error.

    # Next, create 20 students.
    print("\n--- Creating Students ---")
    for _ in range(20):
        if not create_user("student"):
            break # Stop if there was a connection error.
            
    print("\n--- User Population Script Finished ---")

if __name__ == "__main__":
    main()
