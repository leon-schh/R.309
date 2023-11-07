try:
    nom = "test .txt" 

    with open(nom, 'r') as fichier:
        contenu = fichier.read()
        print(contenu)

except FileNotFoundError:
    print("Le fichier spécifié n'a pas été trouvé.")
except IOError:
    print("Une erreur s'est produite lors de la lecture du fichier.")
except FileExistsError:
    print("Ce fichier existe dejà")
except PermissionError:
    print ("Vous n'avez pas les droits d'ouvrir ce fichier")


