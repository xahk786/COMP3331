import os

def authenticate(credentials):
    txt_file = "credentials.txt"

    with open("credentials.txt") as f:
        lines = f.readlines()
        for i in lines:
            if credentials in i:
                return "Valid login"
    
    return "Invalid login"
                
def auth_user(username):
    txt_file = "credentials.txt"

    with open("credentials.txt") as f:
        lines = f.readlines() #lines is a list of strings, where each string is a line in the text file 
        for i in lines:
            check = i.split()[0]
            if check == username:
                return "Valid username"
    
    return "Invalid username"

def auth_pass(password, username):
    txt_file = "credentials.txt"

    with open("credentials.txt") as f:
        lines = f.readlines() #lines is a list of strings, where each string is a line in the text file 
        for i in lines:
            check_user = i.split()[0]
            if check_user == username:
                check_pass = i.split()[1]
                if check_pass == password:
                    return "Valid Password" 
    
    return "Invalid password"

def message_count(file_name, lines):

    msg_num = 1
    for i in range(1, len(lines)):
        check = lines[i].split()
        if check[0].isdigit() == True and check[1] == "name:":
            msg_num = msg_num + 1
    
    return msg_num

def remove_line(file_name, target):
    fp = open(file_name, "r")
    lines = fp.readlines()
    fp.close()

    fl = open(file_name, "w")
    for line in lines:
        if line != target:
            fl.write(line)
    fl.close()

def thread_fixup(file_name):
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    
    count = 1
    for i in range(1, len(lines)):
        curr = lines[i].split()
        if curr[0].isdigit() == True and curr[1] == "name:":
            check = lines[i][0]
            repl= f"{count}"
            if check != repl:
                lines[i] = lines[i].replace(lines[i][0], repl, 1)
            count = count + 1

    return lines

def aquire_threadtitles():
    files = os.listdir('.')
    lst = []
    for i in files:
        if '.' not in i and os.path.isfile(i):
            i = i + "\n"
            lst.append(i)
    return lst