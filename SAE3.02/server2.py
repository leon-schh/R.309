import sys
import socket
import threading
from threading import Event
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QComboBox, QLabel, QMessageBox, QDialog
import mysql.connector

# Connexion à la base de données
conn = mysql.connector.connect(host="localhost", user="root", password="root", database="serveur")
cursor = conn.cursor()

class LoginDialog(QDialog):
# Classe qui gère l'interface d'authetification
    def __init__(self, parent=None):
        # Configuration de l'interface 
        super().__init__(parent)
        self.setWindowTitle("Authentification")

        self.label_username = QLabel("Nom d'utilisateur : ")
        self.edit_username = QLineEdit(self)

        self.label_password = QLabel("Mot de passe : ")
        self.edit_password = QLineEdit(self)
        self.edit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Se connecter", self)
        self.btn_login.clicked.connect(self.login)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_username)
        layout.addWidget(self.edit_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.edit_password)
        layout.addWidget(self.btn_login)

        # Configuration du style
        self.setStyleSheet("""
            QWidget {
                background-color: #000; 
                color: #eb232d; /* Couleur du texte par défaut */
                font-family: monospace;
                font-size : 20px;
            }
            
            QTextEdit, QLineEdit {
                background-color: #3b3c47; 
                color: #fff; 
                border: 1px solid #eb232d; /* Bordure autour des zones de texte */
                padding: 5px; 
            }

            QPushButton {
                border: 5px solid #eb232d;
                border-radius: 8px
                border: 5px solid #eb232d
                padding 1px 5px;
                min-width: 120px;
                min-height: 35px;
                background-color: #eb232d;
                color: #000; 
            }

            QPushButton:hover {
                background-color: #eb232d;
            }
        """)

    
    def show_error_message(self, message):
    # Fonction qui permet d'afficher des messages d'erreurs dans une fenêtre
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Erreur")
        error_dialog.setText(message)
        error_dialog.exec()

    def login(self):
    #Fonction qui gère l'authentification des clients 
        username = self.edit_username.text()
        password = self.edit_password.text()

        if self.check_login(username,password) :
            self.accept()
        else : 
            print ("Identifient ou mot de passe incorrect")

    def check_login (self,username, password):
    # Fonction qui vérifie que le nom d'utilisateur et le mot de passe sont correct
        try:
            cursor.execute("SELECT * FROM admin WHERE username=%s AND passwd=%s", (username, password))
            result = cursor.fetchone()

            if result:
                return True
            else : 
                self.show_error_message("Identifiant ou mot de passe incorrect")
                return False
            
        except mysql.connector.errors:
            self.show_error_message("erreur de base de donées.")
            return False
        
class ServerApp(QWidget):
# Classe du serveur
    def __init__(self):
    # Créer l'interface du serveur 
        super().__init__()

        self.server_socket = socket.socket()
        self.server_socket.bind(("0.0.0.0", 6969))
        self.server_socket.listen(5)

        self.clients = []
        self.pseudo = {}
        self.reception_threads = {}  # Dictionnaire pour stocker les threads de réception
        self.shutdown_flag = False
        self.authenticated = False  # Variable pour suivre l'état de l'authentification

        self.server_stop = False
        self.text_server_stop = "Le serveur va s'éteindre."

        self.init_ui()

        self.disconnected_events = {}  # Dictionnaire pour stocker les indicateurs de déconnexion des clients
        self.reception_threads = {}  # Liste pour stocker les threads de réception

        # Thread pour gérer les connexions clients
        connection_thread = threading.Thread(target=self.accept_connections)
        connection_thread.start()

        # Configuration du style
        self.setStyleSheet("""
            QWidget {
                background-color: #000; 
                color: #eb232d; /* Couleur du texte par défaut */
                font-family: monospace;
                font-size : 20px;
            }
            
            QTextEdit, QLineEdit {
                background-color: #3b3c47; 
                color: #fff; 
                border: 1px solid #eb232d; /* Bordure autour des zones de texte */
                padding: 5px; 
            }

            QPushButton {
                border: 5px solid #eb232d;
                border-radius: 8px
                border: 5px solid #eb232d
                padding 1px 5px;
                min-width: 120px;
                min-height: 35px;
                background-color: #eb232d;
                color: #000; 
            }

            QPushButton:hover {
                background-color: #eb232d;
            }
        """)


    def init_ui(self):
        layout = QVBoxLayout()

        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.command_input = QLineEdit(self)
        layout.addWidget(self.command_input)

        self.send_button = QPushButton('Envoyer Commande', self)
        self.send_button.clicked.connect(self.send_command)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.setWindowTitle('Serveur')
        self.show()

    def send_command(self):
    # Fonction qui permet d'envoyer des commandes
        command = self.command_input.text()
        self.process_command(command)

    def accept_connections(self):
    # Fonction qui accpepet les connexions des clients
        while not self.shutdown_flag:
            try:
                client_socket, _ = self.server_socket.accept()
                if not self.shutdown_flag:
                    connection = threading.Thread(target=self.connect_client, args=[client_socket])
                    connection.start()
            except OSError as e:
                # Ajoute une vérification pour s'assurer que le serveur n'est pas en train de s'arrêter
                if not self.shutdown_flag:
                    print(f"Erreur lors de l'acceptation d'une connexion : {e}")

    def connect_client(self, client):
    # Fonction qui connecte les clients au serveur 
        try:
            data = client.recv(1024).decode().split(",")
            username, command = data[0], data[1]
        except ConnectionResetError:
            print("Le client s'est déconnecté.")
            return

        if command == "CONNECT":
            reception = threading.Thread(target=self.get, args=[client])
            self.clients.append(client)
            self.disconnected_events[client] = Event()
            self.reception_threads[client] = reception
            self.pseudo[client] = username
            self.update_client_status(username, 'ON')

            reception.start()
        else:
            print(f"Commande de connexion inconnue : {command}")
        # Les commandes de connexion permettent de définir le status des clients 

    def update_client_status(self, username, status):
    # Fonction qui permet de mettre à jour le status des clients dans la base de données 
        try:
            cursor.execute("UPDATE client SET status=%s WHERE username=%s", (status, username))
            conn.commit()
            print(f"Statut de {username} mis à jour : {status}")
        except mysql.connector.Error as err:
            print(f"Erreur lors de la mise à jour du statut : {err}")

    def get(self, client):
    # Fonction qui permet d'afficher les clients
        while not self.disconnected_events[client].is_set() and not self.shutdown_flag:
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
                if message.startswith("/disconnect"):
                    self.remove_client(client)  # Déconnecte le client ici
                    break
                elif message[:12] == "/\/P$eudo/\/":
                    self.pseudo[client] = message[12:]
                    message = "\n" + self.pseudo[client] + " a rejoint le serveur !\n"
                    self.broadcast(message, client)
                    print(f"{self.pseudo[client]} est connecté !")
                    self.update_text_area_signal.emit(message)
                else:
                    self.process_message(message, client)

        # Supprime le client et fermer la connexion
        self.remove_client(client)

    def process_message(self, message, client):
        # Ajoute le nom d'utilisateur dans le message
        full_message = f"{self.pseudo[client]}: {message}"
        self.broadcast(full_message, sender_client=client)

        # Gére la commande de déconnexion
        if message == '/disconnect':
            self.handle_disconnect(client)
        else:
            # Affiche le message également sur l'interface graphique
            self.update_text_area_signal.emit(full_message)

    def process_command(self, command):
    # Fonction qui permet de gérer les commandes 
        if not self.authenticated:
            self.show_login_dialog()
        elif command == '/kill':
            # Informe tous les clients que le serveur va être arrêté
            self.broadcast("Le serveur va être arrêté. Déconnexion imminente.")
            # Ferme proprement la connexion avec chaque client
            self.disconnect_clients(self.clients)  # Passer tous les clients connectés
            # Ferme le serveur
            self.server_socket.close()
            sys.exit()  # Arrête le script du serveur
        elif command == '/kick':
            kick_dialog = KickUserDialog(self)
            kick_dialog.exec()
        elif command == '/ban':
            ban_dialog = BanUserDialog(self)
            ban_dialog.exec()
        elif command == '/unban':
            unban_dialog = UnbanUserDialog(self)
            unban_dialog.exec()
            
        else:
            print(f"Commande inconnue : {command}")
            self.update_text_area_signal.emit(f"Commande inconnue : {command}")

    def show_login_dialog(self):
    # Permet d'afficher la fenêtre de login
        login_dialog = LoginDialog(self)
        result = login_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # L'authentification réussit
            self.authenticated = True
            print("Authentification réussie.")
        else:
            # L'authentification échoue
            print("Authentification échouée.")

    def broadcast(self, message, sender_client=None):
    # Fonction qui permet d'envoyer des messages à tous les clients 
        for client in self.clients:
            if client != sender_client:
                try:
                    client.send(message.encode())
                except socket.error as e:
                    print(f"Erreur lors de l'envoi du message au client : {e}")

    def remove_client(self, client):
    # Fonction qui permet de supprimer tous les clients 
        if client in self.clients:
            print(f"{self.pseudo[client]} s'est déconnecté.")
            self.update_text_area_signal.emit(f"{self.pseudo[client]} s'est déconnecté.")
            self.update_client_status(self.pseudo[client], 'OFF')  # Mettre à jour le statut à "OFF"
            del self.pseudo[client]
            self.clients.remove(client)
            client.close()
            self.disconnected_events.pop(client, None)  # Supprime l'indicateur pour ce client
            self.reception_threads.pop(client, None)  # Retire le thread de réception
        else:
            print("Erreur : Tentative de suppression d'un client inexistant.")
    
    def disconnect_clients(self, clients):
    # Fonction qui permet de déconnecter les clients 
        self.shutdown_flag = True  # Défini le drapeau d'arrêt

        for client in clients:
            self.disconnected_events[client].set()  # Marque le client comme déconnecté
            # Si le thread de réception existe, attend qu'il se termine
            if client in self.reception_threads:
                self.reception_threads[client].join()

        
        self.reception_threads = {}  # Retire tous les threads de réception

        # Ferme la socket du serveur si elle n'est pas déjà fermée
        try:
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
        except OSError as e:
            print(f"Erreur lors de la fermeture de la socket du serveur : {e}")

    def arret_server(self):
    # Fonction qui permet d'arreter le serveur
        print(self.text_server_stop)
        self.broadcast(self.text_server_stop)
        self.server_stop = True

        # Ferme tous les clients
        self.disconnect_clients(self.clients)

        # Ferme le socket du serveur après avoir déconnecté tous les clients
        self.server_socket.close()

        self.server_shutdown_signal.emit()

    def close_clients(self):
        # Fonction qui permet de fermer la connexion aux clients
        for client in self.clients:
            self.disconnected_events[client].set()

        for client_thread in list(self.reception_threads.values()):
            client_thread.join()

        self.reception_threads = []

        self.server_shutdown_signal.emit()

class KickUserDialog(QDialog):
# Classe qui gère la fenêtre de la commande /Kick
    def __init__(self, server_app, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Supprimer un utilisateur")

        self.server_app = server_app

        self.label_username = QLabel("Choix de l'utilisateur à kick : ")

        self.combo_users = QComboBox(self)
        self.populate_users()
        
        self.btn_kick = QPushButton("Supprimer", self)
        self.btn_kick.clicked.connect(self.kick_user)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_username)
        layout.addWidget(self.combo_users)
        layout.addWidget(self.btn_kick)

        # Configuration du style
        self.setStyleSheet("""
            QWidget {
                background-color: #000; 
                color: #eb232d; /* Couleur du texte par défaut */
                font-family: monospace;
                font-size : 20px;
            }
            
            QTextEdit, QLineEdit {
                background-color: #3b3c47; 
                color: #fff; 
                border: 1px solid #eb232d; /* Bordure autour des zones de texte */
                padding: 5px; 
            }

            QPushButton {
                border: 5px solid #eb232d;
                border-radius: 8px
                border: 5px solid #eb232d
                padding 1px 5px;
                min-width: 120px;
                min-height: 35px;
                background-color: #eb232d;
                color: #000; 
            }

            QPushButton:hover {
                background-color: #eb232d;
            }

        """)
        self.combo_users.setStyleSheet("""
            QComboBox {
                background-color: #000;
                color: #eb232d;
                border: 1px solid #ccc;
                padding: 5px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: right;
                width: 20px;
                border-left: 1px solid #ccc;
            }

            QComboBox::down-arrow {
                color : #fff;
                width: 5px;                        
            }

            QComboBox QAbstractItemView {
                background-color: #000;
                color: #fff;
                border: 1px solid #ccc;
            }

            QComboBox QAbstractItemView::item:selected {
                background-color: #eb232d 15%;  /* Couleur de fond pour l'élément sélectionné */
                color: #eb232d;  /* Couleur du texte pour l'élément sélectionné */
            }
        """)

    def populate_users(self):
        # Obtient la liste des utilisateurs depuis la base de données
        cursor.execute("SELECT username FROM client")
        users = cursor.fetchall()
        # Ajoute les utilisateurs à la liste déroulante
        self.combo_users.addItems([user[0] for user in users])

    def kick_user(self):
        username = self.combo_users.currentText()
        if username:
            self.handle_kick_command(username)
            self.accept()

    def handle_kick_command(self, username):
        try:
            # Exécute la requête SQL pour supprimer l'utilisateur de la base de données
            cursor.execute("DELETE FROM client WHERE username=%s", (username,))
            conn.commit()
            print(f"Utilisateur {username} supprimé de la base de données.")
            kick_message = f"L'utilisateur {username} a été kick."
            self.server_app.broadcast(kick_message)
            self.server_app.update_text_area_signal.emit(f"L'utilisateur {username} a été kick.")

            # Cherche le client dans la liste des clients connectés
            kicked_client = next((client for client, pseudo in self.server_app.pseudo.items() if pseudo == username), None)
            if kicked_client:
                # Si le client est connecté, lui envoyer un message spécial de bannissement
                try:
                    kick_message = f"/\/Kick/\/L'utilisateur {username} a été kick."
                    kicked_client.send(kick_message.encode())
                except socket.error as e:
                    print(f"Erreur lors de l'envoi du message de kick au client : {e}")

        except mysql.connector.Error as err:
            # Gére les erreurs de base de données
            print(f"Erreur lors de la suppression de l'utilisateur : {err}")

class BanUserDialog(QDialog):
# Classe qui gère la fenêtre de la commande /Ban
    def __init__(self, server_app, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bannir un utilisateur")

        self.server_app = server_app

        self.label_username = QLabel("Choix de l'utilisateur à bannir : ")

        self.combo_users = QComboBox(self)
        self.populate_users()

        self.btn_ban = QPushButton("Bannir", self)
        self.btn_ban.clicked.connect(self.ban_user)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_username)
        layout.addWidget(self.combo_users)
        layout.addWidget(self.btn_ban)

        # Configuration du style
        self.setStyleSheet("""
            QWidget {
                background-color: #000; 
                color: #eb232d; /* Couleur du texte par défaut */
                font-family: monospace;
                font-size : 20px;
            }
            
            QTextEdit, QLineEdit {
                background-color: #3b3c47; 
                color: #fff; 
                border: 1px solid #eb232d; /* Bordure autour des zones de texte */
                padding: 5px; 
            }

            QPushButton {
                border: 5px solid #eb232d;
                border-radius: 8px
                border: 5px solid #eb232d
                padding 1px 5px;
                min-width: 120px;
                min-height: 35px;
                background-color: #eb232d;
                color: #000; 
            }

            QPushButton:hover {
                background-color: #eb232d;
            }

        """)
        self.combo_users.setStyleSheet("""
            QComboBox {
                background-color: #000;
                color: #eb232d;
                border: 1px solid #ccc;
                padding: 5px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: right;
                width: 20px;
                border-left: 1px solid #ccc;
            }

            QComboBox::down-arrow {
                color : #fff;
                width: 5px;                        
            }

            QComboBox QAbstractItemView {
                background-color: #000;
                color: #fff;
                border: 1px solid #ccc;
            }

            QComboBox QAbstractItemView::item:selected {
                background-color: #eb232d 15%;  /* Couleur de fond pour l'élément sélectionné */
                color: #eb232d;  /* Couleur du texte pour l'élément sélectionné */
            }
        """)

    def populate_users(self):
        # Obtient la liste des utilisateurs depuis la base de données
        cursor.execute("SELECT username FROM client WHERE banned = 'no'")
        users = cursor.fetchall()
        # Ajoute les utilisateurs à la liste déroulante
        self.combo_users.addItems([user[0] for user in users])

    def ban_user(self):
        username = self.combo_users.currentText()
        if username:
            self.handle_ban_command(username) 
            self.accept()
            
    def handle_ban_command(self, username):
        try:
            # Exécute la requête SQL pour bannir l'utilisateur dans la base de données
            cursor.execute("UPDATE client SET banned='yes' WHERE username=%s", (username,))
            conn.commit()
            print(f"Utilisateur {username} banni.")

            # Envoie un message de bannissement à tous les clients
            ban_message = f"L'utilisateur {username} a été banni."
            self.server_app.broadcast(ban_message)
            self.server_app.update_text_area_signal.emit(ban_message)

            # Cherche le client dans la liste des clients connectés
            banned_client = next((client for client, pseudo in self.server_app.pseudo.items() if pseudo == username), None)
            if banned_client:
                # Si le client est connecté, lui envoyer un message spécial de bannissement
                try:
                    ban_message = f"/\/Ban/\/L'utilisateur {username} a été banni."
                    banned_client.send(ban_message.encode())
                except socket.error as e:
                    print(f"Erreur lors de l'envoi du message de bannissement au client : {e}")

        except mysql.connector.Error as err:
            # Gére les erreurs de base de données
            print(f"Erreur lors du bannissement de l'utilisateur : {err}")

from PyQt6.QtWidgets import QComboBox

class UnbanUserDialog(QDialog):
# Classe qui gère la fenêtre de la commande /unban 
    def __init__(self, server_app, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Débannir un utilisateur")

        self.server_app = server_app 

        self.label_username = QLabel("Choix de l'utilisateur à débannir : ")

        self.combo_users = QComboBox(self)
        self.populate_users()

        self.btn_unban = QPushButton("Débannir", self)
        self.btn_unban.clicked.connect(self.unban_user)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_username)
        layout.addWidget(self.combo_users)
        layout.addWidget(self.btn_unban)

    def populate_users(self):
        # Obtient la liste des utilisateurs bannis depuis la base de données
        cursor.execute("SELECT username FROM client WHERE banned = 'yes'")
        users = cursor.fetchall()
        # Ajoute les utilisateurs à la liste déroulante
        self.combo_users.addItems([user[0] for user in users])

    def unban_user(self):
        username = self.combo_users.currentText()
        if username:
            self.handle_unban_command(username)
            self.accept()

    def handle_unban_command(self, username):
        try:
            # Exécute la requête SQL pour débannir l'utilisateur dans la base de données
            cursor.execute("UPDATE client SET banned='no' WHERE username=%s", (username,))
            conn.commit()
            print(f"Utilisateur {username} débanni.")

            # Envoie un message de débannissement à tous les clients
            unban_message = f"L'utilisateur {username} a été débanni."
            self.server_app.broadcast(unban_message)
            self.server_app.update_text_area_signal.emit(unban_message)

            # Cherche le client dans la liste des clients connectés
            unbanned_client = next((client for client, pseudo in self.server_app.pseudo.items() if pseudo == username), None)
            if unbanned_client:
                # Si le client est connecté, lui envoyer un message spécial de débannissement
                try:
                    unban_message = f"/\/Unban/\/L'utilisateur {username} a été débanni."
                    unbanned_client.send(unban_message.encode())
                except socket.error as e:
                    print(f"Erreur lors de l'envoi du message de débannissement au client : {e}")

        except mysql.connector.Error as err:
            # Gére les erreurs de base de données
            print(f"Erreur lors du débannissement de l'utilisateur : {err}")

class SignalHandler(QObject):
    update_text_area_signal = pyqtSignal(str)
    server_shutdown_signal = pyqtSignal()


def run_server_app():
    app = QApplication(sys.argv)
    server_app = ServerApp()

    signal_handler = SignalHandler()
    signal_handler.update_text_area_signal.connect(server_app.text_area.append)
    signal_handler.server_shutdown_signal.connect(app.quit)  

    server_app.update_text_area_signal = signal_handler.update_text_area_signal
    server_app.server_shutdown_signal = signal_handler.server_shutdown_signal

    sys.exit(app.exec())


if __name__ == '__main__':
    run_server_app()