import random
import os
import getpass
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

list_of_users = {}

def get_data():
  scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("python-game-344621-1c97bcf83064.json", scopes) 
  file = gspread.authorize(credentials)
  sheet = file.open("Python_MUO_Google_Sheet")
  sheet = sheet.sheet1
  num = 0
  for cell in sheet.col_values(1):
    num = num + 1

  for i in range(num):
    i = i + 1
    if not i == 1:
      user = sheet.acell("A" + str(i)).value
      password = sheet.acell("B" + str(i)).value
      hp = sheet.acell("C" + str(i)).value
      money = sheet.acell("D" + str(i)).value
      items = sheet.acell("E" + str(i)).value
      status = sheet.acell("F" + str(i)).value
      list_of_users[user] = {"password": password, "hp": hp, "money": money, "items": items, "status": status, "row": i}
  people = list_of_users.keys()

  return people
  
def get_users():
  people = get_data()
  return people

def user_exists(username, people):
  if username in people:
    valid = False
  else:
    valid = True
  
  return valid

def add_user_account(username, password):
  hp = 10
  items = [ ]
  money = 50.00
  status = "Offline"
  print("Opening sprea")
  scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("python-game-344621-1c97bcf83064.json", scopes) 
  file = gspread.authorize(credentials)
  sheet = file.open("Python_MUO_Google_Sheet")
  sheet = sheet.sheet1
  
  num = 0
  for cell in sheet.col_values(1):
    num = num + 1
  row = num + 1
  sheet.update_acell("A" + str(row), username)
  sheet.update_acell("B" + str(row), password)
  sheet.update_acell("C" + str(row), hp)
  sheet.update_acell("D" + str(row), money)
  sheet.update_acell("E" + str(row), items)
  sheet.update_acell("F" + str(row), status)

  people = get_users()

  return people
    
def create_user():
  print("Please create your account")
  username = str(input("Enter Account Username: "))
  password = getpass.getpass(prompt="Enter Account Password: ")
  password = hash(password) 
  people = get_users()
  valid = user_exists(username, people)
  if valid == True:
    print("Creating User...\n")
    people = add_user_account(username, password)
    print("User Created\n ")
    login(people)
  else:
    print("User already exists. \n ")
    create_user(people)
    
def login(people):
  username = str(input("Enter Username: "))
  password = getpass.getpass(prompt="Enter Password: ")
  password = hash(password)
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

get_data()
