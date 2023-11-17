import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QGridLayout

class Fenetre(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculateur de Température")
        self.setGeometry(100, 100, 400, 200)

        # Widgets
        self.label_temperature = QLabel("Température:")
        self.entry_temperature = QLineEdit()
        self.label_unite = QLabel ("K")
        self.label_unite2 = QLabel ("°C")
        self.label_resultat = QLabel("Résultat:")
        self.resultat = QLineEdit()
        self.resultat.setReadOnly(True)
        self.combo_operation = QComboBox()
        self.combo_operation.addItems(["K -> °C", "°C -> K"])
        self.bouton_calculer = QPushButton("Calculer")
        self.bouton_aide = QPushButton("?")

        # Connecter le signal currentIndexChanged à la fonction update_label
        self.combo_operation.currentIndexChanged.connect(self.update_label)

        # Layouts : ils affichent les différents widgets 
        layout_principal = QGridLayout()

        layout_principal.addWidget(self.label_temperature, 0 , 0)
        layout_principal.addWidget(self.entry_temperature, 0, 1)
        layout_principal.addWidget(self.label_unite, 0, 2)

        
        layout_principal.addWidget(self.combo_operation, 1, 0)
        layout_principal.addWidget(self.bouton_calculer, 1, 1)
        layout_principal.addWidget(self.bouton_aide, 1, 2)
        

        layout_principal.addWidget(self.label_resultat, 2, 0)
        layout_principal.addWidget(self.resultat, 2, 1)
        layout_principal.addWidget(self.label_unite2, 2, 2)

        # Connexion du signal "clicked" du bouton Calculer à la fonction effectuer_calcul
        self.bouton_calculer.clicked.connect(self.effectuer_calcul)

        # Connexion du signal "clicked" du bouton Aide à la fonction afficher_aide
        self.bouton_aide.clicked.connect(self.afficher_aide)

        # Définition du layout principal de la fenêtre
        self.setLayout(layout_principal)

    # Fonction qui permet de changer K en °C en fonction de la conversion choisie 
    def update_label(self):
        selected_option = self.combo_operation.currentText()

        if "K -> °C" in selected_option:
            self.label_unite.setText("K")
            self.label_unite2.setText("°C")
        elif "°C -> K" in selected_option:
            self.label_unite.setText("°C")
            self.label_unite2.setText("K")
        
    def effectuer_calcul(self):
        temperature_text = self.entry_temperature.text()
        
        if temperature_text:
            try:
                temperature = float(temperature_text)

                # Vérifier si la température est valide
                if "K -> °C" in self.combo_operation.currentText() and temperature < 0:
                    raise ValueError("La température en Kelvin ne peut pas être inférieure à 0 K.")
                elif "°C -> K" in self.combo_operation.currentText() and temperature < -273.15:
                    raise ValueError("La température en Celsius ne peut pas être inférieure à -273.15 °C.")

                # Récupération de l'opération choisie
                operation_text = self.combo_operation.currentText()

                if "K -> °C" in operation_text:
                    resultat = temperature - 273.15 
                elif "°C -> K" in operation_text:
                    resultat = temperature + 273.15
                else:
                    resultat = temperature
            

                self.resultat.setText(f" {resultat:.2f}")
            except ValueError as e:
                if "could not convert string to float" in str(e):
                    QMessageBox.critical(self, "Erreur de saisie", "Veuillez entrer une valeur numérique valide pour la température.")
                else:
                    QMessageBox.critical(self, "Valeur inférieure au zéro absolue.", str(e))
        else:
            self.resultat.setText("Entrez une valeur avant de calculer.")
    def afficher_aide(self):
        # Fonction qui affiche un message d'aide
        message_aide = "Bienvenue dans le Calculateur de Température!\n\n" \
                       "1. Entrez la température dans la zone de texte.\n" \
                       "2. Choisissez l'opération de conversion dans la liste déroulante.\n" \
                       "3. Cliquez sur le bouton 'Convertir' pour afficher le résultat.\n" \
                       "4. Utilisez le bouton 'Aide' pour afficher ce message d'aide."
        QMessageBox.information(self, "Aide", message_aide) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    fenetre.show()
    sys.exit(app.exec())