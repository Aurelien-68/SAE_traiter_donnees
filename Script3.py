import sys
import json
import random
import os
from pathlib import Path

# --- Importation des bibliothèques PyQt ---
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox, QMessageBox, QFileDialog, QMenuBar, QAction
)
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt


# 1) Fonction pour charger la liste des fichiers depuis un fichier JSON

def charger_liste_depuis_json(nom_fichier_json):
    chemin_json = Path(nom_fichier_json)
    if not chemin_json.exists():
        print(f"ERREUR : Le fichier JSON '{nom_fichier_json}' n'existe pas.")
        return []

    # Lecture du fichier JSON
    with open(chemin_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    liste_resultat = []
    # Si les donnees sont dans le format attendu [ [chemin, taille], ... ]
    if data and isinstance(data[0], list): #verifie data n'est pas vide et si le 1er element est une liste
        liste_resultat = data
    # Si les donnees sont dans le format [ {"chemin_complet":..., "taille_octets":...}, ... ]
    elif data and isinstance(data[0], dict):
        for item in data:
            c = item.get("chemin_complet", "")
            t = item.get("taille_octets", 0)
            liste_resultat.append([c, t])
    return liste_resultat


# 2) Fonction pour generer des couleurs aleatoires

def generer_couleurs_aleatoires(nb_maxi_fichiers):
    couleurs = []
    # Generer une couleur aleatoire pour chaque fichier
    for _ in range(nb_maxi_fichiers):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        couleurs.append(QColor(r, g, b))
    return couleurs


# Fenêtre principale de l'application PyQt

class FenetrePrincipale(QMainWindow):
    def __init__(self, repertoire_de_base, liste_fichiers):
        super().__init__()
        self.setWindowTitle("Analyse des gros fichiers")
        self.setGeometry(200, 100, 1000, 600)

        self.repertoire_de_base = repertoire_de_base
        self.liste_fichiers = liste_fichiers  # Liste des fichiers sous forme [ [chemin, taille], ... ]

        # Calcul du nombre de couleurs necessaires
        NB_MAXI_FICHIERS = max(len(self.liste_fichiers), 100)
        self.couleurs = generer_couleurs_aleatoires(NB_MAXI_FICHIERS)

        # Ensemble (set) pour memoriser les fichiers selectionnes par l'utilisateur.
        # Cela garantit que chaque fichier n'est ajoute qu'une seule fois, même si l'utilisateur coche plusieurs fois la même case.
        # Un set permet aussi de verifier rapidement si un fichier est selectionne, ce qui est utile pour d'autres operations comme la generation du script PowerShell.
        self.selected_files = set()

        # Creation de l'interface graphique
        self.create_menus()      # Menu (Fichier, Aide)
        self.init_ui()           # Contenu de la fenêtre
        self.create_status_bar() # Barre de statut

    def create_menus(self):
        """
        Cree la barre de menus avec les options "Fichier" et "Aide".
        """
        menu_bar = self.menuBar()

        # Menu "Fichier"
        menu_fichier = menu_bar.addMenu("Fichier")
        action_quitter = QAction("Quitter", self)
        action_quitter.triggered.connect(self.close)
        menu_fichier.addAction(action_quitter)



    def create_status_bar(self):

        #Cree la barre de statut avec le nombre de fichiers charges

        nb = len(self.liste_fichiers)
        self.statusBar().showMessage(f"Fichiers charges : {nb}")

    def init_ui(self):
        # Application d'une feuille de style (CSS)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8F8F8;
            }
            QTabWidget::pane {
                border: 1px solid #A0A0A0;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background: #D0D0D0;
                color: #333;
                padding: 8px 14px;
                margin: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                font-weight: bold;
                color: #0078D7;
            }
            QCheckBox {
                font-size: 14px;
                padding: 4px;
            }
            QPushButton {
                background-color: #0078D7;
                color: #FFF;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
        """)

        # Creation d'un QTabWidget central
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Ajout des differents onglets
        self.add_tab_camembert()
        self.add_tabs_legendes()
        self.add_tab_ihm()


    # Onglet "Camembert" pour afficher la repartition des fichiers

    def add_tab_camembert(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Creation d'un camembert avec les donnees des fichiers
        series = QPieSeries()
        total_size = sum(t for _, t in self.liste_fichiers)

        for i, (chemin, taille) in enumerate(self.liste_fichiers):
            label = Path(chemin).name
            slice_ = series.append(label, taille)

            # Attribution d'une couleur
            if i < len(self.couleurs):
                slice_.setColor(self.couleurs[i])

            # Affichage du pourcentage si > 5%
            pct = (taille / total_size * 100) if total_size else 0
            if pct > 5:
                slice_.setLabelVisible(True)
                slice_.setLabel(f"{label} ({pct:.1f}%)")

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Repartition des fichiers par taille (Camembert)")

        # Personnalisation de la police du titre
        font_titre = QFont("Arial", 12, QFont.Bold)
        chart.setTitleFont(font_titre)

        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setFont(QFont("Arial", 10))

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chart_view)
        self.tabs.addTab(tab, "Camembert")


    # Onglets pour afficher les legendes des fichiers (25 par onglet)

    def add_tabs_legendes(self):
        nb_par_onglet = 25
        for i in range(0, len(self.liste_fichiers), nb_par_onglet):
            subset = self.liste_fichiers[i : i + nb_par_onglet]

            tab = QWidget()
            layout = QVBoxLayout(tab)
            layout.setSpacing(8)

            for (chemin, taille) in subset:
                cb = QCheckBox(f"{chemin} ({taille} octets)")
                cb.stateChanged.connect(lambda state, f=chemin: self.toggle_file_selection(state, f))
                layout.addWidget(cb)

            self.tabs.addTab(tab, f"Legendes {int(i/nb_par_onglet) + 1}")

    def toggle_file_selection(self, state, file_path):
        """
        Ajoute ou retire un fichier de la selection en fonction de son etat.
        """
        if state == Qt.Checked:
            self.selected_files.add(file_path)
        else:
            self.selected_files.discard(file_path)


    # Onglet pour generer un script PowerShell

    def add_tab_ihm(self):
        # Cree un nouvel onglet avec un bouton permettant de generer un script PowerShell
        tab = QWidget()  # Conteneur pour l'onglet
        layout = QVBoxLayout(tab)  # Mise en page verticale pour organiser les widgets
        layout.setSpacing(10)  # Espacement entre les elements du layout

        # Creation du bouton
        btn = QPushButton("Generer script PowerShell")
        # Connexion du clic du bouton à la methode de generation du script
        btn.clicked.connect(self.callback_generer_script_ps1)

        # Ajout du bouton au layout de l'onglet
        layout.addWidget(btn)

        # Applique le layout au widget (onglet)
        tab.setLayout(layout)

        # Ajoute l'onglet avec le titre "IHM" au widget d'onglets
        self.tabs.addTab(tab, "IHM")

    def callback_generer_script_ps1(self):
        """
        Genère un script PowerShell pour supprimer les fichiers selectionnes.
        """
        if not self.selected_files:
            QMessageBox.warning(self, "Avertissement", "Aucun fichier selectionne !")
            return

        default_name = str(Path(__file__).parent.joinpath("supprime_fichiers.ps1"))
        ps1_path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le script PowerShell",
            default_name,
            "Fichier PowerShell (*.ps1)"
        )
        if not ps1_path:
            return  # Annule

        # Contenu du script PowerShell pour supprimer les fichiers
        script_content = '''Write-Output "Script PowerShell pour supprimer des fichiers sans confirmation"
Write-Output "Attention : cette suppression est definitivement ..."
$reponse = Read-Host "Veuillez confirmer la suppression de tous ces fichiers : (OUI)"
if ($reponse -eq "OUI") {
    $confirmation = Read-Host "Etes-vous bien certain(e) ? (OUI)"
    if ($confirmation -eq "OUI") {
'''
        for fpath in self.selected_files:
            safe_path = fpath.replace('"', '`"')
            script_content += f'        Remove-Item -Path "{safe_path}" -Force\n'

        script_content += '''    } else {
        Write-Output "Operation annulee..."
    }
} else {
    Write-Output "Operation annulee..."
}
'''

        try:
            with open(ps1_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            QMessageBox.information(self, "Succes", f"Script PowerShell genere :\n{ps1_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de creer le script:\n{e}")


# Programme principal

def main():
    # 1) Definir un repertoire de base
    repertoire_de_base = r"C:\Mon\Repertoire\De\Base" # r signifie raw string(interprete pas caractères spéciaux)

    # 2) Nom du fichier JSON
    nom_fichier_json = "fichiers_gros.json"

    # 3) Lecture du fichier JSON
    liste_fichiers = charger_liste_depuis_json(nom_fichier_json)

    # 4) Creation de l'application PyQt
    app = QApplication(sys.argv)

    # 5) Creation de la fenêtre principale
    fenetre = FenetrePrincipale(repertoire_de_base, liste_fichiers)
    fenetre.show()

    # 6) Lancer la boucle d'evenements PyQt
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()