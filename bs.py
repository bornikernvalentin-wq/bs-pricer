import numpy as np
from scipy.stats import norm

def d1_d2 (S,K,T,r,sigma, q) : 
    
    d1 = (np.log(S/K) + (r-q + (sigma**2/2))*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    return(d1, d2)


def prix_call (S,K,T,r,sigma,q) : 
    
    prix = S*np.exp(-q*T)*norm.cdf(d1_d2(S,K,T,r,sigma,q)[0]) - K*np.exp(-r*T)*norm.cdf(d1_d2(S,K,T,r,sigma,q)[1])
    
    return(prix)


def prix_put (S,K,T,r,sigma,q) : 
    
    prix = -S*np.exp(-q*T)*norm.cdf(-d1_d2(S,K,T,r,sigma,q)[0]) + K*np.exp(-r*T)*norm.cdf(-d1_d2(S,K,T,r,sigma,q)[1])
    
    return(prix)

