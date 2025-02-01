import os
import json
import datetime
import sys
import platform
from pathlib import Path


def construire_liste_fichiers(repertoire_de_base):
    fichiers = []
    repertoire = Path(repertoire_de_base)
    # Recherche tous les fichiers dans le repertoire et ses sous-repertoires
    for fichier in repertoire.rglob('*'): # recherche tout dans le dossier et ses cous dossiers ('*' signifie "tout")
        if fichier.is_file():
            infos_stat = fichier.stat()
            date_modif = datetime.datetime.fromtimestamp(infos_stat.st_mtime)
            fichiers.append({
                "Nom du fichier": fichier.name,
                "chemin_complet": str(fichier.resolve()),  # chemin complet du fichier
                "taille_octets": infos_stat.st_size,  # taille du fichier en octets
                "derniere_modification": date_modif.strftime('%Y-%m-%d %H:%M:%S')  # date de dernière modification
            })
    return fichiers

def trier_par_taille_desc(liste_fichiers):
    # Trie les fichiers par taille decroissante
    return sorted(liste_fichiers, key=lambda x: x["taille_octets"], reverse=True)

def filtrer_fichiers(liste_fichiers, taille_mini_mo, nb_max_fichiers):
    # Filtre les fichiers en fonction de la taille minimale et du nombre maximum
    taille_mini_octets = taille_mini_mo * 1024 * 1024  # Convertir Mo en octets
    fichiers_filtres = [f for f in liste_fichiers if f["taille_octets"] >= taille_mini_octets]
    return fichiers_filtres[:nb_max_fichiers]  # Limite à "nb_max_fichiers" fichiers

def exporter_en_json(liste_fichiers, nom_fichier_json):
    # Cree un fichier JSON avec la liste des fichiers filtres
    dossier_sortie = Path(nom_fichier_json).parent
    if not dossier_sortie.exists():
        dossier_sortie.mkdir(parents=True, exist_ok=True)  # Cree le dossier s'il n'existe pas

    for f in liste_fichiers:
        # echappe les antislashs pour le format JSON (sur Windows)
        f["chemin_complet"] = f["chemin_complet"].replace('\\', '\\\\')

    # Sauvegarde la liste dans un fichier JSON
    with open(nom_fichier_json, 'w', encoding='utf-8') as fichier_json:
        json.dump(liste_fichiers, fichier_json, indent=4, ensure_ascii=False)

def main():
    # Efface l'ecran dans PowerShell (Windows) pour un affichage plus propre
    os.system("cls")

    # Recupère le repertoire à analyser (soit en argument, soit par input utilisateur)
    if len(sys.argv) > 1:
        repertoire_de_base = sys.argv[1]
        print(f"[INFO] Repertoire à analyser : {repertoire_de_base}\n")
    else:
        repertoire_de_base = input("-> Entrez le chemin du repertoire à analyser : ").strip()

    if not repertoire_de_base or not Path(repertoire_de_base).exists():
        print("\n[ERREUR] Le repertoire est invalide ou introuvable.")
        return

    print("\n========== Paramètres d'analyse ==========\n")

    # Demande à l'utilisateur la taille minimale des fichiers en Mo
    try:
        taille_mini_mo = float(input("-> Taille minimale des fichiers en Mo (ex: 10) : ").strip())
    except ValueError:
        taille_mini_mo = 10.0  # Valeur par defaut si entree incorrecte
        print("[INFO] Valeur incorrecte, utilisation de 10 Mo par defaut.")

    # Demande à l'utilisateur le nombre maximum de fichiers à afficher
    try:
        nb_max_fichiers = int(input("-> Nombre maximum de fichiers à conserver (ex: 100) : ").strip())
    except ValueError:
        nb_max_fichiers = 100  # Valeur par defaut
        print("[INFO] Valeur incorrecte, utilisation de 100 fichiers par defaut.")

    print("\n========== Debut de l'analyse ==========\n")

    # 5) Construction de la liste des fichiers dans le repertoire
    fichiers = construire_liste_fichiers(repertoire_de_base)
    print(f"=> Nombre total de fichiers trouves : {len(fichiers)}")

    # 6) Tri des fichiers par taille decroissante
    fichiers_tries = trier_par_taille_desc(fichiers)

    # 7) Filtrage des fichiers selon les critères de taille et de nombre
    fichiers_filtres = filtrer_fichiers(fichiers_tries, taille_mini_mo, nb_max_fichiers)
    print(f"=> Nombre de fichiers après filtrage : {len(fichiers_filtres)}")

    if not fichiers_filtres:
        print("! Aucun fichier ne correspond aux critères de filtrage.\n")

    # 8) Creation du fichier JSON dans le dossier du script
    dossier_script = Path(__file__).resolve().parent
    nom_fichier_json = dossier_script.joinpath("fichiers_gros.json")

    exporter_en_json(fichiers_filtres, str(nom_fichier_json))
    print(f"\n[OK] Fichier JSON genere ici : {nom_fichier_json.resolve()}")

    # 9) Affiche un aperçu des premiers fichiers filtres (max 5)
    if fichiers_filtres:
        print("\n========== Aperçu des fichiers retenus ==========")
        for f in fichiers_filtres[:5]:
            print(f"  - {f['chemin_complet']} (taille : {f['taille_octets']} octets)")

    print("\n========== Fin de l'analyse ==========\n")

if __name__ == "__main__":
    main()
