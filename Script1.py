import os
import json
import datetime
import sys
import platform
from pathlib import Path


def construire_liste_fichiers(repertoire_de_base):
    fichiers = []
    repertoire = Path(repertoire_de_base)
    for fichier in repertoire.rglob('*'):
        if fichier.is_file():
            infos_stat = fichier.stat()
            date_modif = datetime.datetime.fromtimestamp(infos_stat.st_mtime)
            fichiers.append({
                "Nom du fichier": fichier.name,
                "chemin_complet": str(fichier.resolve()),
                "taille_octets": infos_stat.st_size,
                "derniere_modification": date_modif.strftime('%Y-%m-%d %H:%M:%S')
            })
    return fichiers

def trier_par_taille_desc(liste_fichiers):
    return sorted(liste_fichiers, key=lambda x: x["taille_octets"], reverse=True)

def filtrer_fichiers(liste_fichiers, taille_mini_mo, nb_max_fichiers):
    taille_mini_octets = taille_mini_mo * 1024 * 1024
    fichiers_filtres = [f for f in liste_fichiers if f["taille_octets"] >= taille_mini_octets]
    return fichiers_filtres[:nb_max_fichiers]

def exporter_en_json(liste_fichiers, nom_fichier_json):
    dossier_sortie = Path(nom_fichier_json).parent
    if not dossier_sortie.exists():
        dossier_sortie.mkdir(parents=True, exist_ok=True)

    for f in liste_fichiers:
        # Échapper les antislashs (pour JSON/Windows)
        f["chemin_complet"] = f["chemin_complet"].replace('\\', '\\\\')

    with open(nom_fichier_json, 'w', encoding='utf-8') as fichier_json:
        json.dump(liste_fichiers, fichier_json, indent=4, ensure_ascii=False)

def main():
    # Efface la console PowerShell pour un affichage plus propre (Windows)
    # Si vous voulez être multiplateforme, décommentez la condition:
    # if platform.system() == "Windows":
    os.system("cls")

    # 2) Récupération du répertoire (argument ou input)
    if len(sys.argv) > 1:
        repertoire_de_base = sys.argv[1]
        print(f"[INFO] Répertoire à analyser (fourni en argument) : {repertoire_de_base}\n")
    else:
        repertoire_de_base = input("-> Entrez le chemin du répertoire à analyser : ").strip()

    if not repertoire_de_base or not Path(repertoire_de_base).exists():
        print("\n[ERREUR] Le répertoire spécifié est invalide ou introuvable.")
        return

    print("\n========== Paramètres d'analyse ==========\n")

    # 3) Saisie de la taille minimale (Mo)
    try:
        taille_mini_mo = float(input("-> Taille minimale des fichiers en Mo (ex: 10) : ").strip())
    except ValueError:
        taille_mini_mo = 10.0
        print("[INFO] Valeur incorrecte, utilisation de 10 Mo par défaut.")

    # 4) Saisie du nb max
    try:
        nb_max_fichiers = int(input("-> Nombre maximum de fichiers à conserver (ex: 100) : ").strip())
    except ValueError:
        nb_max_fichiers = 100
        print("[INFO] Valeur incorrecte, utilisation de 100 par défaut.")

    print("\n========== Début de l'analyse ==========\n")

    # 5) Construction de la liste de tous les fichiers
    fichiers = construire_liste_fichiers(repertoire_de_base)
    print(f"=> Nombre total de fichiers trouvés : {len(fichiers)}")

    # 6) Tri par taille décroissante
    fichiers_tries = trier_par_taille_desc(fichiers)

    # 7) Filtrage
    fichiers_filtres = filtrer_fichiers(fichiers_tries, taille_mini_mo, nb_max_fichiers)
    print(f"=> Nombre de fichiers après filtrage : {len(fichiers_filtres)}")

    if not fichiers_filtres:
        print("! Aucun fichier ne correspond aux critères de filtrage.\n")

    # 8) Création du JSON dans le même dossier que le script
    dossier_script = Path(__file__).resolve().parent
    nom_fichier_json = dossier_script.joinpath("fichiers_gros.json")

    exporter_en_json(fichiers_filtres, str(nom_fichier_json))
    print(f"\n[OK] Fichier JSON généré ici : {nom_fichier_json.resolve()}")

    # 9) Aperçu (jusqu'à 5 fichiers)
    if fichiers_filtres:
        print("\n========== Aperçu des premiers fichiers retenus ==========")
        for f in fichiers_filtres[:5]:
            print(f"  - {f['chemin_complet']} (taille : {f['taille_octets']} octets)")

    print("\n========== Fin de l'analyse ==========\n")

if __name__ == "__main__":
    main()
