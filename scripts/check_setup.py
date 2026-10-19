"""
Verifie que l'atelier est pret : les bibliotheques s'importent, et yfinance
peut parler au reseau. Lance-le avec `python scripts/check_setup.py` juste
apres `pip install -r requirements.txt`.

Ce script est de l'outillage (cours I.1) : il ne fait partie d'aucun
exercice note, il sert seulement a diagnostiquer l'installation.
"""

import sys


def check_imports():
    names = ["numpy", "scipy", "pandas", "matplotlib", "pytest", "yfinance"]
    ok = True
    for name in names:
        try:
            module = __import__(name)
            version = getattr(module, "__version__", "?")
            print(f"  [ok] {name} {version}")
        except ImportError as exc:
            print(f"  [ECHEC] {name} : {exc}")
            ok = False
    return ok


def check_yfinance_network():
    import yfinance as yf

    try:
        df = yf.Ticker("^GSPC").history(period="5d")
    except Exception as exc:  # reseau coupe, DNS, Yahoo qui bloque, etc.
        print(f"  [ECHEC reseau] {type(exc).__name__}: {exc}")
        print("  -> normal si tu es hors ligne ou derriere un proxy/pare-feu")
        print("     restrictif ; relance depuis ta machine personnelle.")
        return False

    if df.empty:
        print("  [ECHEC] la requete a reussi mais n'a renvoye aucune ligne")
        return False

    print(f"  [ok] {len(df)} lignes recues, derniere cloture : "
          f"{df['Close'].iloc[-1]:.2f}")
    return True


if __name__ == "__main__":
    print("1. Imports des bibliotheques")
    imports_ok = check_imports()

    print("\n2. Appel reseau yfinance (S&P 500, 5 derniers jours)")
    network_ok = check_yfinance_network() if imports_ok else False

    print("\nResume :", "tout est pret." if imports_ok and network_ok
          else "il reste un point a corriger avant l'exercice 0.4.")
    sys.exit(0 if imports_ok and network_ok else 1)
