# lancescripts.ps1
Param(
    [string]$pythonPath = "python"  # Définit le chemin de Python, valeur par défaut "python"
)

Write-Host "=== 1) Lancement de l'interface PyQt (searchgraph.py) ==="

# Lancer searchgraph.py pour choisir un répertoire
$rep_base = & $pythonPath ".\searchgraph.py"

Write-Host "Répertoire sélectionné : '$rep_base'"

# Vérification du répertoire
if (-not $rep_base) {
    Write-Host "Aucun répertoire sélectionné."
    exit
}
if (!(Test-Path $rep_base)) {
    Write-Host "Répertoire invalide."
    exit
}

Write-Host "=== 2) Lancement de script1.py (analyse + JSON) ==="
# Lancer script1.py avec le répertoire choisi
& $pythonPath ".\script1.py" "$rep_base"

Write-Host "=== 3) Vérification du fichier fichiers_gros.json ==="
# Vérifier si le fichier JSON est généré
if (Test-Path ".\fichiers_gros.json") {
    Write-Host "fichiers_gros.json généré avec succès."
    Write-Host "=== 4) Lancement de script3.py (lecture JSON + interface) ==="
    # Lancer script3.py pour afficher l'interface
    & $pythonPath ".\script3.py"
}
else {
    Write-Host "ERREUR : fichiers_gros.json non trouvé."
    Write-Host "script3.py non lancé."
}

Write-Host "=== Fin du script PowerShell ==="
