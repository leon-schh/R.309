import socket                                   # Importer la bibliothèque socket pour gérer les connexions réseau

def client1():
    try :
        client_socket = socket.socket()                 # Créer un objet socket pour le client
        client_socket.connect(('172.20.10.3', 6984))    # Établir une connexion avec le serveur à l'adresse IP '172.20.10.3' et au port 6984
        message = input(" -> ")
        while message != "bye":
            client_socket.send(message.encode())
            reply = client_socket.recv(1024).decode()       # Recevoir la réponse du serveur, la décoder en chaîne
            print(f"Réponse du serveur : {reply}")          # Afficher la réponse reçue du serveur
        if message == "bye":
            print ("Déconnexion.")
            client_socket.close() 
        elif message == "arret":
            print("Arrêt du serveur.")
            client_socket.close()
    except ConnectionRefusedError:
        print ("Erreur de connexion. Le serveur est indisponnible pour le moment.")
    except Exception :
        print ("Une erreur s'est produite.")
    finally : 
        client_socket.close()
if __name__ == "__main__":
    client1()
