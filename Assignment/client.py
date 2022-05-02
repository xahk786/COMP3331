"""
    Python 3
    Usage: python3 client.py server_port
    z5208639, Ali Khan
"""
from socket import *
import sys

serverName = 'localhost'

#Server would be running on the same host as Client
if len(sys.argv) != 2:
    print("\n===== Error, Usage: python3 client.py server_port ======\n")
    exit(0)
    
serverPort = int(sys.argv[1])

# define a socket for the client side, it would be used to communicate with the server
clientSocket = socket(AF_INET, SOCK_DGRAM)


def online_check(username):
    o_check = f"o_check {username}"
    clientSocket.sendto(o_check.encode('utf-8'),(serverName, serverPort))

    o_rec, serverAddress = clientSocket.recvfrom(2048)
    if int(o_rec.decode()) == 0:
        print("This user is already online, please try again.")
        return 0
    else:
        return 1


login_curr = ""

while True:
    username = input("Enter your username: ").strip()

    if online_check(username) == 0:
        continue

    user_check = f"login User {username}"
    clientSocket.sendto(user_check.encode('utf-8'),(serverName, serverPort))

    usr_rec, serverAddress = clientSocket.recvfrom(2048)
    print(usr_rec.decode('utf-8'))

    if usr_rec.decode() == "Invalid username":
        print(f"Creating a new account with username: {username}")
        passw = input("Please your password: ").strip()
        new_acc = f"login new_acc {username} {passw}"
        clientSocket.sendto(new_acc.encode('utf-8'),(serverName, serverPort))

        new_acc_rec, serverAddress = clientSocket.recvfrom(2048)
        print(new_acc_rec.decode('utf-8'))
        
        login_curr = username
        print(f"Welcome {username}")
        break

    if usr_rec.decode() == "Valid username":
        password = input("Enter your password: ").strip()
        pass_check = f"login Pass {password} {username}"
        clientSocket.sendto(pass_check.encode('utf-8'),(serverName, serverPort))

        pass_rec, serverAddress = clientSocket.recvfrom(2048)
        print(pass_rec.decode('utf-8'))

        if pass_rec.decode() == "Valid Password":
            login_curr = username
            print(f"Welcome {username}")
            break
        else:
            print("Error: Password for this user is incorrect")


online = f"add_online {login_curr}"   
clientSocket.sendto(online.encode('utf-8'),(serverName, serverPort))

while 1:
    command = input("Enter a command: ")

    if command == "XIT":
        msg = f"XIT {login_curr}"
        clientSocket.sendto(msg.encode('utf-8'),(serverName, serverPort))
        bye_rec, serverAddress = clientSocket.recvfrom(2048)
        print(bye_rec.decode('utf-8'))
        break
    
    if command.split()[0] == "CRT":
        msg = f"CRT {command.split()[1]} {login_curr}"
        clientSocket.sendto(msg.encode('utf-8'),(serverName, serverPort))
        thrd_rec, serverAddress = clientSocket.recvfrom(2048)
        print(thrd_rec.decode('utf-8'))

    if command.split()[0] == "MSG":
        cmd = command.split()[0]
        title = command.split()[1]
        sentence = " ".join(command.split()[2:])
        msg = f"{cmd} {login_curr} {title} {sentence}"
        clientSocket.sendto(msg.encode('utf-8'),(serverName, serverPort))
        MSG_rec, serverAddress = clientSocket.recvfrom(2048)
        print(MSG_rec.decode('utf-8'))
    
    if command.split()[0] == "DLT":
        cmd = command.split()[0]
        title = command.split()[1]
        num = command.split()[2]
        msg = f"{cmd} {login_curr} {title} {num}"
        clientSocket.sendto(msg.encode('utf-8'),(serverName, serverPort))
        del_rec, serverAddress = clientSocket.recvfrom(2048)
        print(del_rec.decode('utf-8'))

    if command.split()[0] == "EDT":
        cmd = command.split()[0]
        title = command.split()[1]
        num = command.split()[2]
        edit = " ".join(command.split()[3:])
        msg = f"{cmd} {login_curr} {title} {num} {edit}"
        clientSocket.sendto(msg.encode('utf-8'),(serverName, serverPort))
        edt_rec, serverAddress = clientSocket.recvfrom(2048)
        print(edt_rec.decode('utf-8'))
    
    if command.split()[0] == "LST":
        clientSocket.sendto(f"LST".encode('utf-8'),(serverName, serverPort))
        lst_rec, serverAddress = clientSocket.recvfrom(2048)
        print(lst_rec.decode('utf-8'))
    
    if command.split()[0] == "RDT":
        title = command.split()[1]
        clientSocket.sendto(f"RDT {title}".encode('utf-8'),(serverName, serverPort))
        rdt_rec, serverAddress = clientSocket.recvfrom(2048)
        print(rdt_rec.decode('utf-8'))
    
    if command.split()[0] == "RMV":
        title = command.split()[1]
        clientSocket.sendto(f"RMV {login_curr} {title}".encode('utf-8'),(serverName, serverPort))
        rmv_rec, serverAddress = clientSocket.recvfrom(2048)
        print(rmv_rec.decode('utf-8'))
    
    if command.split()[0] == "UPD":
        thread = command.split()[1]
        upd_file = command.split()[2]
        clientSocket.sendto(f"UPD {login_curr} {thread} {upd_file}".encode('utf-8'),(serverName, serverPort))
        upd_rec, serverAddress = clientSocket.recvfrom(2048)
        out = upd_rec.decode('utf-8')
        print(out)
        if (out == "File ready to upload"):
            #set up tcp and upload file 
            clientSocket_tcp = socket(AF_INET, SOCK_STREAM)
            clientSocket_tcp.connect((serverName, serverPort))
            data = open(upd_file, 'rb').read()

            clientSocket_tcp.send(data)
            clientSocket_tcp.close()
            uplr_rec, serverAddress = clientSocket.recvfrom(2048)
            print(uplr_rec.decode('utf-8'))
    
    if command.split()[0] == "DWN":
        title = command.split()[1]
        f_name = command.split()[2]
        clientSocket.sendto(f"DWN {title} {f_name}".encode('utf-8'),(serverName, serverPort))
        
        dld_rec, serverAddress = clientSocket.recvfrom(2048)
        out = dld_rec.decode('utf-8')
        print(out)
        if out == "File successfully found, downloading....":
            clientSocket_tcp = socket(AF_INET, SOCK_STREAM)
            clientSocket_tcp.connect((serverName, serverPort))

            data = clientSocket_tcp.recv(1024)
            big = data
            data = clientSocket_tcp.recv(1024)
            while data:
                big = big + data
                data = clientSocket_tcp.recv(1024)

            f = open(f_name, "wb")
            f.write(big)
            f.close()

            clientSocket_tcp.close()

clientSocket.close()




