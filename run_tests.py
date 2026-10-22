"""Lance tous les tests du projet.

Dans Spyder : ouvre ce fichier et appuie sur F5. C'est tout.
Marche quel que soit le dossier de travail de la console, et utilise
toujours le Python de la console Spyder (donc celui du .venv).
"""
import subprocess
import sys
from pathlib import Path

racine = Path(__file__).resolve().parent  # dossier de ce fichier = racine du projet

res = subprocess.run(
    [sys.executable, "-m", "pytest", "-v"],
    cwd=racine,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
)
print(res.stdout)
print(res.stderr)
print("=> TOUS LES TESTS PASSENT" if res.returncode == 0 else "=> IL Y A DES ECHECS (voir au-dessus)")
