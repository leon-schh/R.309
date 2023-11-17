import socket                                   # Importer la bibliothèque socket pour gérer les connexions réseau

def client1():
    sending = True
    while sending :
        try :
            client_socket = socket.socket()                 # Créer un objet socket pour le client
            client_socket.connect(('172.20.10.3', 6984))    # Établir une connexion avec le serveur à l'adresse IP '172.20.10.3' et au port 6984
            message = input(" -> ")                         # permet au client de saisir le message à envoyer 
            client_socket.send(message.encode())            # permet d'envoyer le message au serveur 
            reply = client_socket.recv(1024).decode()       # Recevoir la réponse du serveur, la décoder en chaîne
            print(f"Réponse du serveur : {reply}")          # Afficher la réponse reçue du serveur
            if message == "bye":                            
                client_socket.close()                       # Ferme la connection avec le serveur 
                sending = False                             # Le client arrete d'envoyer au serveur
            if message == "arret":
                client_socket.close()                       # Ferme la connection avec le serveur 
                sending = False                             # Le client arrête d'envoyer au serveur
        except ConnectionRefusedError:
            print ("Erreur de connexion. Le serveur est indisponnible pour le moment.")
        except Exception :
            print ("Une erreur s'est produite.")
        finally : 
            client_socket.close()
if __name__ == "__main__":
    client1()
