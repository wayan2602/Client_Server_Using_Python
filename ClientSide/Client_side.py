import socket
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input(str("Enter the server adress: "))

client.connect((host,1200))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current directory

#Function to display Client Menu
def Menu():
    print("1. Request data")
    print("2. Open Data")
    print("3. Chat with Server")
    print("4. Break")
    print()


#Functin for Request Data
def req_data():
    '''Show Available Data'''
    msg = 'SHOWING MENU'.strip()  #inisiasi
    client.send(msg.encode("utf-8"))  #Encode format string to byte and send
    data = client.recv(1024)  #recv a reply from server
    print("Format request: DataName.extention")
    print("Ex: datacovid.png")
    print("\nData Available:")
    print(data.decode())
    print()

    while True:     
        msg = input("Enter Command:").strip() 
        if len(msg) == 0:
            continue
        client.send(msg.encode("utf-8"))  
        if msg == 'break':
            break
        data = client.recv(1024) 
        if len(str(data, 'utf-8').split('|')) == 2:  
            filename, filesize = str(data, 'utf8').split('|') 
            path = os.path.join(BASE_DIR, filename) 
            filesize = int(filesize)
           
            f = open(path, 'ab')  
            has_receive = 0 
            while has_receive != filesize:
                data1 = client.recv(1024) 
                f.write(data1) 
                has_receive += len(data1) 
            f.close()  
        print("Data: ", data.decode(), "is downloaded")
        os.system(msg)

def open_file():
    opt = input(str("Input File Name: "))
    while opt != 0:
        if opt == "Data_Jan.txt":
            os.system("Data_Jan.txt")
        if opt == "infovaksin1.jpg":
            os.system("infovaksin1.jpg")
        opt = input(str("Input File Name: "))

def chating():
    msg = 'chat'.strip()  
    client.send(msg.encode("utf-8"))
    print("Waiting Server to response")
    while True:
        rply = client.recv(1024)
        print("Server: ",rply.decode())
        msg = input("Client:").strip()
        client.send(msg.encode("utf-8"))
        if msg == "break":
            break


########################################################
Menu()
option = int(input("Input menu: "))

while option != 0:
    if option == 1:
        req_data()
    elif option == 2:
        open_file()
    elif option == 3:
        chating()
    else:
        print("Invalid")
        break

client.close()