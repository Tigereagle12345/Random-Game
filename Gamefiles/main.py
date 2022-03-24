import random
import os
import getpass
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

list_of_users = {}

yes = ["Y", "y", "Yes", "yes"]
no = ["N", "n", "No", "no"]

ranks = ["Beggar", "Peasant", "Worker", "Trader", "Soldier", "Advisor", "Ruler"]

# -----------------------------------------------------------------------------

# Login + Setup

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
      stats = sheet.acell("G" + str(i)).value
      fstat, cstat, mstat, estat, istat = decode_stats(stats)
      mode = sheet.acell("H" + str(i)).value
      rank = sheet.acell("I" + str(i)).value
      rank = ranks[int(rank)]
      day = sheet.acell("J" + str(i)).value
      code = rank = sheet.acell("K" + str(i)).value
      list_of_users[user] = {"password": password, "hp": hp, "money": money, "items": items, "status": status, "row": i, "stats": {"fstat": fstat, "cstat": cstat, "mstat": mstat, "estat": estat, "istat": istat}, "mode": mode, "rank": rank, "day": day, "gamecode": code}
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
  items = "[ ]"
  money = 0.00
  status = "Offline"
  print("Opening spreadsheet...")
  scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("python-game-344621-1c97bcf83064.json", scopes) 
  file = gspread.authorize(credentials)
  sheet = file.open("Python_MUO_Google_Sheet")
  sheet = sheet.sheet1

  code = 0
  num = 0
  for cell in sheet.col_values(1):
    num = num + 1
  row = num + 1
  
  day = 1
  
  print("Adding Data...")
  sheet.update_acell("A" + str(row), username)
  sheet.update_acell("B" + str(row), password)
  sheet.update_acell("C" + str(row), hp)
  sheet.update_acell("D" + str(row), money)
  sheet.update_acell("E" + str(row), items)
  sheet.update_acell("F" + str(row), status)
  sheet.update_acell("G" + str(row), "None")
  sheet.update_acell("I" + str(row), 0)
  sheet.update_acell("J" + str(row), day)
  sheet.update_acell("K" + str(row), code)

  people = get_users()

  return people
    
def create_user():
  print("Please create your account")
  username = str(input("Enter Account Username: "))
  password = encrypt_pass(str(getpass.getpass(prompt="Enter Password: ")))
  people = get_users()
  valid = user_exists(username, people)
  if valid == True:
    print("Creating User...")
    people = add_user_account(username, password)
    print("User Created\n ")
    clear()
    login(people)
  else:
    print("User already exists. \n ")
    create_user(people)

def update_status(row, status):
  scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("python-game-344621-1c97bcf83064.json", scopes) 
  file = gspread.authorize(credentials)
  sheet = file.open("Python_MUO_Google_Sheet")
  sheet = sheet.sheet1

  sheet.update_acell("F" + str(row), status)

def encrypt_pass(password):
  key = "ihofhvhurhurehurhuhojrevghuoerhoeruhroej"
  key_length = len(key)
  key_as_int = [ord(i) for i in key]
  password_int = [ord(i) for i in password]
  password_encrypted = ""
  for i in range(len(password_int)):
      value = (password_int[i] + key_as_int[i % key_length]) % 26
      password_encrypted += chr(value + 65)
      
  return password_encrypted

    
def login(people):
  print("Please Login")
  username = str(input("Enter Username: "))
  password = encrypt_pass(str(getpass.getpass(prompt="Enter Password: ")))
  pass_hash = list_of_users[username]["password"]
  if password == pass_hash and username in people:
    money = list_of_users[username]["money"]
    hp = list_of_users[username]["hp"]
    items = list_of_users[username]["items"]
    user_row = list_of_users[username]["row"]
    user_data = {username: user_row}
    update_status(user_row, "Online")
    open("user_data.py", "w").close()
    with open('user_data.py', 'w') as convert_file:
     convert_file.write("user_data = " + json.dumps(user_data))
    
    print("Logged In!")
    clear()
    begin_game(username)
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

def clear():
  os.system("cls")

def pause():
  stop =  input("Enter any key to continue... ")
  clear()

def choices(num_of_options, options, username):
  nums = []
  print("What would you like to do?")
  for i in range(num_of_options):
    print(str(i + 1) + ". " + str(options[i]))
    nums.append(int(i + 1))
  answer = int(input(str(username) + ": "))
  if answer in nums:
    return answer
  else:
    print("Unavalible option, please try again\n")
    choices(num_of_options, options, username)

def reroll(end, rerolls, username, fstat, cstat, mstat, estat, istat):
  answer = input("Would you like to reroll your stats? Y/N\n")
  if answer in yes:
    stats = roll_stats(end, rerolls, username)
  elif answer in no:
    print("Stats have been finalized.")
    stats = encode_stats(fstat, cstat, mstat, estat, istat, username)
  else:
    print("Unknown answer, please try again.")
    stats = reroll(end, rerolls, username)

  return stats

def encode_stats(fstat, cstat, mstat, estat, username):
  fstat = "F" + str(fstat)
  cstat = "|C" + str(cstat)
  mstat = "|M" + str(mstat)
  estat = "|E" + str(estat)
  istat = "|I" + str(istat)
  stats = fstat + cstat + mstat + estat + istat
  
  scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("python-game-344621-1c97bcf83064.json", scopes) 
  file = gspread.authorize(credentials)
  sheet = file.open("Python_MUO_Google_Sheet")
  sheet = sheet.sheet1
  row = list_of_users[username]["row"]

  sheet.update_acell("G" + str(row), stats)
  
  return stats

def decode_stats(stats):
  fstat = stats.split("|C")[0]
  stats.replace(fstat, "")
  
  cstat = stats.split("|M")[0]
  stats.replace(cstat, "")

  mstat = stats.split("|E")[0]
  stats.replace(mstat, "")

  estat = stats.split("|I")[0]
  stats.replace(estat, "")

  istat = stats
  stats.replace(istat, "")
  
  return fstat, cstat, mstat, estat, istat

def roll_stats(end, rerolls, username):
  roll = input("\nPress enter to role stats: ")
  fstat = random.randrange(1, end, 1)
  cstat = random.randrange(1, end, 1)
  mstat = random.randrange(1, end, 1)
  estat = random.randrange(1, end, 1)
  istat = random.randrange(1, end, 1)
  print("Your stats are:\nStrength: " + str(fstat) + "\nCharisma: " + str(cstat) + "\nMagic: " + str(mstat) + "\nStamina: " + str(estat) + "\nIntelligence: " + str(istat))
  print("You have " + str(rerolls) + " rerolls left.")
  if rerolls > 0:
    answer = input("Would you like to reroll your stats? Y/N\n")
    if answer in yes:
      stats = roll_stats(end, rerolls, username)
    elif answer in no:
      print("Stats have been finalized.")
      stats = encode_stats(fstat, cstat, mstat, estat, istat, username)
    else:
      print("Unknown answer, please try again.")
      stats = reroll(end, rerolls, username, fstat, cstat, mstat, estat, istat)
  else:
    stats = encode_stats(fstat, cstat, mstat, estat, istat, username)
  
  return stats

def choose_mode(username):
  modes = ["Easy", "Normal", "Hard", "Impossible"]

  row = list_of_users[username]["row"]
  scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("python-game-344621-1c97bcf83064.json", scopes) 
  file = gspread.authorize(credentials)
  sheet = file.open("Python_MUO_Google_Sheet")
  sheet = sheet.sheet1

  mode = sheet.acell("H" + str(row)).value
  stats = sheet.acell("G" + str(row)).value
  if mode in modes:
    if stats != "None":
      play(username)
    else:
      print("Choose a gamemode: \n\n")
      choice = int(input("1. Easy\n2. Normal\n3. Hard\n4. Impossible\n" + str(username) + ": "))
      if choice == 1:
        mode = "Easy"
        end = 20
        rerolls = 3
      elif choice == 2:
        mode = "Normal"
        end = 15
        rerolls = 2
      elif choice == 3:
        mode = "Hard"
        end = 10
        rerolls = 1
      elif choice == 4:
        mode = "Impossible"
        end = 5
        rerolls = 0
      else:
        print("Invalid choice, please try again")
        clear()
        choose_mode(username)
      stats = roll_stats(end, rerolls)

    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("python-game-344621-1c97bcf83064.json", scopes) 
    file = gspread.authorize(credentials)
    sheet = file.open("Python_MUO_Google_Sheet")
    sheet = sheet.sheet1
    row = list_of_users[username]["row"]

    sheet.update_acell("H" + str(row), mode)

    play(username)

def exit_game(mode, username, stats):
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("python-game-344621-1c97bcf83064.json", scopes) 
    file = gspread.authorize(credentials)
    sheet = file.open("Python_MUO_Google_Sheet")
    sheet = sheet.sheet1
    
    row = list_of_users[username]["row"]
    money = list_of_users[username]["money"]
    hp = list_of_users[username]["hp"]
    items = list_of_users[username]["items"]
    
    sheet.update_acell("C" + str(row), hp)
    sheet.update_acell("D" + str(row), money)
    sheet.update_acell("E" + str(row), items)
    sheet.update_acell("G" + str(row), stats)
    sheet.update_acell("H" + str(row), mode)
    
    os.system("python log_off.py")
    exit()

# -----------------------------------------------------------------------------

# Game

def begin_game(username):
  clear()
  answer = choices(3, ["Tutorial", "Begin Game", "End Game"], username)
  if answer == 1:
    clear()
    print("Tutorial:\n")
    print("\n")
    print("This is a game where the goal is to rise through the city's hierarchy and conquer new lands until you are the ruler of the world!\nTo acomplish this, you will have to make many decisions, which will all influence your future.")
    print("\n\n")
    print("How a turn works:")
    print("\n\n")
    print("Each turn, you will recive a report which will contain information about your money, current rank, territories you control and more! Based on this information, you will make your decisions.")
    print("Similarly to role-playing game, you will have several possible actions for most situations, such as a choice between fighting someone and choosing to bribe them. This means that you will have stats, which will be randomly generated and can improve over time.")
    print("The game will start after you proceed.\nHave Fun!")
    pause()
    choose_mode(username)
  elif answer == 2:
    choose_mode(username)
  elif answer == 3:
    exit_game("", username, "")
  else:
    print("ERROR: Answe doesn't exist")
    answer = choices(3, ["Tutorial", "Begin Game", "End Game"], username)

def report(username):
  print("\nReport:\n\n")
  print("Rank: "  + str(list_of_users[username]["rank"]))
  print("Day: " + str(list_of_users[username]["day"]))
  print("Hp: " + str(list_of_users[username]["hp"]))
  print("Money: $" + str(list_of_users[username]["money"]))
  pause()

def play(username):
  code = list_of_users[username]["gamecode"]
  rank = list_of_users[username]["rank"]
  money = list_of_users[username]["money"]
  hp = list_of_users[username]["hp"]
  day = list_of_users[username]["day"]
  start = 0
  end = 0
  step = 0
  
  print("Welcome to the city!\nYour current rank is " + str(rank))
  print("The day is day " + str(day))
  print("Hp: " + str(hp))
  print("Money: $" + str(money))
  pause()
  while 1 == 1:
    report(username)
    if day == encounters[code]["when"]:
      print(encounters[code]["desc"] + "\n")
      answer = choices(encounters[code]["num"], encounters[code]["options"], username)
      money, hp, rank = encounters[code]["function"](money, hp, rank, answer)
      code = code + 1
    else:
      if rank == ranks[0]:
        start = 0.01
        end = 3.76
        step = 0.01
      elif rank == ranks[1]:
        start = 0.1
        end = 10.00
        step = 0.1
      elif rank == ranks[2]:
        start = 1
        end = 15.00
        step = 0.5
      elif rank == ranks[3]:
        start = 10
        end = 30
        step = 1
      elif rank == ranks[4]:
        start = 25
        end = 250
        step = 20
      elif rank == ranks[5]:
        start = 500
        end = 5000
        step = 50
      elif rank == ranks[6]:
        start = 1000
        end = 50000.00
        step = 100
      gain = random.randrange(start, end, step)
      money = float(money) + float(gain)
      print("You made $" + str(gain))
      print("You now have $" + str(money))

# -----------------------------------------------------------------------------

# Levels
def en_zero(money, hp, rank, answer):
  if answer == 1:
    print("The man thanks you for returning his purse and gives you $50. He also says that he is a merchant and offers to hire you for a month at half pay and after that will pay you full pay. However, doing this would mean that you would have to pay for transport to work which would be $25 a month (Money will be payed now).")
    answer = input("Do you accept? Y/N: ")
    if answer in yes:
      rank = "Worker"
      money = money + 25
      print("You are now have the rank worker!")
  elif answer == 2:
    money = money + 100
    print("You got $100 more dollars")
    print("You now have $" + str(money))
    rank = "Peasant"
  
  return money, hp, rank

encounters = {
      0: {"when": 5, "desc": "One day, while you are begging in the city, a man comes and tips you $5 before leaving. While he is leaving, however, he drops his purse, which you pick up. In it is $100, more money than you have seen in your life!", "num": 2, "options": ["Run after him and give him his purse back", "Keep the money for yourself"], "function": en_zero}
      #1: {"when": 20, "desc": "", "num": 3, "options": [""], "function": en_one}
      #2: {"when": 50, "desc": "", "num": 3, "options": [""], "function": en_two}
      #3: {"when": 70, "desc": "", "num": 3, "options": [""], "function": en_three}
  }
# -----------------------------------------------------------------------------

# Code

start()
