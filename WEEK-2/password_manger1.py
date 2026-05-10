import json
import base64
import os

FILE_NAME = "passwords.json"


def save_password():
    website = input("Enter Website Name: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    encoded_password = base64.b64encode(password.encode()).decode()

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
    else:
        data = {}

    data[website] = {
        "username": username,
        "password": encoded_password
    }

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

    print("Password Saved Successfully!")


def get_password():
    website = input("Enter Website Name: ")

    if not os.path.exists(FILE_NAME):
        print(" No Data Found")
        return

    with open(FILE_NAME, "r") as file:
        data = json.load(file)

    if website in data:
        username = data[website]["username"]
        encoded_password = data[website]["password"]

        # Decode Password
        password = base64.b64decode(encoded_password.encode()).decode()

        print("\nSaved Credentials")
        print("-------------------")
        print("Website :", website)
        print("Username:", username)
        print("Password:", password)

    else:
        print(" Website Not Found")


while True:

    print("\n===== PASSWORD MANAGER =====")
    print("1. Save Password")
    print("2. Get Password")
    print("3. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        save_password()

    elif choice == "2":
        get_password()

    elif choice == "3":
        print("Thank You!")
        break

    else:
        print("Invalid Choice")