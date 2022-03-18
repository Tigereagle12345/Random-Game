import random
import os
import getpass
import json

def get_users():
  from users import list_of_users
  people = list_of_users.keys()
  
  return people

def user_exists(username, people):
  if username in people:
    valid = False
  else:
    valid = True
  
  return valid
  
def create_user():
  print("Please create your account")
  username = str(input("Enter Account Username: "))
  password = getpass.getpass(prompt="Enter Account Password: ")
  password = hash(password) 
  hp = 10
  items = {}
  money = 50.00
  people = get_users()
  valid = user_exists(username, people)
  if valid == True:
    print("Creating User...")
    from users import list_of_users
    print(list_of_users)
    list_of_users[username] = {"password": password, "hp": hp, "items": items, "money": money}
    open("users.py", "w").close()
    with open("users.py", "w") as file:
      file.write("list_of_users = ")
      file.write(json.dumps(list_of_users))
      file.close
    print("User Created\n ")
    login(people)
  else:
    print("User already exists. \n ")
    create_user(people)
    
def login(people):
  username = str(input("Enter Username: "))
  password = getpass.getpass(prompt="Enter Password: ")
  password = hash(password)
  from users import list_of_users
  pass_hash = list_of_users[username]["password"]
  if password == pass_hash and username in people:
    money = list_of_users[username]["money"]
    hp = list_of_users[username]["hp"]
    items = list_of_users[username]["items"]
    print("Logged In!")
  else:
    print("Incorrect Username or Password\n")
    login(people)
    
def start():
  print("What would you like to do?")
  starttype = str(input("1. Login to an existing account\n2. Create an account: "))
  if starttype == "1":
    people = get_users()
    login(people)
  elif starttype == "2":
    create_user()
  else:
    print("Action unavalible, please try again.\n")
    start()
