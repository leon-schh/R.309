import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class Fenetre(QWidget):
    def __init__(self):
        super().__init__()                                      # Appel du constructeur de la classe parente

        # Configuration initiale de la fenêtre
        self.setWindowTitle("Une première Fenêtre")
        self.setGeometry(100, 100, 400, 200)

        # création des Widgets
        self.label_nom = QLabel(" Saisir votre Nom:")
        self.entry_nom = QLineEdit()
        self.bouton_ok = QPushButton("OK")
        self.label_resultat = QLabel("")
        self.bouton_quitter = QPushButton ("Quitter")

        # Layout, permet d'afficher les différents élements 
        layout = QVBoxLayout()
        layout.addWidget(self.label_nom)
        layout.addWidget(self.entry_nom)
        layout.addWidget(self.bouton_ok)
        layout.addWidget(self.label_resultat)
        layout.addWidget(self.bouton_quitter)

        # Connecter les boutons à leur fonction respective
        self.bouton_ok.clicked.connect(self.afficher_message)
        self.bouton_quitter.clicked.connect(self.close)

        # Définir le layout principal
        self.setLayout(layout)

    def afficher_message(self):
        nom = self.entry_nom.text()                   # Récupération du texte saisi dans le champ de saisie
        message = f"Bonjour {nom}"                    # Création du message de salutation
        self.label_resultat.setText(message)          # Affichage du message dans l'étiquette

if __name__ == "__main__":
    app = QApplication(sys.argv)                    # Création de l'application Qt
    fenetre = Fenetre()                             # Création d'une instance de la classe Fenetre
    fenetre.show()                                  # Affichage de la fenêtre
    sys.exit(app.exec())                            # Exécution de la boucle principale de l'application