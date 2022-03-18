import random
import osprint
import getpass

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
  username = str(input("Enter Username: "))
  password = getpass.getpass(prompt="Enter Password: ")
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
    open("users.txt", "w").close()
    f = open("users.txt", "w")
    f.write(list_of_users)
    f.close
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
  else:
    print("Incorrect Username or Password")
create_user()
