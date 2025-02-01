import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

def main():
    # Cree l'application Qt. Cette ligne est indispensable pour demarrer l'interface graphique PyQt.

    app = QApplication(sys.argv)

    # Ouvre une fenêtre de selection de repertoire
    directory = QFileDialog.getExistingDirectory(None, "Choisir un repertoire")

    # Si un repertoire a ete selectionne
    if directory:
        print(directory)
    else:
        # Si l'utilisateur annule, on affiche une chaîne vide
        print("")

    # Quitte l'application après la selection
    sys.exit(0)

if __name__ == "__main__":
    main()