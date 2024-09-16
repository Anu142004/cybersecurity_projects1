import threading
import socket
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

def brodcast(message):
    for client in clients:
        clients.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            brodcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            brodcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break
def recieve():
    while True:
        client,address = server.accept()
        print(f"connected with {str(address)}")

        client.send('nick'.encode('ascii'))
        nickname=client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        print(f'nickname of the client is {nickname}!')
        brodcast(f'{nickname} joined the chat! '.encode(ascii))
        client.send('connected to the server!'.encode('ascii'))
        thread = threading.Thread(target=handle,args=(clients,))
        thread.start()
print("server is the liesting..")
recieve()
