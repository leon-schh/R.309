import socket                                           # Importer la bibliothèque socket pour gérer les connexions réseau

server_socket = socket.socket()                         # Créer un objet socket pour le serveur
server_socket.bind(('0.0.0.0', 6984))                   # Associer le socket à l'adresse IP '0.0.0.0' (écoute de toutes les interfaces) et au port 6984
server_socket.listen(1)                                 # Écouter les connexions entrantes, avec une file d'attente pour une connexion

conn, address = server_socket.accept()                  # Accepter une connexion entrante et obtenir un objet de connexion (conn) et l'adresse du client (address)
message = conn.recv(1024).decode()                      # Recevoir des données (message) du client, les décoder en chaîne

if message == "bye":
        print("Le serveur a reçu la commande bye. Arret de la connexion.")
        reply = "La connexion au serveur va se couper. Au revoir !"
        conn.send(reply.encode())                               # Envoyer la réponse encodée au client
        conn.close()                                            # Fermer la connexion avec le client
else: 
    while message !="bye":
        print(f"Le serveur a reçu le message : {message}")      # Afficher le message reçu du client
        reply = f"Le serveur a bien reçu le message : {message}"                  # Créer une réponse à envoyer au client
        conn.send(reply.encode())                               # Envoyer la réponse encodée au client
        #conn.close()                                            # Fermer la connexion avec le client
        #server_socket.close()                                   # Fermer le socket du serveur

    print("Le serveur a reçu la commande bye. Arrêt de la connexion.")
    reply = "La connexion au serveur va se couper. Au revoir !"
    conn.send(reply.encode())
    conn.close()

    

