import random
import osprint
import getpass

def get_users():
  from main import list_of_users
  users = list_of_users.keys()
  
  return users

def user_exists(username, users):
  if username in users:
    valid = False
  else:
    valid = True
  
  return valid
  
def create_user():
  username = str(input("Enter Username: "))
  password = getpass.getpass(prompt="Enter Password: ")
  password = hash(password)
  hp = 10
  items = {}
  money = 50
  users = get_users()
  valid = user_exists(username, users)
  if valid == True:
    print("Creating User...")
    from main import list_of_users
    print(list_of_users)
    list_of_users[username] = {"password": password, "hp": hp, "items": items, "money": money}
    open("users.txt", "w").close()
    f = open("users.txt", "w")
    f.write(list_of_users)
    f.close
  else:
    print("User already exists. \n ")
    create_user()
    
def login():
  username = str(input("Enter Username: "))
  password = getpass.getpass(prompt="Enter Password: ")
  password = 
