import pytest
from bs import prix_call, prix_put
import numpy as np

def test_valeurs_reference():
    # S=100, K=100, T=1 an, r=5 %, sigma=20 %, q=0 : valeurs classiques de manuel
    call = prix_call(100, 100, 1, 0.05, 0.20, 0)
    put = prix_put(100, 100, 1, 0.05, 0.20, 0)

    assert abs(call - 10.4506) < 1e-3
    assert abs(put - 5.5735) < 1e-3

def test_pariteCP() : 
    
    S = 90
    K = 105
    T = 1
    r = 0.02
    sigma = 0.25
    q = 0.01
    
    assert(abs(prix_call(S, K, T, r, sigma, q) - prix_put(S, K, T, r, sigma, q) - (S*np.exp(-q*T) - K*np.exp(-r*T)))) < 1e-10
    
    
def test_bornesC() : 
    
    S = 90
    grilleK = np.linspace(80, 120, 41)
    T = 1
    r = 0.02
    sigma = 0.25
    q = 0.01
    
    assert(np.all(S*np.exp(-q*T) > prix_call(S, grilleK, T, r, sigma, q)))
    assert(np.all(prix_call(S, grilleK, T, r, sigma, q) > np.maximum(S*np.exp(-q*T) - grilleK*np.exp(-r*T),0)))


def test_bornesP() : 
    
    S = 90
    grilleK = np.linspace(80, 120, 41)
    T = 1
    r = 0.02
    sigma = 0.25
    q = 0.01
    
    assert(np.all(grilleK*np.exp(-r*T) > prix_put(S, grilleK, T, r, sigma, q)))
    assert(np.all(prix_put(S, grilleK, T, r, sigma, q) > np.maximum(grilleK*np.exp(-r*T)- S*np.exp(-q*T),0)))

def test_monotonie():
    
    S = 90
    grilleK = np.linspace(80, 120, 41)
    T = 1
    r = 0.02
    sigma = 0.20
    q = 0.01

    assert(np.all(np.diff(prix_call(S,grilleK,T,r,sigma,q)) <= 0))

    sigma = np.linspace(0.05, 1, 41)
    K = 105
    
    assert(np.all(np.diff(prix_call(S,K,T,r,sigma,q)) >= 0))
    
def test_convexite():
    
    grilleK = np.linspace(80, 120, 41)
    S = 90
    T = 1
    r = 0.02
    sigma = 0.20
    q = 0.01
    
    assert(np.all(prix_call(S,grilleK,T,r,sigma,q)[1:-1] <= (prix_call(S,grilleK,T,r,sigma,q)[:-2] + prix_call(S,grilleK,T,r,sigma,q)[2:])/2))

@pytest.mark.parametrize("fonction", [prix_call, prix_put])
@pytest.mark.parametrize("args", [
    (0, 100, 1, 0.05, 0.2, 0),       # S nul
    (-5, 100, 1, 0.05, 0.2, 0),      # S négatif
    (100, 0, 1, 0.05, 0.2, 0),       # K nul
    (100, -5, 1, 0.05, 0.2, 0),      # K négatif
    (100, 100, -1, 0.05, 0.2, 0),    # T négatif
    (100, 100, 1, 0.05, -0.2, 0),    # sigma négatif
])
def test_entrees_invalides(fonction, args):
    with pytest.raises(ValueError):
        fonction(*args)


def test_T_nul_renvoie_le_payoff():
    assert prix_call(120, 100, 0, 0.05, 0.2, 0.01) == 20
    assert prix_call(80, 100, 0, 0.05, 0.2, 0.01) == 0
    assert prix_put(80, 100, 0, 0.05, 0.2, 0.01) == 20
    assert prix_put(120, 100, 0, 0.05, 0.2, 0.01) == 0


def test_sigma_nul_est_la_limite_de_la_formule():
    for S, K in [(100, 20), (100, 90), (100, 100), (90, 105)]:
        args = (S, K, 1, 0.05)
        assert abs(prix_call(*args, 0, 0.01) - prix_call(*args, 1e-6, 0.01)) < 1e-4
        assert abs(prix_put(*args, 0, 0.01) - prix_put(*args, 1e-6, 0.01)) < 1e-4


def test_cas_limites_sans_nan():
    resultats = [
        prix_call(100, 100, 0, 0.05, 0.2, 0),
        prix_put(100, 100, 0, 0.05, 0.2, 0),
        prix_call(100, 100, 1, 0.05, 0, 0),
        prix_put(100, 100, 1, 0.05, 0, 0),
    ]
    assert not np.any(np.isnan(resultats))


def test_melange_de_zero_et_positif_refuse():
    with pytest.raises(ValueError):
        prix_call(100, 100, 1, 0.05, np.array([0.0, 0.2]), 0)
    with pytest.raises(ValueError):
        prix_put(100, 100, np.array([0.0, 1.0]), 0.05, 0.2, 0)
