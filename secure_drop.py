import json
import hashlib
import socket
import sys

path_to_json = "./user.json"
path_to_contacts= "./contacts.json"

def add_user():
    #Opens user.json file then asks for Full name and Email
    handler = open(path_to_json, "r")
    json_object = json.load(handler)
    handler.close()
    handler = open(path_to_json, "w+")
    name = input("Enter Full Name:")
    json_object["name"] = name
    email = input("Enter Email Address:")
    
    #Hash email address then store into json file
    salt = "$2b$12$tpoiOiogc8o8I/p5Cdpkje"
    hashed_email = email + salt
    hashed_email = hashlib.md5(hashed_email.encode())
    hashed_email = hashed_email.hexdigest()
    json_object["email"] = hashed_email
    
    #Ask for password and makes sure it matches
    password1 = input("Enter Password:")
    password2 = input("Re-enter Password:")
    while  password1 != password2:
        print("Passwords did not match try again")
        password1 = input("Enter Password:")
        password2 = input("Re-enter Password:")
    print("User has succesfully registered")

    #Hash password then store into json file 
    salt = "$2b$12$tpoiOiogc8o8I/p5Cdpkje"
    hashed_password = password1 + salt
    hashed_password = hashlib.md5(hashed_password.encode())
    hashed_password = hashed_password.hexdigest()
    json_object["passwords"] = hashed_password
    json.dump(json_object, handler)
    handler.close()

def user_login():
    attempts = 1
    max_attempts = 3
    handler = open(path_to_json, "r")
    json_object = json.load(handler)
    inputted_email = input("Enter Email Address:")
    
    #Hash email2 to see if it matches with hashed email1
    salt = "$2b$12$tpoiOiogc8o8I/p5Cdpkje"
    hashed_email2 = inputted_email + salt
    hashed_email2 = hashlib.md5(hashed_email2.encode())
    hashed_email2 = hashed_email2.hexdigest()
    
    json_email = json_object["email"]
    inputted_password = input("Enter password:")
    
    #Hash password2 to see if it matches with hashed password
    salt = "$2b$12$tpoiOiogc8o8I/p5Cdpkje"
    hashed_password2 = inputted_password + salt
    hashed_password2 = hashlib.md5(hashed_password2.encode())
    hashed_password2 = hashed_password2.hexdigest()
    json_password = json_object["passwords"]
    
    while attempts < max_attempts:
        if json_email == hashed_email2 and json_password == hashed_password2:
            print("Welcome to Secure Drop!")
            break
        else:
            #Hashing of inputted email and password to see if it matches with the user.json file
            print("Email and Password combination invalid.")
            attempts+=1
            inputted_email = input("Enter Email Address:")
            inputted_password = input("Enter password:")
            salt = "$2b$12$tpoiOiogc8o8I/p5Cdpkje"
            hashed_email2 = inputted_email + salt
            hashed_password2 = inputted_password + salt
            hashed_email2 = hashlib.md5(hashed_email2.encode())
            hashed_password2 = hashlib.md5(hashed_password2.encode())
            hashed_email2 = hashed_email2.hexdigest()
            hashed_password2 = hashed_password2.hexdigest()
            
            if attempts == max_attempts:
                print("Max attempts has been reached. Exiting program")
                #exit()
            continue


def menu():
    command = input("Type \"help\" for commands\n")
    if command == "help":
        print("\"add\" -> Add a new contact")
        print("\"list\" -> List all online contacts")
        print("\"send\" -> Transfer file to contact")
        print("\"exit\" -> Exit SecureDrop")

    while 1:    
        command = input("Type your command\n")
        if command == "exit":
            exit()
        if command == "add":
            add()
        if command == "list":
            list()
        if command == "send":
            send()
        
        print("\"add\" -> Add a new contact")
        print("\"list\" -> List all online contacts")
        print("\"send\" -> Transfer file to contact")
        print("\"exit\" -> Exit SecureDrop")

def add():
    #Opens contact.json file to input contacts
    contacts = open(path_to_contacts, "r+")
    json_object = json.load(contacts)
    name = input("Enter Contact Name:")
    email = input("Enter Contact Email Address:")
    #Adding new contacts to the end of the json object
    json_object["contacts"][0][name] = email
    
    #Re-opens the contact.json file but deletes everything in it to add the new json object with the new contacts
    contacts = open(path_to_contacts, "w")
    json.dump(json_object, contacts)
    print("Contact added successfully")
    contacts.close()

#Since we were not able to figure out how to tell if a contact was online, we just printed all the contacts
def list():
    #Opens contact.json file to read the data
    contacts = open(path_to_contacts,"r")
    json_object = json.load(contacts)
    print("Contacts: ")
    #Loops throught the json_object to print all the key-value pairs
    for k in json_object["contacts"][0]:
        print(k,"'s email is:", json_object["contacts"][0][k])

def send():
    #IP and Port are hard-coded due to that we were not able to figure this part out
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4467
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 2048

    #Starting up and connecting to the TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    #Opens up the file with the correct file pathway 
    filename = input("Please enter the path of the file you would like to send:")
    message = open(filename, "rb")
    data = message.read(SIZE)

    #Sends filename to the server
    client.send(filename.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    #Sends file data to the server
    while data:
        client.send(data)
        data = message.read(SIZE)

    message.close()
    client.close()
    print("File Transfer Successful")

#start of main function
handler = open(path_to_json, "r")
info = json.load(handler)
users = info["email"]
passwords = info["passwords"]

#Checks to see if there is nothing in email or password fields of the user.json file
if len(info['email']) == 0 or len(info['passwords']) == 0:
    print("No users are registered with this client.")
    handler.close()
    response = input("Do you want to register a new user (y/n)?")
    if response == 'y' or response == 'Y':
        add_user()
    elif response == 'n' or reponse == 'N':
        print("Exiting secure drop");
        exit()
else:
    user_login()
    menu()
