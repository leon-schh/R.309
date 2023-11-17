import threading
import socket

host = "0.0.0.0"
port = 6969
server_socket = socket.socket()
server_socket.bind((host, port))
server_stop = False
connected = False
text_server_stop= "\n                                 _           _                    _             \n  ___  ___ _ ____   _____ _ __  (_)___   ___| |_ ___  _ __  _ __ (_)_ __   __ _ \n / __|/ _ \ '__\ \ / / _ \ '__| | / __| / __| __/ _ \| '_ \| '_ \| | '_ \ / _` |\n \__ \  __/ |   \ V /  __/ |    | \__ \ \__ \ || (_) | |_) | |_) | | | | | (_| |\n |___/\___|_|    \_/ \___|_|    |_|___/ |___/\__\___/| .__/| .__/|_|_| |_|\__, |\n                                                     |_|   |_|            |___/\n"
clients = []
pseudo = {}

def get(client):
    global server_stop
    global pseudo
    global clients

    while not server_stop:
        if client in clients:
            try:
                message = client.recv(1024).decode()
            except ConnectionResetError:
                print("Client forcibly disconnected")
                server_stop = True
            except ConnectionAbortedError:
                print("Client forcibly disconnected")
                server_stop = True
            except OSError:
                print("client has probably disconnected")
            else:
                if message[:12] == "/\/P$eudo/\/":
                    pseudo[client] = message[12:]
                    message = "\n"+pseudo[client]+" has join the server !!!\n"
                    for client_receve in clients:
                                if client_receve != client:
                                    client_receve.send(message.encode())
                    print(f"{pseudo[client]} is connected")
                else:
                    if message == 'bye':
                        print(f"{pseudo[client]} has disconnected")
                        message = "\n"+pseudo[client]+" has left the server BYE !\n"
                        for client_receve in clients:
                            if client_receve != client:
                                client_receve.send(message.encode())
                        clients.remove(client)
                        del pseudo[client]
                        client.close()
                        
                    elif message == 'arret':
                        print(text_server_stop)
                        server_stop = True
                    else:
                        message = "\n"+"message from "+pseudo[client]+" :"+message+"\n"
                        for client_receve in clients:
                            if client_receve != client:
                                client_receve.send(message.encode())

    


def connect(client):
    global server_stop
    global clients
    
    reception = threading.Thread(target=get, args=[client])
    clients.append(client)
    reception.start()
    while not server_stop:
        if server_stop:
            for client in clients:
                    client.send(text_server_stop.encode())
      
    
    reception.join()
    for client in clients:
        client.close()

    arret_server()
            
            
def arret_server():
    server = socket.socket()
    server.connect(("localhost", port))
    server.close()



if __name__ == '__main__':
    while not server_stop:
        server_socket.listen(5)
        client_socket, address = server_socket.accept()
        if not server_stop:
            connection = threading.Thread(target=connect, args=[client_socket])
            connection.start()

    connection.join()
    server_socket.close()
    