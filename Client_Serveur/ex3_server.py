import threading
import socket

host = "0.0.0.0"
port = 6969
server_socket = socket.socket()
server_socket.bind((host, port))
server_stop = False
connected = False
text_server_stop= "Le serveur va s'éteindre."
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
                print("Le client s'est déconecté.")
                server_stop = True
            except ConnectionAbortedError:
                print("Le client s'est déconecté.")
                server_stop = True
            except OSError:
                print("Le client s'est probablement déconnecté.")
            else:
                if message[:12] == "/\/P$eudo/\/":
                    pseudo[client] = message[12:]
                    message = "\n"+pseudo[client]+" a rejoint le serveur !\n"
                    for client_receve in clients:
                                if client_receve != client:
                                    client_receve.send(message.encode())
                    print(f"{pseudo[client]} est connecté !")
                else:
                    if message == 'bye':
                        print(f"{pseudo[client]} s'est déconnecté.")
                        message = "\n"+pseudo[client]+" a quitté le serveur :( \n"
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
                        message = "\n"+"message de  "+pseudo[client]+" : "+message+"\n"
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
    