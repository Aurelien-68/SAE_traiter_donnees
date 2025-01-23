# lancescripts.ps1
Param(
    [string]$pythonPath = "python"  # ou "C:\Python39\python.exe" si besoin
)

Write-Host "=== 1) Lancement de l'interface PyQt (searchgraph.py) pour sélectionner un répertoire ==="

# Lance searchgraph.py et récupère le répertoire sélectionné sur la sortie standard
$rep_base = & $pythonPath ".\searchgraph.py"

Write-Host "Répertoire sélectionné : '$rep_base'"

# Vérifications
if (-not $rep_base) {
    Write-Host "Aucun répertoire n'a été sélectionné ou l'utilisateur a annulé."
    exit
}
if (!(Test-Path $rep_base)) {
    Write-Host "Le répertoire '$rep_base' n'existe pas ou est invalide."
    exit
}

Write-Host "=== 2) Lancement de script1.py (analyse + génération du JSON) avec le répertoire ==="
& $pythonPath ".\script1.py" "$rep_base"

Write-Host "=== 3) Vérification de la présence du fichier fichiers_gros.json ==="
if (Test-Path ".\fichiers_gros.json") {
    Write-Host "Le fichier fichiers_gros.json a été généré avec succès."
    Write-Host "=== 4) Lancement de script3.py (lecture du JSON + interface) ==="
    & $pythonPath ".\script3.py"
}
else {
    Write-Host "ERREUR : Le fichier fichiers_gros.json n'a pas été trouvé."
    Write-Host "script3.py ne sera pas lancé."
}

Write-Host "=== Fin du script PowerShell ==="
