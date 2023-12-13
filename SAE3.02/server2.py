import threading
import socket

host = "0.0.0.0"
port = 6969
server_socket = socket.socket()
server_socket.bind((host, port))
server_stop = False
text_server_stop = "Le serveur va s'éteindre."
clients = []
pseudo = {}

def get(client):
    global server_stop
    global pseudo

    while not server_stop:
        try:
            message = client.recv(1024).decode()
        except ConnectionResetError:
            print("Le client s'est déconnecté.")
            break
        except ConnectionAbortedError:
            print("Le client s'est déconnecté.")
            break
        except OSError:
            print("Le client s'est probablement déconnecté.")
            break
        else:
            if message[:12] == "/\/P$eudo/\/":
                pseudo[client] = message[12:]
                message = "\n" + pseudo[client] + " a rejoint le serveur !\n"
                broadcast(message, client)
                print(f"{pseudo[client]} est connecté !")
            else:
                process_message(message, client)

    # Supprimer le client et fermer la connexion
    remove_client(client)

def process_message(message, client):
    global server_stop

    if message == 'bye':
        print(f"{pseudo[client]} s'est déconnecté.")
        message = "\n" + pseudo[client] + " s'est déconnecté :( \n"
        broadcast(message, client)
        remove_client(client)
    else:
        # Ajoutez le nom d'utilisateur dans le message
        full_message = f"{pseudo[client]}: {message}"
        broadcast(full_message, sender_client=client)

        # Affichez le message également sur le serveur
        print(full_message)
        
def broadcast(message, sender_client=None):
    global clients

    for client in clients:
        if client != sender_client:
            try:
                client.send(message.encode())
            except socket.error as e:
                print(f"Erreur lors de l'envoi du message au client : {e}")

def remove_client(client):
    global clients
    global pseudo

    if client in clients:
        clients.remove(client)
        del pseudo[client]
        client.close()

def connect(client):
    global server_stop
    global clients

    reception = threading.Thread(target=get, args=[client])
    clients.append(client)
    reception.start()

    # Attendez que le serveur soit arrêté
    reception.join()

    # Fermer toutes les connexions client restantes
    for client in clients:
        client.close()

    # Arrêter le serveur
    arret_server()

def arret_server():
    global server_stop
    global clients

    print(text_server_stop)
    broadcast(text_server_stop)

    server_stop = True

if __name__ == '__main__':
    while not server_stop:
        server_socket.listen(5)
        client_socket, address = server_socket.accept()
        if not server_stop:
            connection = threading.Thread(target=connect, args=[client_socket])
            connection.start()

    connection.join()
    server_socket.close()