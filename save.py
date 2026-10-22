"""Sauvegarde le projet sur GitHub (git add + commit + push).

Dans Spyder : ouvre ce fichier et appuie sur F5.
Pour un message précis, change la variable MESSAGE ci-dessous.
Un commit = une étape qui marche (ex. "prix_call et prix_put corrects").
"""
import subprocess
from datetime import datetime
from pathlib import Path

MESSAGE = ""  # laisse vide pour un message automatique avec la date

racine = Path(__file__).resolve().parent
msg = MESSAGE or f"Sauvegarde du {datetime.now():%d/%m/%Y %H:%M}"


def git(*args):
    r = subprocess.run(["git", *args], cwd=racine, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    print("$ git", " ".join(args))
    print(r.stdout + r.stderr)
    return r.returncode


git("add", "-A")
git("commit", "-m", msg)   # code 1 + "nothing to commit" = normal si rien n'a changé
git("push")
print("Terminé. Vérifie sur GitHub que le commit apparaît.")
