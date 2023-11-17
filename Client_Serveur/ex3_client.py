import socket
import threading

host = "127.0.0.1"
port = 6969
server = socket.socket()
connected = False
conn= "Connexion au serveur réussie !"
text_server_stop=  "Le serveur s'est bien arrêté !"
bye =  'Deconnexion.'


def send(server):
    global connected
    first_connection = True
    while connected:
        if first_connection:
            message = input("Quel est votre Pseudo ? : ")
            message = "/\/P$eudo/\/"+message
            try:
                server.send(message.encode())

            except ConnectionAbortedError:
                print("Aucun serveur connecté.")
                connected = False

            except ConnectionResetError:
                print("Le serveur s'est arrêté.")
                connected = False

            else:
                if message == "bye":
                    print("Vous ne pouvez pas vous deconnecter, donnez d'abord votre pseudo.")
                    
                elif message == "arret":
                    print("Vous ne pouvez pas arrêter le serveur.")
                    
                else:
                    first_connection = False
        else:
            message = input("")
            try:
                server.send(message.encode())

            except ConnectionAbortedError:
                print("Aucun serveur connecté.")
                connected = False

            except ConnectionResetError:
                print("Le serveur s'est arrêté.")
                connected = False

            else:
                if message == "bye":
                    print(bye)
                    server.send(message.encode())
                    connected = False
                if message == "arret":
                    print("Le serveur va s'éteindre.")
                    server.send(message.encode())
                    message = server.recv(1024).decode() #attente de confirmation
                    connected = False

    server.close()


    



try:
    server.connect((host, port))
except ConnectionRefusedError:
    print("404 Server hors-ligne")
else:
    envoi = threading.Thread(target=send, args=[server])
    print(conn)
    connected = True
    envoi.start()
    while connected:
        try:
            message = server.recv(1024).decode()
        except ConnectionResetError:
            print("Le serveur s'est arrêté.")
            connected = False
        except ConnectionAbortedError:
            print("Le serveur s'est arrêté.")
            connected = False
        else:
            if message == text_server_stop:
                connected = False
            """if message == "server is shutting down, you all will be disconnected":
                print(message)
                server.close()
                connected = False
            else:"""
            print(message)

    envoi.join()
    server.close()
        
