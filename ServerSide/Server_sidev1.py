#import Libraries
import socket
import os


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #protocol type
host = socket.gethostbyname(socket.gethostname()) #get the local ip
print(host)

server.bind((host, 1200)) #Bind the port to listen n socket address
server.listen(5)

dir_name = 'serverFile' #specified directory path to save server file
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #BASE_DIR is project directory.
FILE_DIR = os.path.join(BASE_DIR, dir_name) #path to server file
file_name = sorted(os.listdir(FILE_DIR)) #Get the name of server file and put in a list
#FILEDIR = os.path.join(BASE_DIR)
#filname = sorted(os.listdir(FILE_DIR))
file_name = ' '.join(i for i in file_name) #Join Server file Name

print("[WAITING] Waiting for connection.......")


while True:
    conn, addr = server.accept()
    print("Connection Established with: ", format(addr)) #get request from client

    while True:
        data = conn.recv(1024) #Receiving data from client
        print("Recv from Client: ", data)
        command = data.decode()
        if not data:
            print("Connection Lost")
            break
        
        #command for Chating
        if data.decode('utf-8', errors='ignore') == 'chat':
            while True:
                msg = input(str("Server: ")) #input dari server
                msg = msg.encode()
                conn.send(msg)

                rply = conn.recv(1024) #reply from client
                rply = rply.decode()
                print("Client: ", rply)
                if rply == 'break':
                    break

        #Command to display available data ini server         
        if data.decode('utf-8', errors='ignore') == 'SHOWING MENU':
            conn.send(file_name.encode('utf-8', errors='ignore'))

        #Command for break
        elif data.decode('utf-8', errors='ignore') == 'break':
            break

        #Command for send data to client
        else:
            filee_name = data.decode('utf-8', errors='ignore')
            file_path = os.path.join(FILE_DIR, filee_name) #take specified data path in serverFile
            file_size = os.stat(file_path).st_size #to get the size of data in byte
            file_info = '%s|%s' %(filee_name, file_size) #to send data info (name and size)
            conn.sendall(bytes(file_info, 'utf-8', errors='ignore'))
            f = open(file_path, 'rb')
            has_sent = 0
            while has_sent != file_size:
                file = f.read(1024)
                conn.sendall(file)
                has_sent += len(file)
            f.close()
            print("Sending Successful")
    break
server.close()


