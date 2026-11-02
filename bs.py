import numpy as np
from scipy.stats import norm

def d1_d2 (S,K,T,r,sigma, q) : 
    
    d1 = (np.log(S/K) + (r-q + (sigma**2/2))*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    return(d1, d2)


def prix_call (S,K,T,r,sigma,q) : 
    
    # 1. Entrées impossibles
    if not np.all(S > 0) :
        raise ValueError("S doit être strictement positif")
    if not np.all(K > 0) :
        raise ValueError("K doit être strictement positif")
    if not np.all(T >= 0) : 
        raise ValueError("T ne doit pas être négatif")
    if not np.all(sigma >= 0) : 
        raise ValueError("sigma ne doit pas être négatif")
    
    # 2. Cas limites
    if np.all(T == 0) : 
        return(np.maximum(S - K, 0))
    if np.all(sigma == 0) : 
        return(np.maximum(S*np.exp(-q*T) - K*np.exp(-r*T), 0))
    
    # 3. Mélange de 0 et de valeurs positives : refusé
    if not np.all(T > 0) : 
        raise ValueError("T : mélange de 0 et de valeurs positives non géré")
    if not np.all(sigma > 0) : 
        raise ValueError("sigma : mélange de 0 et de valeurs positives non géré")
    
    # 4. Formule
    d1, d2 = d1_d2(S,K,T,r,sigma,q)
    prix = S*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    
    return(prix)


def prix_put (S,K,T,r,sigma,q) : 
    
    # 1. Entrées impossibles
    if not np.all(S > 0) :
        raise ValueError("S doit être strictement positif")
    if not np.all(K > 0) :
        raise ValueError("K doit être strictement positif")
    if not np.all(T >= 0) : 
        raise ValueError("T ne doit pas être négatif")
    if not np.all(sigma >= 0) : 
        raise ValueError("sigma ne doit pas être négatif")
    
    # 2. Cas limites
    if np.all(T == 0) : 
        return(np.maximum(K - S, 0))
    if np.all(sigma == 0) : 
        return(np.maximum(K*np.exp(-r*T) - S*np.exp(-q*T), 0))
    
    # 3. Mélange de 0 et de valeurs positives : refusé
    if not np.all(T > 0) : 
        raise ValueError("T : mélange de 0 et de valeurs positives non géré")
    if not np.all(sigma > 0) : 
        raise ValueError("sigma : mélange de 0 et de valeurs positives non géré")
    
    # 4. Formule
    d1, d2 = d1_d2(S,K,T,r,sigma,q)
    prix = -S*np.exp(-q*T)*norm.cdf(-d1) + K*np.exp(-r*T)*norm.cdf(-d2)
    
    return(prix)

def greeks (option, S, K, T, r, sigma, q) :
    
    # Entrées : les grecques ne sont définies que pour S, K, T, sigma > 0
    if option not in ("call", "put") :
        raise ValueError("option doit valoir 'call' ou 'put'")
    if not np.all(S > 0) :
        raise ValueError("S doit être strictement positif")
    if not np.all(K > 0) :
        raise ValueError("K doit être strictement positif")
    if not np.all(T > 0) :
        raise ValueError("T doit être strictement positif")
    if not np.all(sigma > 0) :
        raise ValueError("sigma doit être strictement positif")
    
    d1, d2 = d1_d2(S, K, T, r, sigma, q)
    
    # Termes qui reviennent
    A = S*np.exp(-q*T)        # spot actualisé du dividende
    B = K*np.exp(-r*T)        # strike actualisé
    
    # Grecques du call (valeurs brutes : vega pour sigma en décimale, theta par an)
    delta = np.exp(-q*T)*norm.cdf(d1)
    gamma = np.exp(-q*T)*norm.pdf(d1)/(S*sigma*np.sqrt(T))
    vega = A*norm.pdf(d1)*np.sqrt(T)
    theta = -A*norm.pdf(d1)*sigma/(2*np.sqrt(T)) + q*A*norm.cdf(d1) - r*B*norm.cdf(d2)
    
    # Le put se déduit du call par la parité (gamma et vega identiques)
    if option == "put" :
        delta = delta - np.exp(-q*T)
        theta = theta - q*A + r*B
    
    return(delta, gamma, theta, vega)