import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

def main():
    # Crée l'application Qt
    app = QApplication(sys.argv)

    # Ouvre une fenêtre de sélection de répertoire
    directory = QFileDialog.getExistingDirectory(None, "Choisir un répertoire")

    # Si un répertoire a été sélectionné
    if directory:
        print(directory)
    else:
        # Si l'utilisateur annule, on affiche une chaîne vide
        print("")

    # Quitte l'application après la sélection
    sys.exit(0)

if __name__ == "__main__":
    main()