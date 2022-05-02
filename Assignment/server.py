from socket import *
from threading import Thread
import sys, select, os
from helper import authenticate, auth_user, auth_pass, message_count, remove_line, thread_fixup, aquire_threadtitles

"""
    Python 3
    Usage: python3 server.py server_port
    z5208639, Ali Khan
"""
# acquire server host and port from command line parameter
if len(sys.argv) != 2:
    print("\n===== Error usage, python3 server.py SERVER_PORT ======\n")
    exit(0)

serverPort = int(sys.argv[1])

# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('localhost', serverPort))

print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")

server = {"online": [],  
          "data": { },
          "threads": [],       
        } 

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    command = message.split()[0].decode()
       
    if (command == "o_check"):
        u_check = message.split()[1].decode()
        result = "1"
        if u_check in server["online"]:
            result = "0"
        serverSocket.sendto(result.encode(), clientAddress)

    if command == "add_online":
        u_check = message.split()[1].decode()
        if u_check not in server["online"]:
            server["online"].append(u_check)
        
    if command == "login":
            auth_check = message.split()[1].decode()
            if "User" in auth_check:
                print("New login request")
                result = auth_user(message.split()[2].decode())
                serverSocket.sendto(result.encode(), clientAddress)
            
            if "Pass" in auth_check:
                print("Password entered")
                result = auth_pass(message.split()[2].decode(), message.split()[3].decode() )
                serverSocket.sendto(result.encode(), clientAddress)
            
            if "new_acc" in auth_check:
                print("Creating an account")
                name = message.split()[2].decode()
                p_wd = message.split()[3].decode()
                line = f"{name} {p_wd}"
                with open("credentials.txt", "a") as f:
                    f.write(line)
                    f.write("\n")
                    f.close() 
                serverSocket.sendto("New account successfully created".encode(), clientAddress)

    if command == "XIT":
        usr = message.split()[1].decode()
        server["online"].remove(usr)
        serverSocket.sendto(f"Loggin off, goodbye {usr}".encode(), clientAddress)
        print(server["online"])

    if command == "CRT":
        title = message.split()[1].decode()
        usr = message.split()[2].decode()
        
        if title not in server["threads"]:
            f = open(title, "w")
            f.write(f"{usr}\n")
            f.close()
            server["threads"].append(title)
            serverSocket.sendto(f"Thread created".encode(), clientAddress)
        else:
             serverSocket.sendto(f"Thread already exists, cannot create".encode(), clientAddress)

    
    if command == "MSG":

        usr = message.split()[1].decode()
        title = message.split()[2].decode()
        encrypted = message.split()[3:]

        sentence = []
        for i in range(len(encrypted)):
            sentence.append(encrypted[i].decode())
        sentence = " ".join(sentence)

        if title in server["threads"]:
            test = open(title)
            lines = test.readlines()
            test.close()
            msg_num = message_count(title, lines)

            content = f"{msg_num} {usr}: {sentence}"

            f = open(title, "a")
            f.write(f"{content}\n")
            f.close()
            serverSocket.sendto(f"Messaged added to thread".encode(), clientAddress)
        else:
            serverSocket.sendto(f"Thread does not exist, cannot add message".encode(), clientAddress)


    if command == "EDT":
        usr = message.split()[1].decode()
        title = message.split()[2].decode()
        num = message.split()[3].decode()
        encrypted = message.split()[4:]

        msg = []
        for i in range(len(encrypted)):
            msg.append(encrypted[i].decode())
        msg = " ".join(msg)

        print(msg)

        found_exception = 0
        if title not in server["threads"]:
            serverSocket.sendto(f"Error: Thread does not exist, cannot remove message".encode(), clientAddress)
            found_exception = 1

        if found_exception == 0:
            f = open(title, 'r')
            lines = f.readlines()
            f.close()

            found = 0
            capture = ""
            name_check = ""
            for i in lines:
                if i[0] == num:
                    found = 1
                    capture = i
                    name_check = capture.split()[1]
                    name_check = name_check[:-1]
        
            if name_check != usr:
                serverSocket.sendto(f"Error: User did not send this message, cannot edit message".encode(), clientAddress) 
                
            elif found == 0:
                serverSocket.sendto(f"Error: Message # does not exist, cannot edit message".encode(), clientAddress)
            
            else:
                f = open(title, "r")
                lines = f.readlines()
                f.close()
                print(lines)
                print(capture)
                for i in range(1, len(lines)):
                    if lines[i] == capture:
                        new_msg = f"{num} {usr}: {msg}\n"
                        lines[i] = new_msg
                        break

                f = open(title, "w")
                f.writelines(lines)
                f.close()

                serverSocket.sendto(f"Message successfully edited".encode(), clientAddress)

    if command == "RMV":
        usr = message.split()[1].decode()
        title = message.split()[2].decode()

        found_exception = 0
        if title not in server["threads"]:
            serverSocket.sendto(f"Error: Thread does not exist, cannot remove thread_file".encode(), clientAddress)
            found_exception = 1
                
        if found_exception == 0:
            f = open(title, 'r')
            lines = f.readlines()
            f.close()

            examine = lines[0].replace("\n", "")

            if examine != usr:
                serverSocket.sendto(f"Error: User is not thread creator, cannot remove thread_file".encode(), clientAddress)
            else:
                os.remove(title)
                server["threads"].remove(title)
                serverSocket.sendto(f"Thread file successfully removed".encode(), clientAddress)


    if command == "DLT":

        usr = message.split()[1].decode()
        title = message.split()[2].decode()
        num = message.split()[3].decode()
        
        found_exception = 0
        if title not in server["threads"]:
            serverSocket.sendto(f"Error: Thread does not exist, cannot remove message".encode(), clientAddress)
            found_exception = 1

        if found_exception == 0:
            f = open(title, 'r')
            lines = f.readlines()
            f.close()

            found = 0
            capture = ""
            name_check = ""
            for i in lines:
                if i[0] == num:
                    found = 1
                    capture = i
                    name_check = capture.split()[1]
                    name_check = name_check[:-1]
        
            if name_check != usr:
                serverSocket.sendto(f"Error: User did not send this message, cannot remove message".encode(), clientAddress) 
                
            elif found == 0:
                serverSocket.sendto(f"Error: Message # does not exist, cannot remove message".encode(), clientAddress)
                
            else:
                remove_line(title, capture)
                lines = thread_fixup(title)

                f = open(title, "w")
                f.writelines(lines)
                f.close()

                serverSocket.sendto(f"Message successfully deleted".encode(), clientAddress)
    
    if command == "LST":
        grab = server["threads"]

        if len(grab) == 0:
            serverSocket.sendto(f"There are no existing threadtitles".encode(), clientAddress)
        else:
            lst = []
            for i in grab:
                i = i + "\n"
                lst.append(i)

            final = lst[-1].replace("\n", "")
            lst[-1] = final

            thread_files = "".join(lst)
            serverSocket.sendto(f"Here are the following threadtitles:\n{thread_files}".encode(), clientAddress)

    if command == "RDT":
        title = message.split()[1].decode()
        
        if title in server["threads"]:
            f = open(title, 'r')
            lines = f.readlines()
            f.close()
            
            contents = "Thread contains no contents"
            if (len(lines) > 1):
                lines = lines[1:]
                final = lines[-1].replace("\n", "")
                lines[-1] = final
                contents = "".join(lines)
            
            serverSocket.sendto(f"{contents}".encode(), clientAddress)
        else:
            serverSocket.sendto(f"Error, thread with this title does not exist".encode(), clientAddress)

    if command == "UPD":
        usr = message.split()[1].decode()
        title = message.split()[2].decode() 
        upd_file = message.split()[3].decode()
        
        found_exception = 0
        if title not in server["threads"]:
            serverSocket.sendto(f"Error: Thread does not exist, cannot upload file to thread".encode(), clientAddress)
            found_exception = 1
        
        if (found_exception == 0):
            error = 0

            if title in server["data"].keys():
                grab = server["data"][f"{title}"]
                for i in grab:
                    if f"{upd_file}" in i:
                        error = 1
                        break

            if error == 1:
                serverSocket.sendto(f"Error: File already exists in thread, cannot upload".encode(), clientAddress)
            else:
                serverSocket.sendto(f"File ready to upload".encode(), clientAddress)
                #set up tcp connection and upload
                serverSocket_tcp = socket(AF_INET, SOCK_STREAM)
                serverSocket_tcp.bind(('localhost', serverPort))
                serverSocket_tcp.listen(1)

                connectionSocket_tcp, addr = serverSocket_tcp.accept()

                data = connectionSocket_tcp.recv(1024)
                big = data
                data = connectionSocket_tcp.recv(1024)
                while data:
                    big = big + data
                    data = connectionSocket_tcp.recv(1024)
                data = big
                
                package = {f"{upd_file}": data}
                if title not in server["data"].keys():
                    server["data"][f"{title}"] = []

                server["data"][title].append(package)
                
                connectionSocket_tcp.close()
                
                #add record of file to thread
                f = open(title, "a")
                f.write(f"{usr} uploaded {upd_file}\n")
                f.close()

                serverSocket.sendto(f"File uploaded and record added to thread ".encode(), clientAddress)
    
    if command == "DWN":
        title = message.split()[1].decode()
        f_name = message.split()[2].decode()

        error = 1
        if title in server["threads"]:
            grab = server["data"][f"{title}"]
            for i in grab:
                if f"{f_name}" in i:
                    error = 0
                    break

        serverSocket_tcp = socket(AF_INET, SOCK_STREAM)
        serverSocket_tcp.bind(('localhost', serverPort))
        serverSocket_tcp.listen(1)
        
        if error == 1:
            serverSocket.sendto(f"Error: File does not exist in thread, cannot download".encode(), clientAddress)
        else:
            serverSocket.sendto(f"File successfully found, downloading....".encode(), clientAddress)
            
            connectionSocket_tcp, addr = serverSocket_tcp.accept()

            for i in server["data"][f"{title}"]:
                if f"{f_name}" in i:
                    connectionSocket_tcp.sendall(i[f_name])
                    break

        connectionSocket_tcp.close()

    print(server)          
