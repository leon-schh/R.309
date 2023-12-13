import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import socket
text_server_stop = "Le serveur va s'éteindre."

class ClientApp(QWidget):
    message_sent = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.server_ip = '127.0.0.1'
        self.server_port = 6969
        self.username = ""
        self.client_socket = None
        self.init_ui()
        

    def init_ui(self):
        self.setWindowTitle('Client de Messagerie')

        self.label_username = QLabel('Nom d\'utilisateur:')
        self.edit_username = QLineEdit(self)
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
        v_layout.addWidget(self.label_username)
        v_layout.addWidget(self.edit_username)
        v_layout.addWidget(self.btn_connect)

        v_layout.addWidget(self.label_chat)
        v_layout.addWidget(self.chat_display)

        v_layout.addWidget(self.label_message)
        v_layout.addWidget(self.edit_message)
        v_layout.addWidget(self.btn_send)

        self.setLayout(v_layout)

    def connect_to_server(self):
        self.username = self.edit_username.text()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
        except socket.error as e:
            self.chat_display.append(f"Erreur de connexion au serveur : {e}")
            return

        self.chat_display.append(f"Connecté au serveur en tant que {self.username}")

        self.receive_thread = ReceiveThread(self.client_socket)
        self.receive_thread.message_received.connect(self.update_chat_display)
        self.receive_thread.start()

        # Envoi du nom d'utilisateur au serveur
        self.client_socket.send(f"/\/P$eudo/\/{self.username}".encode('utf-8'))

    def send_message(self):
        if self.client_socket:
            message = self.edit_message.text()
            self.client_socket.send(message.encode('utf-8'))
            self.edit_message.clear()

            # Émettre le signal uniquement si le message ne provient pas du serveur
            if not message.startswith(text_server_stop):
                self.message_sent.emit(f"{self.username}: {message}")

            

    def update_chat_display(self, message):
        self.chat_display.append(message)

    def send_message(self):
        global message_sent
        if self.client_socket:
            message = self.edit_message.text()
            self.client_socket.send(message.encode('utf-8'))
            self.edit_message.clear()

            # Émettre le signal pour indiquer que le message a été envoyé
            self.message_sent.emit(f"{self.username}: {message}")


class ReceiveThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket

    def run(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                # Vérifiez si le message provient du serveur ou du client
                if message != text_server_stop:
                    self.message_received.emit(message)
            except socket.error as e:
                print(f"Erreur de réception : {e}")
                break



if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_app = ClientApp()

    client_app.show()
    sys.exit(app.exec())