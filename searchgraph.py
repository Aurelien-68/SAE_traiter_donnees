import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

def main():
    # Crée l'application Qt
    app = QApplication(sys.argv)

    # Ouvre la boîte de dialogue de sélection de répertoire
    directory = QFileDialog.getExistingDirectory(None, "Choisir un répertoire")

    # Si l'utilisateur a sélectionné un dossier et validé
    if directory:
        print(directory)
    else:
        # En cas d'annulation, on renvoie une chaîne vide
        print("")

    sys.exit(0)

if __name__ == "__main__":
    main()
