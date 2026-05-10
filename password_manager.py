

import json
import os
import base64

FILE_NAME = "passwords.json"


def encrypt_password(password):

    encoded = base64.b64encode(password.encode()).decode()
    return encoded


def decrypt_password(encoded_password):
   
    decoded = base64.b64decode(encoded_password.encode()).decode()
    return decoded



def load_data():
    if not os.path.exists(FILE_NAME):
        return {}

    with open(FILE_NAME, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}



def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)




def add_credentials():
    website = input("Enter Website Name: ")
    username = input("Enter Username/Email: ")
    password = input("Enter Password: ")

    encrypted_password = encrypt_password(password)

    data = load_data()

    data[website] = {
        "username": username,
        "password": encrypted_password
    }

    save_data(data)

    print("\n Credentials Saved Successfully!\n")



def retrieve_credentials():
    website = input("Enter Website Name to Search: ")

    data = load_data()

    if website in data:
        username = data[website]["username"]
        encrypted_password = data[website]["password"]

        decrypted_password = decrypt_password(encrypted_password)

        print("\n===== SAVED CREDENTIALS =====")
        print(f"Website : {website}")
        print(f"Username: {username}")
        print(f"Password: {decrypted_password}")
        print("=============================\n")

    else:
        print("\n No credentials found for this website.\n")



def view_websites():
    data = load_data()

    if not data:
        print("\n  No saved credentials.\n")
        return

    print("\nSaved Websites:")
    print("----------------")

    for website in data:
        print(website)

    print()



def main():
    while True:
        print("========== PASSWORD MANAGER ==========")
        print("1. Add New Credentials")
        print("2. Retrieve Credentials")
        print("3. View Saved Websites")
        print("4. Exit")
        print("======================================")

        choice = input("Enter Your Choice: ")

        if choice == "1":
            add_credentials()

        elif choice == "2":
            retrieve_credentials()

        elif choice == "3":
            view_websites()

        elif choice == "4":
            print("\n Exiting Password Manager...")
            break

        else:
            print("\n Invalid Choice. Try Again.\n")



if __name__ == "__main__":
    main()