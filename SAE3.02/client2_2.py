import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QDialog, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPalette, QColor
import socket
import mysql.connector
conn = mysql.connector.connect(host="localhost", user = "root", password="root", database="serveur")
cursor = conn.cursor()

text_server_stop = "Le serveur va s'éteindre."

class CreateAccountWindow(QDialog):
# Classe qui gère la fenêtre de la création de compte
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.init_ui()

        # Configuration du style
        self.setStyleSheet("""
            QWidget {
                background-color: #000; 
                color: #1527ed; /* Couleur du texte par défaut */
                font-family: monospace;
                font-size : 20px;
            }
            
            QTextEdit, QLineEdit {
                background-color: #3b3c47; 
                color: #fff; 
                border: 1px solid #1527ed; /* Bordure autour des zones de texte */
                padding: 5px; 
            }

            QPushButton {
                border: 5px solid #1527ed;
                border-radius: 8px
                border: 5px solid #1527ed
                padding 1px 5px;
                min-width: 120px;
                min-height: 35px;
                background-color: #1527ed;
                color: #000; 
            }

            QPushButton:hover {
                background-color: #1527ED;
            }
        """)


    def init_ui(self):
    # Fonction qui paramètre l'interface graphique
        self.setWindowTitle('Créer un compte')

        self.label_username = QLabel('Nom d\'utilisateur:')
        self.edit_username = QLineEdit(self)

        self.label_password = QLabel('Mot de passe:')
        self.edit_password = QLineEdit(self)
        self.edit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_create_account = QPushButton('Créer le compte', self)
        self.btn_create_account.clicked.connect(self.create_account)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_username)
        layout.addWidget(self.edit_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.edit_password)
        layout.addWidget(self.btn_create_account)

    def create_account(self):
    #Fonction qui gère la création de compte 
        # Obtenir le nom d'utilisateur et le mot de passe des champs d'entrée
        username = self.edit_username.text()
        password = self.edit_password.text()

        # Obtenir l'adresse IP du client
        ip_address = socket.gethostbyname(socket.gethostname())

        # Exécute une requête SQL pour insérer les informations dans la table client
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO client (username, passwd, IP, banned) VALUES (%s, %s,%s, %s)", (username, password,ip_address, "no"))
            self.db_connection.commit()
            cursor.close()
            self.accept()  # Fermez la fenêtre de création de compte après la création du compte
        except mysql.connector.Error as err:
            # Gére les erreurs de base de données
            print(f"Erreur lors de la création du compte : {err}")
            # Affiche un message d'erreur ou autre logique en cas d'échec
            self.show_error_message("Erreur lors de la création du compte : Nom d'utilisateur déja pris. Veuillez en choisir un autre.")
    
    def show_error_message(self, message):
    # Fonction qui permet d'afficher une fenêtre d'erreur 
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Erreur")
        error_dialog.setText(message)
        error_dialog.exec()

class LoginWindow(QDialog):
# Classe qui gère la fnenêtre d'authentification 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connexion au Serveur")

        client_app = ClientApp
        self.label_username = QLabel("Identifiant:")
        self.edit_username = QLineEdit(self)

        self.label_password = QLabel("Mot de passe:")
        self.edit_password = QLineEdit(self)
        self.edit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.submit_button = QPushButton("Se Connecter")
        self.submit_button.clicked.connect(self.submit_login)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_username)
        layout.addWidget(self.edit_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.edit_password)
        layout.addWidget(self.submit_button)

        # Ajoute un bouton pour créer un compte
        self.btn_create_account = QPushButton('Créer un compte', self)
        self.btn_create_account.clicked.connect(self.show_create_account_window)
        layout.addWidget(self.btn_create_account)

        # Configuration du style
        self.setStyleSheet("""
            QWidget {
                background-color: #000; 
                color: #1527ed; /* Couleur du texte par défaut */
                font-family: monospace;
                font-size : 20px;
            }
            
            QTextEdit, QLineEdit {
                background-color: #3b3c47; 
                color: #fff; 
                border: 1px solid #1527ed; /* Bordure autour des zones de texte */
                padding: 5px; 
            }

            QPushButton {
                border: 5px solid #1527ed;
                border-radius: 8px
                border: 5px solid #1527ed
                padding 1px 5px;
                min-width: 120px;
                min-height: 35px;
                background-color: #1527ed;
                color: #000; 
            }

            QPushButton:hover {
                background-color: #1527ED;
            }
        """)

    def show_create_account_window(self):
    # fonction qui permet d'afficher la fenêtre de création de compte 
        create_account_window = CreateAccountWindow(self.parent().db_connection)
        if create_account_window.exec():
            # Si la fenêtre de création de compte est acceptée, récupérez les informations ici
            username = create_account_window.edit_username.text()
            password = create_account_window.edit_password.text()

    def submit_login(self):
    # Fonction qui permet de renseigner les logins
        username = self.edit_username.text()
        password = self.edit_password.text()

        # Vérifie les informations dans la base de données
        if self.check_login_credentials(username, password):
            self.accept()
            

        else:
            # Affiche un message d'erreur ou autre logique en cas d'échec
            print("Identifiant ou mot de passe incorrect.")
        

    def check_login_credentials(self, username, password):
    #  Fonction qui vérifie les logins dans le base de données
        try:
            # Exécute une requête SQL pour vérifier les informations de connexion
            cursor.execute("SELECT * FROM client WHERE username=%s AND passwd=%s", (username, password))
            result = cursor.fetchone()

            if result:
                # Vérifie si l'utilisateur est banni
                if result[2] == 'yes':
                    self.show_error_message("Vous êtes banni.")
                    return False
                # L'utilisateur n'est pas banni
                else :
                    return True
            else:
                if result[2] == 'yes':
                    error_message = "Utilisateur banni."
                    return False
                else :
                    # Les informations de connexion sont incorrectes
                    error_message = "Identifiant ou mot de passe incorrect."
                    self.show_error_message(error_message)
                    return False
        except mysql.connector.Error as err:
            # Gére les erreurs de base de données
            print(f"Erreur de base de données: {err}")
            return False

    def show_error_message(self, message):
    # Fonction qui permet d'afficher une fenêtre d'erreur 
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Erreur")
        error_dialog.setText(message)
        error_dialog.exec()

class ClientApp(QWidget):
# Classe qui gère la fenêtre du client 
    message_sent = pyqtSignal(str)
    ban_received = pyqtSignal()
    kick_received = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ban_dialog = None
        self.connection_status = False

        self.db_connection = mysql.connector.connect(host="localhost", user="root", password="root", database="serveur")

        self.login_window = LoginWindow(self)
        if not self.login_window.exec():
            sys.exit()  # Fermez l'application si la connexion échoue

        self.server_ip = '127.0.0.1'
        self.server_port = 6969
        self.username = ""
        self.client_socket = None
        self.init_ui()
        
        # Configuration du style
        self.setStyleSheet("""
            QWidget {
                background-color: #000; 
                color: #1527ed; /* Couleur du texte par défaut */
                font-family: monospace;
                font-size : 20px;
            }
            
            QTextEdit, QLineEdit {
                background-color: #3b3c47; 
                color: #fff; 
                border: 1px solid #1527ed; /* Bordure autour des zones de texte */
                padding: 5px; 
            }

            QPushButton {
                border: 5px solid #1527ed;
                border-radius: 8px
                border: 5px solid #1527ed
                padding 1px 5px;
                min-width: 120px;
                min-height: 35px;
                background-color: #1527ed;
                color: #000; 
            }

            QPushButton:hover {
                background-color: #1527ED;
            }
        """)

    def init_ui(self):
        self.setWindowTitle('Client de Messagerie')

        self.btn_connect = QPushButton('Se Connecter')
        self.btn_connect.clicked.connect(self.connect_to_server)

        self.label_chat = QLabel('Chat:')
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)

        self.label_message = QLabel('Message:')
        self.edit_message = QLineEdit(self)
        self.btn_send = QPushButton('Envoyer')
        self.btn_send.clicked.connect(self.send_message)
        self.message_sent.connect(self.update_chat_display)

        # Layouts
        v_layout = QVBoxLayout(self)

        v_layout.addWidget(self.btn_connect)

        v_layout.addWidget(self.label_chat)
        v_layout.addWidget(self.chat_display)

        v_layout.addWidget(self.label_message)
        v_layout.addWidget(self.edit_message)
        v_layout.addWidget(self.btn_send)

        self.setLayout(v_layout)

    def connect_to_server(self):
    # Fonction qui permet la connexion du client au serveur 
        self.username = self.login_window.edit_username.text()  # Met à jour le pseudonyme avec la valeur du champ d'entrée

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            command = "CONNECT"
            self.client_socket.send(f"{self.username},{command}".encode())
        except socket.error:
            self.chat_display.append(f"Erreur 404, Serveur Hors-ligne")
            return

        self.chat_display.append(f"Connecté au serveur en tant que {self.username}")

        self.connection_status = True
        self.btn_connect.hide()
        self.receive_thread = ReceiveThread(self.client_socket)
        # Lie les différents messages envoyé du serveur à sa fonction
        self.receive_thread.message_received.connect(self.update_chat_display)
        self.receive_thread.kill_received.connect(self.handle_kill_received)
        self.receive_thread.kick_received.connect(self.handle_kick_received)
        self.receive_thread.ban_received.connect(self.handle_ban_received)
        self.receive_thread.start()

        # Envoi du nom d'utilisateur au serveur
        self.client_socket.send(f"/\/P$eudo/\/{self.username}".encode('utf-8'))

    def send_message(self):
    # Fonction qui permet d'envoyer des messages 
        if self.client_socket:
            try:
                message = self.edit_message.text()
                if message == '/disconnect':
                    self.message_sent.emit (f"{message} : Commande inconnue.")
                    self.edit_message.clear()
                else:
                    self.client_socket.send(message.encode('utf-8'))
                    self.edit_message.clear()
            except OSError:
                print ("Erreur 404, Serveur Hors-ligne")
                self.chat_display.append("Erreur 404, Serveur Hors-ligne")

            # Émet le signal uniquement si le message ne provient pas du serveur
            if not message.startswith(text_server_stop):
                if message != '/disconnect':
                    self.message_sent.emit(f"{self.username}: {message}")

    def send_disconnect_command(self):
    # Permet d'envoyer une commande de déconnexion, qui signale au serveur que le client se déconnecte 
        if self.client_socket:
            disconnect_command = '/disconnect'
            command = "DISCONNECT"
            self.client_socket.send(command.encode())
            self.client_socket.send(disconnect_command.encode('utf-8'))
            self.client_socket.close()  # Close the client socket
    
    def handle_server_shutdown(self):
    # Fonction qui gère la fermeture du serveur 
        self.client_socket.close()
        self.chat_display.append(text_server_stop)

    def update_chat_display(self, message):
    # Fonction qui met à jour la fenêtre de chat
        self.chat_display.append(message)

    def show_create_account_window(self):
    # Fonction qui affiche les utilisateurs crées 
        create_account_window = CreateAccountWindow(self.db_connection)
        create_account_window.exec()

    def disconnect_on_close(self):
        # Envoie une commande de déconnexion au serveur
        self.send_disconnect_command()
        # Ferme la connexion
        self.client_socket.close()

    def handle_kill_received(self):
        # Affiche un message d'erreur sur l'interface utilisateur
        error_message = "Le serveur va s'éteindre. Vous allez être déconnecté."
        self.show_error_message(error_message)
        # Ferme la connexion et l'application
        self.disconnect_on_close()
        
        # Ferme la fenêtre du client
        self.close()

    def handle_kick_received(self):
    # Fonction qui gère le kick par le serveur 
        print("Vous avez été kick par l'administrateur.")
        
        # Affiche un message d'erreur sur l'interface utilisateur
        error_message = "Vous avez été kick par l'administrateur. La connexion sera fermée."
        self.show_error_message(error_message)

        # Ferme la connexion et l'application
        self.disconnect_on_close()
        
        # Ferme la fenêtre du client
        self.close()

    def handle_kick_message(self):
    # Fonction qui gère le message de kick envoyé par le serveur 
        print("Vous avez été kick par l'administrateur.")
        # Émettez un signal pour informer l'interface utilisateur du bannissement
        self.kick_received.emit()

    def handle_ban_received(self):
    # Fonction qui gère le banissement du client 
        print("Vous avez été banni par l'administrateur.")
        
        # Afficher un message d'erreur sur l'interface utilisateur
        error_message = "Vous avez été banni par l'administrateur. La connexion sera fermée."
        self.show_error_message(error_message)

        # Fermer la connexion et l'application
        self.disconnect_on_close()
        
        # Fermer la fenêtre du client
        self.close()

    def handle_ban_message(self):
    # Fonction qui gère le message de ban reçu par le serveur 
        print("Vous avez été banni par l'administrateur.")
        # Émettez un signal pour informer l'interface utilisateur du bannissement
        self.ban_received.emit()

    def show_error_message(self, message):
    # Fonctio qui permet d'afficher une fenêtre d'erreur 
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Erreur")
        error_dialog.setText(message)
        error_dialog.exec()

class ReceiveThread(QThread):
    message_received = pyqtSignal(str)
    ban_received = pyqtSignal()
    kick_received = pyqtSignal()
    kill_received = pyqtSignal()

    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.client_app = client_app

    def run(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == text_server_stop:
                    self.handle_server_shutdown()
                    break
                elif "/\/Ban/\/" in message:
                    self.ban_received.emit()
                elif "/\/Kick/\/" in message:
                    self.kick_received.emit()  #
                elif "Le serveur va être arrêté. Déconnexion imminente." in message:
                    self.kill_received.emit()
                else:
                    self.message_received.emit(message)
            except socket.error as e:
                print(f"Erreur de réception : {e}")
                break
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_app = ClientApp()
    app.setStyle("Fusion")
    client_app.show()
    sys.exit(app.exec())