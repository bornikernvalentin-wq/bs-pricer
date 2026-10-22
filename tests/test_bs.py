from bs import prix_call, prix_put


def test_valeurs_reference():
    # S=100, K=100, T=1 an, r=5 %, sigma=20 %, q=0 : valeurs classiques de manuel
    call = prix_call(100, 100, 1, 0.05, 0.20, 0)
    put = prix_put(100, 100, 1, 0.05, 0.20, 0)

    assert abs(call - 10.4506) < 1e-3
    assert abs(put - 5.5735) < 1e-3
