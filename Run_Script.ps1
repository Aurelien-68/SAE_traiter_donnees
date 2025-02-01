# lancescripts.ps1
Param(
    [string]$pythonPath = "python"  # Definit le chemin de Python, valeur par defaut "python"
)

Write-Host "=== 1) Lancement de l'interface PyQt (searchgraph.py) ==="

# Lancer searchgraph.py pour choisir un repertoire
$rep_base = & $pythonPath ".\searchgraph.py"

Write-Host "Repertoire selectionne : '$rep_base'"

# Verification du repertoire
if (-not $rep_base) {
    Write-Host "Aucun repertoire selectionne."
    exit
}
if (!(Test-Path $rep_base)) {
    Write-Host "Repertoire invalide."
    exit
}

Write-Host "=== 2) Lancement de script1.py (analyse + JSON) ==="
# Lancer script1.py avec le repertoire choisi
& $pythonPath ".\script1.py" "$rep_base"

Write-Host "=== 3) Verification du fichier fichiers_gros.json ==="
# Verifier si le fichier JSON est genere
if (Test-Path ".\fichiers_gros.json") { #Test-Path:vérifie si un fichier ou un dossier existe.
    Write-Host "fichiers_gros.json genere avec succes."
    Write-Host "=== 4) Lancement de script3.py (lecture JSON + interface) ==="
    # Lancer script3.py pour afficher l'interface
    & $pythonPath ".\script3.py"
}
else {
    Write-Host "ERREUR : fichiers_gros.json non trouve."
    Write-Host "script3.py non lance."
}

Write-Host "=== Fin du script PowerShell ==="
